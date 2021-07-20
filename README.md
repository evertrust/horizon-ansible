# Evertrust Horizon Collection

The Ansible Evertrust Horizon collection includes a vaiety of Ansible content to help the utilistation of Horizon instances.  

<!-- Start requires_ansible -->
## Ansible version compatibility

This collectino has been tested against following versions >= 2.11.2.  
<!-- End requires_ansible -->

## Python version compatibility

This collection requires Python 3.5 or greater.

<!-- Start collection content -->
## Included content

### Inventory plugins
Name | Description
--- | ---
[evertrust.horizon.horizon_inventory](https://github.com/EverTrust/horizon-ansible/blob/main/plugins/inventory/horizon_inventory.py) | Horizon inventory

### Lookup plugins
Name | Description
--- | ---
[evertrust.horizon.horizon_lookup](https://github.com/EverTrust/horizon-ansible/blob/main/plugins/lookup/horizon_lookup.py) | Look up informations about a certificate 

### Action plugins
Name | Description
--- | ---
[evertrust.horizon.horzon_enroll](https://github.com/EverTrust/horizon-ansible/blob/main/plugins/action/horizon_enroll.py) | Enroll a certificate
[evertrust.horizon.horzon_recover](https://github.com/EverTrust/horizon-ansible/blob/main/plugins/action/horizon_recover.py) | Recover a certificate
[evertrust.horizon.horzon_revoke](https://github.com/EverTrust/horizon-ansible/blob/main/plugins/action/horizon_revoke.py) | Revoke a certificate
[evertrust.horizon.horzon_update](https://github.com/EverTrust/horizon-ansible/blob/main/plugins/action/horizon_update.py) | Update a certificate

<!-- End collection content -->

## Installing the collection

You can install the Horizon collection wth the Ansible Galaxy CLI:

    ansible-collection collection install evertrust.horizon

You can also nclude it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: evertrust.horizon
```

The python module dependencies are not installed by `ansible-galaxy`. They can be manually installed using pip:

    pip install requirements.txt