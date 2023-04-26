# Horizon Ansible

This collection includes plenty of modules to interact with Horizon instances and automate your certificate management workflows.

## Installation

### System requirements

This collection requires Python 3.6 or greater. It offers compatibility with the following Horizon versions :

| Collection version | Horizon version |
|--------------------|-----------------|
| 1.2.0              | 2.2.0+          |
| 1.1.0              | 2.2.0+          |
| 1.0.1              | 2.0.0+          |


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

Some modules require external Python dependencies (mainly the `cryptography` module), which are not installed by `ansible-galaxy`. They can be manually installed using pip:

    pip install requirements.txt


## Documentation

The full documentation for this collection can be found at [evertrust.github.io/horizon-ansible/html](https://evertrust.github.io/horizon-ansible).

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE.md](LICENSE.md) to see the full text.
