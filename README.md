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
[evertrust.horizon.horizon_inventory](https://github.com/EverTrust/horizon-ansible/blob/main/docs/evertrust.horizon.horizon_inventory.asciidoc) | Horizon inventory

### Lookup plugins
Name | Description
--- | ---
[evertrust.horizon.horizon_lookup](https://github.com/EverTrust/horizon-ansible/blob/main/docs/evertrust.horizon.horizon_lookup.asciidoc) | Look up informations about a certificate 

### Action plugins
Name | Description
--- | ---
[evertrust.horizon.horizon_feed](https://github.com/EverTrust/horizon-ansible/blob/main/docs/evertrust.horizon.horizon_feed_action.asciidoc) | Feed a certificate to Horizon
[evertrust.horizon.horizon_enroll](https://github.com/EverTrust/horizon-ansible/blob/main/docs/evertrust.horizon.horizon_enroll_action.asciidoc) | Enroll a certificate
[evertrust.horizon.horizon_recover](https://github.com/EverTrust/horizon-ansible/blob/main/docs/evertrust.horizon.horizon_recover_action.asciidoc) | Recover a certificate
[evertrust.horizon.horizon_revoke](https://github.com/EverTrust/horizon-ansible/blob/main/docs/evertrust.horizon.horizon_revoke_action.asciidoc) | Revoke a certificate
[evertrust.horizon.horizon_update](https://github.com/EverTrust/horizon-ansible/blob/main/docs/evertrust.horizon.horizon_update_action.asciidoc) | Update a certificate

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

See [LICENSE.md]() to see the full text.
