"""Test the SDK-backed collection against one licensed Horizon image."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
from uuid import uuid4

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID
import horizon
import httpx
from pymongo import MongoClient
from pymongo.errors import PyMongoError
from testcontainers.core.container import DockerContainer
from testcontainers.core.network import Network


MONGODB_IMAGE = (
    "mongo:8.2.10@sha256:1286be0f98b0da2575280a7a07e50446dfd707d683fd8e51937526b6e3c65fd9"
)
ADMIN_API_ID = "administrator"
ADMIN_API_KEY = "sample_password"
REQUESTER_API_ID = "ansible-requester"
REQUESTER_API_KEY = "Ansible-Requester-42!"
APPLICATION_SECRET = "This-is-a-long-string-used-for-1"
KEYSET = (
    '{"primaryKeyId":654595919,"key":[{"keyData":'
    '{"typeUrl":"type.googleapis.com/google.crypto.tink.AesGcmKey",'
    '"value":"GiDCRlT8qXbwAwgC7eu0HZrHXqUwGgFSh+NT9nBPRncHIw==",'
    '"keyMaterialType":"SYMMETRIC"},"status":"ENABLED",'
    '"keyId":654595919,"outputPrefixType":"TINK"}]}'
)
ADMIN_PASSWORD_HASH = (
    "$6$9HA6fehfu7Ae0Luz$IFRCiN.UF3tKFCyOO/EO5ib8438r8GfZgYAZFbPZIBZHQQyX6mN1Wmw6mkN10X84XG1x9lncmEZpv59kpIwy.0"
)


class MongoDB:
    def __init__(self, network):
        self.alias = "mongodb-%s" % uuid4().hex[:8]
        self.container = DockerContainer(MONGODB_IMAGE).with_exposed_ports(27017)
        self.container.with_env("MONGO_INITDB_ROOT_USERNAME", "ato")
        self.container.with_env("MONGO_INITDB_ROOT_PASSWORD", "testpwd")
        self.container.with_env("MONGO_INITDB_DATABASE", "mongoDBTest")
        self.container.with_network(network)
        self.container.with_network_aliases(self.alias)
        self.container.start()
        self.in_network_uri = "mongodb://ato:testpwd@%s:27017/mongoDBTest?authSource=admin" % self.alias
        host_uri = "mongodb://ato:testpwd@%s:%s/mongoDBTest?authSource=admin" % (
            self.container.get_container_host_ip(),
            self.container.get_exposed_port(27017),
        )
        self._wait_ready(host_uri)

    @staticmethod
    def _wait_ready(uri, timeout=30):
        deadline = time.monotonic() + timeout
        error = None
        with MongoClient(uri, serverSelectionTimeoutMS=1000) as client:
            while time.monotonic() < deadline:
                try:
                    client.admin.command("ping")
                    return
                except PyMongoError as exception:
                    error = exception
                    time.sleep(0.5)
        raise RuntimeError("MongoDB did not become ready: %s" % type(error).__name__)

    def stop(self):
        self.container.stop()


class HorizonServer:
    def __init__(self, image, network, mongodb_uri, license_path, application_path):
        self.container = DockerContainer(image).with_exposed_ports(9000)
        self.container.with_volume_mapping(str(license_path), "/horizon/license.txt", "ro")
        self.container.with_volume_mapping(str(application_path), "/opt/horizon/etc/application.conf", "ro")
        environment = {
            "LICENSE_PATH": "/horizon/license.txt",
            "APPLICATION_SECRET": APPLICATION_SECRET,
            "EVENT_SEAL_SECRET": APPLICATION_SECRET,
            "KEYSET": KEYSET,
            "MONGODB_URI": mongodb_uri,
            "HOSTS_ALLOWED.0": ".",
            "HOSTNAME": "127.0.0.1",
            "HRZ_ADMIN_PWD_HASH": ADMIN_PASSWORD_HASH,
        }
        for key, value in environment.items():
            self.container.with_env(key, value)
        self.container.with_network(network)
        self.container.start()
        self.endpoint = "http://%s:%s" % (
            self.container.get_container_host_ip(),
            self.container.get_exposed_port(9000),
        )
        self._wait_ready()

    def _wait_ready(self, timeout=120):
        deadline = time.monotonic() + timeout
        error = None
        while time.monotonic() < deadline:
            try:
                ready = self.container.exec([
                    "sh",
                    "-c",
                    "curl -fsS --max-time 2 http://127.0.0.1:7626/ready >/dev/null",
                ])
                if ready.exit_code == 0:
                    response = httpx.get(self.endpoint + "/", timeout=2)
                    if response.status_code < 500:
                        return
                    error = "HTTP %s" % response.status_code
                else:
                    error = ready.output.decode(errors="replace").strip()
            except Exception as exception:
                error = type(exception).__name__
            self.container.get_wrapped_container().reload()
            if self.container.get_wrapped_container().status == "exited":
                break
            time.sleep(1)
        raise RuntimeError("Horizon did not become ready: %s" % error)

    def stop(self):
        self.container.stop()

    def write_logs(self, path):
        stdout, stderr = self.container.get_logs()
        path.write_bytes(stdout + b"\n" + stderr)


def generate_test_ca(common_name):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    subject = issuer = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, common_name)])
    now = datetime.now(timezone.utc)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(issuer)
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=5))
        .not_valid_after(now + timedelta(days=3650))
        .add_extension(x509.BasicConstraints(ca=True, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=False,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=True,
                crl_sign=True,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(x509.SubjectKeyIdentifier.from_public_key(private_key.public_key()), critical=False)
        .sign(private_key, hashes.SHA256())
    )
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    ).decode()
    certificate_pem = certificate.public_bytes(serialization.Encoding.PEM).decode()
    return private_key_pem, certificate_pem


def sdk_configuration(endpoint):
    configuration = horizon.Configuration(host=endpoint)
    configuration.api_key["apiId"] = ADMIN_API_ID
    configuration.api_key["apiKey"] = ADMIN_API_KEY
    configuration.debug = False
    return configuration


def level(access_level="authorized"):
    return horizon.AuthorizationLevel(accessLevel=access_level)


def provision_horizon(endpoint):
    ca_key, ca_certificate = generate_test_ca("test-integrated-ca")
    localized = [horizon.LocalizedString(lang="en", value="Ansible integration")]
    with horizon.ApiClient(sdk_configuration(endpoint)) as client:
        connector = horizon.IntegratedCAConnector(
            name="test-integrated-ca",
            type="integrated",
            cryptoType="legacy",
            caKey=horizon.SecretString(value=ca_key),
            caCert=ca_certificate,
            crtLifetime="30 days",
            crlLifetime="7 days",
            crtBackDate="5 minutes",
            checkPop=True,
        )
        horizon.PkiConnectorApi(client).pki_connector_add(horizon.PKIConnectors(connector))
        horizon.CaApi(client).ca_add(
            horizon.CertificateAuthorityRequest(
                name="test-integrated-ca",
                certificate=ca_certificate,
                trustedForClientAuthentication=True,
                trustedForServerAuthentication=True,
                outdatedRevocationStatusPolicy="lastavailablestatus",
                public=True,
                downloadable=True,
            )
        )
        for label in ("label-1", "label-2"):
            horizon.CertificateLabelApi(client).label_add(
                horizon.Label(name=label, displayName=localized, description=localized)
            )
        for team in ("TeamA", "TeamB"):
            horizon.SecurityTeamApi(client).security_team_add(
                horizon.Team(name=team, displayName=localized, description=localized)
            )

        identity_api = horizon.SecurityIdentityLocalApi(client)
        identity_api.security_identity_local_add(
            horizon.LocalIdentityOnAdd(
                identifier=REQUESTER_API_ID,
                name="Ansible enrollment requester",
            )
        )
        horizon.SecurityPrincipalinfoApi(client).security_principal_info_add(
            horizon.PrincipalInfo(
                identifier=REQUESTER_API_ID,
                enabled=True,
            )
        )
        identity_api.security_identity_local_password_set(
            horizon.SetPasswordRequest(
                identifier=REQUESTER_API_ID,
                password=REQUESTER_API_KEY,
            )
        )

        authorization = horizon.CertificateProfileAuthorizationLevels(
            enroll=level(),
            enrollApi=level(),
            requestEnroll=level("authenticated"),
            approveEnroll=level(),
            revoke=level(),
            requestRevoke=level(),
            approveRevoke=level(),
            search=level(),
            update=level(),
            requestUpdate=level(),
            approveUpdate=level(),
            recover=level(),
            recoverApi=level(),
            requestRecover=level(),
            approveRecover=level(),
            renew=level(),
            renewApi=level(),
            requestRenew=level(),
            approveRenew=level(),
        )
        profile = horizon.WebRAProfile(
            module="webra",
            name="Ansible",
            displayName=localized,
            description=localized,
            authorizationMode="authorized",
            enabled=True,
            pkiConnector="test-integrated-ca",
            certificateTemplate=horizon.CertificateTemplate(
                subject=[
                    horizon.DNElement(
                        type=name,
                        mandatory=name == "CN",
                        editableByRequester=True,
                        editableByApprover=True,
                    )
                    for name in ("CN", "O", "OU")
                ],
                sans=[
                    horizon.SANElement(
                        type=name,
                        editableByRequester=True,
                        editableByApprover=True,
                        min=0,
                        max=10,
                    )
                    for name in ("DNSNAME", "RFC822NAME")
                ],
                labels=[
                    horizon.LabelElement(
                        label=name,
                        mandatory=False,
                        editableByRequester=True,
                        editableByApprover=True,
                    )
                    for name in ("label-1", "label-2")
                ],
                teamPolicy=horizon.TeamPolicy(
                    editableByRequester=True,
                    editableByApprover=True,
                    mandatory=False,
                    whitelist=["TeamA", "TeamB"],
                ),
            ),
            authorizationLevels=authorization,
            requestsPolicy=horizon.RequestsPolicy(),
            cryptoPolicy=horizon.ManagedCertificateProfileCryptoPolicy(
                centralized=True,
                decentralized=True,
                defaultKeyType="rsa-2048",
                authorizedKeyTypes=["rsa-2048", "rsa-4096", "ec-secp384r1"],
                preferredEnrollmentMode="centralized",
                escrow=True,
                p12passwordMode="random",
                p12storeEncryptionType="DES_AVERAGE",
                showP12PasswordOnEnroll=True,
                showP12OnEnroll=True,
                showP12PasswordOnRecover=True,
                showP12OnRecover=True,
                keyAvailability="7 days",
            ),
            selfPermissions=horizon.CertificateProfileSelfPermissions(
                selfRecover=True,
                selfUpdate=True,
                selfRevoke=True,
                selfRenew=True,
                selfPopRenew=True,
                selfPopRevoke=True,
                selfPopUpdate=True,
            ),
            renewalPeriod="30 days",
        )
        horizon.CertificateProfileApi(client).certificate_profile_add(horizon.CertificateProfiles(profile))
        horizon.DiscoveryCampaignApi(client).discovery_campaign_add(
            horizon.DiscoveryCampaign(
                name="Ansible",
                description="Ansible integration",
                authorizationLevels=horizon.DiscoveryCampaignAuthorizationLevels(
                    search=level(),
                    feed=level(),
                ),
                eventOnSuccess=False,
                eventOnWarning=False,
                eventOnFailure=False,
                hosts=["localhost"],
                ports=["443"],
                enabled=True,
            )
        )

        # Fail before running Ansible if Horizon accepted a create request but
        # did not make one of the fixtures available.  The integration targets
        # rely on these objects to exercise profile, team, label, and discovery
        # policy validation rather than merely testing request submission.
        label_api = horizon.CertificateLabelApi(client)
        for label in ("label-1", "label-2"):
            if label_api.label_get(label).name != label:
                raise RuntimeError("Horizon label fixture was not persisted: %s" % label)
        team_api = horizon.SecurityTeamApi(client)
        for team in ("TeamA", "TeamB"):
            if team_api.security_team_get(team).name != team:
                raise RuntimeError("Horizon team fixture was not persisted: %s" % team)
        stored_profile = horizon.CertificateProfileApi(client).certificate_profile_get("Ansible")
        if stored_profile.actual_instance.name != "Ansible":
            raise RuntimeError("Horizon certificate profile fixture was not persisted")
        stored_campaign = horizon.DiscoveryCampaignApi(client).discovery_campaign_get("Ansible")
        if stored_campaign.name != "Ansible" or not stored_campaign.enabled:
            raise RuntimeError("Horizon discovery campaign fixture was not persisted or enabled")


def build_and_install(source_root, work_root, environment, artifact=None):
    ansible_galaxy = shutil.which("ansible-galaxy")
    if ansible_galaxy is None:
        raise RuntimeError("ansible-galaxy is not available in PATH")
    collection_root = work_root / "collections"
    collection_root.mkdir()
    if artifact is None:
        artifact_dir = work_root / "artifact"
        artifact_dir.mkdir()
        subprocess.run(
            [ansible_galaxy, "collection", "build", "--force", "--output-path", str(artifact_dir)],
            cwd=source_root,
            env=environment,
            check=True,
        )
        artifacts = list(artifact_dir.glob("*.tar.gz"))
        if len(artifacts) != 1:
            raise RuntimeError("Expected one collection artifact, found %s" % len(artifacts))
        artifact = artifacts[0]
    else:
        artifact = artifact.expanduser().resolve()
        if not artifact.is_file():
            raise RuntimeError("Collection artifact is not a file: %s" % artifact)
    subprocess.run(
        [
            ansible_galaxy,
            "collection",
            "install",
            "--force",
            "-p",
            str(collection_root),
            str(artifact),
        ],
        env=environment,
        check=True,
    )
    integration_requirements = source_root / "tests/integration/requirements.yml"
    subprocess.run(
        [
            ansible_galaxy,
            "collection",
            "install",
            "--force",
            "-p",
            str(collection_root),
            "-r",
            str(integration_requirements),
        ],
        env=environment,
        check=True,
    )
    crypto_manifest = collection_root / "ansible_collections/community/crypto/MANIFEST.json"
    crypto_metadata = json.loads(crypto_manifest.read_text(encoding="utf-8"))["collection_info"]
    print(
        "Ansible collection: %s.%s %s"
        % (crypto_metadata["namespace"], crypto_metadata["name"], crypto_metadata["version"])
    )
    return artifact, collection_root


def integration_targets(collection, selected_targets=None):
    targets_root = collection / "tests/integration/targets"
    targets = sorted(path.name for path in targets_root.iterdir() if (path / "tasks/main.yml").is_file())
    if not targets:
        raise RuntimeError("No integration targets were found in the installed artifact")
    if selected_targets:
        missing = sorted(set(selected_targets) - set(targets))
        if missing:
            raise RuntimeError("Unknown integration target(s): %s" % ", ".join(missing))
        return selected_targets
    return targets


def ansible_test_environment(collection_root, environment):
    test_environment = environment.copy()
    if sys.platform == "darwin":
        # Ansible forks module workers.  macOS proxy discovery loads
        # Objective-C frameworks and otherwise aborts a worker when their
        # first initialization happens after that fork.
        test_environment.setdefault("OBJC_DISABLE_INITIALIZE_FORK_SAFETY", "YES")
    existing_collections = str(Path.home() / ".ansible/collections")
    test_environment["ANSIBLE_COLLECTIONS_PATH"] = "%s:%s" % (collection_root, existing_collections)
    return test_environment


def image_log_label(image):
    return "".join(
        character if character.isalnum() or character in ".-_" else "-"
        for character in image
    ).strip("-")


def run_image(
    image,
    license_path,
    application_path,
    collection_root,
    source_root,
    environment,
    run_id,
    selected_targets=None,
):
    network = mongodb = server = None
    collection = collection_root / "ansible_collections/evertrust/horizon"
    config_path = collection / "tests/integration/integration_config.yml"
    sdk_version = horizon.__version__
    log_prefix = "horizon-sdk-%s-image-%s-%s" % (sdk_version, image_log_label(image), run_id)
    log_path = source_root / "tests/output" / ("%s-ansible.log" % log_prefix)
    server_log_path = source_root / "tests/output" / ("%s-server.log" % log_prefix)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        network = Network().create()
        mongodb = MongoDB(network)
        server = HorizonServer(image, network, mongodb.in_network_uri, license_path, application_path)
        provision_horizon(server.endpoint)
        config_path.write_text(
            json.dumps({
                "endpoint": server.endpoint,
                "x_api_id": ADMIN_API_ID,
                "x_api_key": ADMIN_API_KEY,
                "requester_x_api_id": REQUESTER_API_ID,
                "requester_x_api_key": REQUESTER_API_KEY,
                "approver_x_api_id": ADMIN_API_ID,
                "approver_x_api_key": ADMIN_API_KEY,
            }) + "\n",
            encoding="utf-8",
        )
        config_path.chmod(0o600)
        test_environment = ansible_test_environment(collection_root, environment)
        ansible_test = shutil.which("ansible-test")
        if ansible_test is None:
            raise RuntimeError("ansible-test is not available in PATH")
        with log_path.open("w", encoding="utf-8") as log:
            result = subprocess.run(
                [
                    ansible_test,
                    "integration",
                    *integration_targets(collection, selected_targets),
                    "-v",
                    "--color",
                    "no",
                    "--python-interpreter",
                    sys.executable,
                ],
                cwd=collection,
                env=test_environment,
                stdout=log,
                stderr=subprocess.STDOUT,
                check=False,
            )
        return result.returncode, log_path
    finally:
        config_path.unlink(missing_ok=True)
        if server is not None:
            server.write_logs(server_log_path)
            server.stop()
        if mongodb is not None:
            mongodb.stop()
        if network is not None:
            network.remove()


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--license",
        default=os.environ.get("HORIZON_LICENSE_PATH"),
        help="Path to a Horizon license (or set HORIZON_LICENSE_PATH)",
    )
    parser.add_argument(
        "--image",
        required=True,
        help="Fully qualified Horizon container image reference",
    )
    parser.add_argument(
        "--artifact",
        type=Path,
        help="Use an existing collection artifact instead of building one in temporary storage",
    )
    parser.add_argument(
        "--target",
        action="append",
        dest="targets",
        help="Run only this integration target (repeat for more than one target)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.license:
        raise SystemExit("A Horizon license path is required")
    license_path = Path(args.license).expanduser().resolve()
    if not license_path.is_file():
        raise SystemExit("The Horizon license path is not a file")
    source_root = Path(__file__).resolve().parents[2]
    environment = os.environ.copy()
    run_id = uuid4().hex[:12]
    with tempfile.TemporaryDirectory(prefix="horizon-integration-") as directory:
        work_root = Path(directory)
        application_path = work_root / "application.conf"
        application_path.write_text("play.http.session.secure = false\n", encoding="utf-8")
        ansible_local_temp = work_root / "ansible-local"
        ansible_local_temp.mkdir()
        environment["ANSIBLE_LOCAL_TEMP"] = str(ansible_local_temp)
        artifact, collection_root = build_and_install(
            source_root,
            work_root,
            environment,
            artifact=args.artifact,
        )
        print("Built integration artifact: %s" % artifact.name)
        print("SDK distribution: evertrust-horizon %s (import horizon)" % horizon.__version__)
        print("MongoDB image: %s" % MONGODB_IMAGE)
        print("Running Horizon image %s" % args.image, flush=True)
        try:
            return_code, log_path = run_image(
                args.image,
                license_path,
                application_path,
                collection_root,
                source_root,
                environment,
                run_id,
                selected_targets=args.targets,
            )
        except Exception as exception:
            print("FAIL Horizon fixture setup (%s)" % type(exception).__name__)
            traceback.print_exc()
            raise SystemExit("Horizon integration setup failed")
        if return_code != 0:
            raise SystemExit("Horizon integration failed; see %s" % log_path)
        print("PASS Horizon image %s" % args.image)


if __name__ == "__main__":
    main()
