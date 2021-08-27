# Evertrust Horizon Collection

The Ansible Evertrust Horizon collection includes a variety of Ansible content to help the utilistation of Horizon instances.  

<!-- Start requires_ansible -->
## Ansible version compatibility

This collection has been tested against following versions >= 2.11.2.  
<!-- End requires_ansible -->

## Python version compatibility

This collection requires Python 3.5 or greater.

<!-- Start collection content -->
## Included content

### Inventory plugins
Name | Description
--- | ---
[evertrust.horizon.inventory](docs/evertrust.horizon.inventory.asciidoc) | Horizon inventory

### Lookup plugins
Name | Description
--- | ---
[evertrust.horizon.lookup](docs/evertrust.horizon.lookup.asciidoc) | Look up informations about a certificate 

### Action plugins
Name | Description
--- | ---
[evertrust.horizon.feed](docs/evertrust.horizon.feed_action.asciidoc) | Feed a certificate to Horizon
[evertrust.horizon.enroll](docs/evertrust.horizon.enroll_action.asciidoc) | Enroll a certificate
[evertrust.horizon.recover](docs/evertrust.horizon.recover_action.asciidoc) | Recover a certificate
[evertrust.horizon.revoke](docs/evertrust.horizon.revoke_action.asciidoc) | Revoke a certificate
[evertrust.horizon.update](docs/evertrust.horizon.update_action.asciidoc) | Update a certificate

<!-- End collection content -->

## Installing the collection

You can install the Horizon collection with the Ansible Galaxy CLI:

    ansible-collection collection install evertrust.horizon

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: evertrust.horizon
```

The python module dependencies are not installed by `ansible-galaxy`. They can be manually installed using pip:

    pip install requirements.txt

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE.md](LICENSE.md) to see the full text.
