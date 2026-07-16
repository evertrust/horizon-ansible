"""Test the handwritten Horizon client against licensed Horizon releases.

The generated SDK is used only to provision and verify isolated server-side
fixtures.  The installed Ansible collection continues to execute its current
handwritten HTTP client.
"""

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
HORIZON_IMAGES = {
    "2.8.10": (
        "quay.io/evertrust/horizon:2.8.10@"
        "sha256:d9181a2e9b372ac7e2955cc29142db1711084deeca86c415229e06cd42e11eec"
    ),
    "2.9.4": (
        "quay.io/evertrust/horizon:2.9.4@"
        "sha256:a1c79cea6183092e31033054cb46d88aa808d2f87458ff82cf4527a5b3b50fec"
    ),
    "2.10.3": (
        "quay.io/evertrust/horizon:2.10.3@"
        "sha256:ee768f89889332b1aedb9497db4ecaad11df7bc0ad8805b36423a3fa4786c981"
    ),
}
DEFAULT_IMAGES = tuple(HORIZON_IMAGES)
ADMIN_API_ID = "administrator"
ADMIN_API_KEY = "sample_password"
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
    def __init__(self, version, network, mongodb_uri, license_path, application_path):
        self.container = DockerContainer(HORIZON_IMAGES[version]).with_exposed_ports(9000)
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


def level():
    return horizon.AuthorizationLevel(accessLevel="authorized")


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

        authorization = horizon.CertificateProfileAuthorizationLevels(
            enroll=level(),
            enrollApi=level(),
            requestEnroll=level(),
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
                authorizedKeyTypes=["rsa-2048", "rsa-4096"],
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


def integration_targets(collection):
    targets_root = collection / "tests/integration/targets"
    targets = sorted(path.name for path in targets_root.iterdir() if (path / "tasks/main.yml").is_file())
    if not targets:
        raise RuntimeError("No integration targets were found in the installed artifact")
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


EXPECTED_API_WARNINGS = (
    "Profile does not exist or is disabled",
    "Label element 'unexistantLabel' is not authorized",
    "UnknownTeam",
    "already revoked",
    "Nonce not found in jwt",
    "Could not parse provided PEM",
    "Unknown algorithm",
)


def audit_horizon_log(path):
    """Fail when Horizon reports an unexpected request-level failure."""
    successful_submissions = 0
    malformed_csr_failures = 0
    pop_challenges = 0
    unexpected = []

    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if '"code":"REQUEST-SUBMIT"' in line:
            if '"status":"success"' in line:
                successful_submissions += 1
            elif '"status":"failure"' in line:
                if "Could not parse provided PEM" in line and "certrequest" in line:
                    malformed_csr_failures += 1
                else:
                    unexpected.append(line[:500])

        if (
            '"code":"SEC-AUTHENTICATION"' in line
            and '"apiError","value":"SEC-AUTH-010"' in line
        ):
            pop_challenges += 1

        if "/api/v1/" in line and ("[WARN]" in line or "[ERROR]" in line):
            if not any(expected.lower() in line.lower() for expected in EXPECTED_API_WARNINGS):
                unexpected.append(line[:500])

    if successful_submissions == 0:
        unexpected.append("Horizon did not log any successful REQUEST-SUBMIT events")
    if malformed_csr_failures > 1:
        unexpected.append(
            "Expected at most one deliberate malformed-CSR failure, found %s"
            % malformed_csr_failures
        )
    if unexpected:
        raise RuntimeError(
            "Unexpected Horizon request failures in %s:\n%s"
            % (path, "\n".join(unexpected))
        )

    print(
        "Horizon request audit: %s successful submissions, "
        "%s expected malformed CSR failures, %s PoP nonce challenges"
        % (successful_submissions, malformed_csr_failures, pop_challenges)
    )


def run_version(version, license_path, application_path, collection_root, source_root, environment, run_id):
    network = mongodb = server = None
    result = None
    audit_error = None
    integration_started = False
    collection = collection_root / "ansible_collections/evertrust/horizon"
    config_path = collection / "tests/integration/integration_config.yml"
    log_prefix = "horizon-handwritten-image-%s-%s" % (version, run_id)
    log_path = source_root / "tests/output" / ("%s-matrix.log" % log_prefix)
    server_log_path = source_root / "tests/output" / ("%s-server.log" % log_prefix)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        network = Network().create()
        mongodb = MongoDB(network)
        server = HorizonServer(version, network, mongodb.in_network_uri, license_path, application_path)
        provision_horizon(server.endpoint)
        config_path.write_text(
            json.dumps({
                "endpoint": server.endpoint,
                "x_api_id": ADMIN_API_ID,
                "x_api_key": ADMIN_API_KEY,
            }) + "\n",
            encoding="utf-8",
        )
        config_path.chmod(0o600)
        test_environment = ansible_test_environment(collection_root, environment)
        ansible_test = shutil.which("ansible-test")
        if ansible_test is None:
            raise RuntimeError("ansible-test is not available in PATH")
        integration_started = True
        with log_path.open("w", encoding="utf-8") as log:
            result = subprocess.run(
                [
                    ansible_test,
                    "integration",
                    *integration_targets(collection),
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
    finally:
        config_path.unlink(missing_ok=True)
        if server is not None:
            server.write_logs(server_log_path)
            if integration_started:
                try:
                    audit_horizon_log(server_log_path)
                except Exception as exception:
                    audit_error = exception
            server.stop()
        if mongodb is not None:
            mongodb.stop()
        if network is not None:
            network.remove()
    if audit_error is not None:
        raise audit_error
    return result.returncode, log_path


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--license",
        default=os.environ.get("HORIZON_LICENSE_PATH"),
        help="Path to a Horizon license (or set HORIZON_LICENSE_PATH)",
    )
    parser.add_argument(
        "--images",
        nargs="+",
        default=DEFAULT_IMAGES,
        choices=DEFAULT_IMAGES,
        metavar="VERSION",
    )
    parser.add_argument(
        "--artifact",
        type=Path,
        help="Use an existing collection artifact instead of building one in temporary storage",
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
    failures = []
    run_id = uuid4().hex[:12]
    with tempfile.TemporaryDirectory(prefix="horizon-matrix-") as directory:
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
        print("Built one matrix artifact: %s" % artifact.name)
        print(
            "Provisioning-only SDK: Anto-test-hrz %s (collection uses handwritten HTTP)"
            % horizon.__version__
        )
        print("MongoDB image: %s" % MONGODB_IMAGE)
        for version in args.images:
            print("Running Horizon %s (%s)" % (version, HORIZON_IMAGES[version]), flush=True)
            try:
                return_code, log_path = run_version(
                    version,
                    license_path,
                    application_path,
                    collection_root,
                    source_root,
                    environment,
                    run_id,
                )
            except Exception as exception:
                failures.append(version)
                print("FAIL Horizon %s during fixture setup (%s)" % (version, type(exception).__name__))
                traceback.print_exc()
                continue
            if return_code == 0:
                print("PASS Horizon %s" % version)
            else:
                failures.append(version)
                print("FAIL Horizon %s; see %s" % (version, log_path))
    if failures:
        raise SystemExit("Horizon matrix failed: %s" % ", ".join(failures))


if __name__ == "__main__":
    main()
