# Horizon Ansible

This collection includes plenty of modules to interact with Horizon instances and automate your certificate management workflows.

## Installation

### System requirements

This collection requires Python 3.11 or greater and `ansible-core` 2.19.11 or
greater (but earlier than 2.21). It offers compatibility with the following
Horizon versions:

| Collection version | Horizon version |
|--------------------|-----------------|
| 1.5.1              | 2.8.x, 2.9.x, 2.10.x |
| 1.5                | 2.2.0+          |
| 1.4                | 2.2.0+          |
| 1.3                | 2.2.0 - 2.4.x   |
| 1.2                | 2.2.0 - 2.3.x   |
| 1.1                | 2.2.0 - 2.3.x   |
| 1.0                | 2.0.0 - 2.3.x   |


### Ansible Galaxy
You can install the Horizon collection with the Ansible Galaxy CLI:

    ansible-galaxy collection install evertrust.horizon

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: evertrust.horizon
```

### Dependencies

The collection uses the Horizon SDK distributed as `evertrust-horizon` and
imported in Python as `horizon`. Python dependencies are not installed by
`ansible-galaxy`; install them with:

    pip install -r requirements.txt

Install these dependencies in the Python environment used by the Ansible
controller because Horizon action, lookup, and inventory plugins execute there.

### Authentication

Provide either a complete API-key pair (`x_api_id` and `x_api_key`) or a
complete mTLS pair (`client_cert` and `client_key`). Partial pairs and empty
values are rejected locally. If both complete pairs are supplied, mTLS takes
precedence.

Renewal, revocation, and update actions may instead authenticate through proof
of possession when they receive the certificate's `private_key`. A private key
passed to the import action is certificate payload, not authentication, so
import still requires a complete API-key or mTLS pair.

### Change and check-mode behavior

Successful enrollment, feed, import, recovery, renewal, revocation, and update
actions report `changed: true`. A revocation ignored through
`skip_already_revoked` reports `changed: false`, and template reads always
report `changed: false`.

In Ansible check mode, mutating Horizon actions do not contact Horizon. They
return `skipped: true` with `changed: true` as a prediction that running the
operation normally would perform a change. Template reads remain available in
check mode.


## Documentation

The full documentation for this collection can be found at [evertrust.github.io/horizon-ansible](https://evertrust.github.io/horizon-ansible/).

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE.md](LICENSE.md) to see the full text.
