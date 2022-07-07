.. Document meta

:orphan:

.. |antsibull-internal-nbsp| unicode:: 0xA0
    :trim:

.. role:: ansible-attribute-support-label
.. role:: ansible-attribute-support-property
.. role:: ansible-attribute-support-full
.. role:: ansible-attribute-support-partial
.. role:: ansible-attribute-support-none
.. role:: ansible-attribute-support-na
.. role:: ansible-option-type
.. role:: ansible-option-elements
.. role:: ansible-option-required
.. role:: ansible-option-versionadded
.. role:: ansible-option-aliases
.. role:: ansible-option-choices
.. role:: ansible-option-choices-entry
.. role:: ansible-option-default
.. role:: ansible-option-default-bold
.. role:: ansible-option-configuration
.. role:: ansible-option-returned-bold
.. role:: ansible-option-sample-bold

.. Anchors

.. _ansible_collections.evertrust.horizon.horizon_inventory_inventory:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

evertrust.horizon.horizon_inventory inventory -- Horizon inventory plugin
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This inventory plugin is part of the `evertrust.horizon collection <https://galaxy.ansible.com/evertrust/horizon>`_ (version 1.1.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install evertrust.horizon`.

    To use it in a playbook, specify: :code:`evertrust.horizon.horizon_inventory`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Generate hosts inventory from Horizon using an HCQL query.
- Use a YAML configuration file that ends with \ :literal:`horizon\_inventory.(yml|yaml`\ ).


.. Aliases


.. Requirements






.. Options

Parameters
----------


.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Comments

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-ca_bundle"></div>

      .. _ansible_collections.evertrust.horizon.horizon_inventory_inventory__parameter-ca_bundle:

      .. rst-class:: ansible-option-title

      **ca_bundle**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-ca_bundle" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Path of a CA bundle used to validate the Horizon instance SSL certificate.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-client_cert"></div>

      .. _ansible_collections.evertrust.horizon.horizon_inventory_inventory__parameter-client_cert:

      .. rst-class:: ansible-option-title

      **client_cert**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-client_cert" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Path of a client certificate.

      Required if you use certificate based authentication


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-client_key"></div>

      .. _ansible_collections.evertrust.horizon.horizon_inventory_inventory__parameter-client_key:

      .. rst-class:: ansible-option-title

      **client_key**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-client_key" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Path of a client certificate's key.

      Required if you use certificate based authentication


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-endpoint"></div>

      .. _ansible_collections.evertrust.horizon.horizon_inventory_inventory__parameter-endpoint:

      .. rst-class:: ansible-option-title

      **endpoint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-endpoint" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Your Horizon instance base endpoint.

      It must include the protocol (https://) and no trailing slash nor path.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-fields"></div>

      .. _ansible_collections.evertrust.horizon.horizon_inventory_inventory__parameter-fields:

      .. rst-class:: ansible-option-title

      **fields**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-fields" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Fields to be retrieved from Horizon.

      If omitted, all fields will be returned.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`\_id`
      - :ansible-option-choices-entry:`certificate`
      - :ansible-option-choices-entry:`discoveredTrusted`
      - :ansible-option-choices-entry:`dn`
      - :ansible-option-choices-entry:`holderId`
      - :ansible-option-choices-entry:`issuer`
      - :ansible-option-choices-entry:`keyType`
      - :ansible-option-choices-entry:`labels`
      - :ansible-option-choices-entry:`metadata`
      - :ansible-option-choices-entry:`module`
      - :ansible-option-choices-entry:`notAfter`
      - :ansible-option-choices-entry:`notBefore`
      - :ansible-option-choices-entry:`owner`
      - :ansible-option-choices-entry:`profile`
      - :ansible-option-choices-entry:`revocationDate`
      - :ansible-option-choices-entry:`revocationReason`
      - :ansible-option-choices-entry:`serial`
      - :ansible-option-choices-entry:`signingAlgorithm`
      - :ansible-option-choices-entry:`subjectAlternateNames`
      - :ansible-option-choices-entry:`thirdPartyData`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-hostnames"></div>

      .. _ansible_collections.evertrust.horizon.horizon_inventory_inventory__parameter-hostnames:

      .. rst-class:: ansible-option-title

      **hostnames**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-hostnames" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A list in order of precedence for hostname variables.

      To use labels as hostnames use the syntax label.<key>.


      .. rst-class:: ansible-option-line

      :ansible-option-default-bold:`Default:` :ansible-option-default:`[]`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-query"></div>

      .. _ansible_collections.evertrust.horizon.horizon_inventory_inventory__parameter-query:

      .. rst-class:: ansible-option-title

      **query**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-query" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      HCQL query to filter the results.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-x_api_id"></div>

      .. _ansible_collections.evertrust.horizon.horizon_inventory_inventory__parameter-x_api_id:

      .. rst-class:: ansible-option-title

      **x_api_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-x_api_id" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Horizon identifier

      Required if you use credentials authentication


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-x_api_key"></div>

      .. _ansible_collections.evertrust.horizon.horizon_inventory_inventory__parameter-x_api_key:

      .. rst-class:: ansible-option-title

      **x_api_key**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-x_api_key" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`




      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Horizon password

      Required if you use credentials authentication


      .. raw:: html

        </div>


.. Attributes


.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    plugin: evertrust.horizon.horizon_inventory

    endpoint: "https://<horizon-endpoint>"
    x_api_id: "<horizon-id>"
    x_api_key: "<horizon-password>"

    query: "null"
    # fields:

    # Possible values: san.ip, san.dns, discoveryData.ip, discoveryData.Hostname, label.<key>
    # To use your host IPs as inventory hostnames, the correct syntax would be label.ansible_host
    hostnames:
      - label.ansible_host
      - san.dns




.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Evertrust R&D (@EverTrust)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.

.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/EverTrust/horizon-ansible/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/EverTrust/horizon-ansible" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

