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

.. _ansible_collections.evertrust.horizon.horizon_revoke_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

evertrust.horizon.horizon_revoke module -- Horizon revoke plugin
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `evertrust.horizon collection <https://galaxy.ansible.com/evertrust/horizon>`_ (version 1.1.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install evertrust.horizon`.

    To use it in a playbook, specify: :code:`evertrust.horizon.horizon_revoke`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Performs an revocation against the Horizon API.

.. note::
    This module has a corresponding :ref:`action plugin <action_plugins>`.

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

      .. _ansible_collections.evertrust.horizon.horizon_revoke_module__parameter-ca_bundle:

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
        <div class="ansibleOptionAnchor" id="parameter-certificate_pem"></div>

      .. _ansible_collections.evertrust.horizon.horizon_revoke_module__parameter-certificate_pem:

      .. rst-class:: ansible-option-title

      **certificate_pem**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-certificate_pem" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A certificate string in the PEM format, or the path to the certificate PEM file.


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-certificate_pem/src"></div>

      .. _ansible_collections.evertrust.horizon.horizon_revoke_module__parameter-certificate_pem/src:

      .. rst-class:: ansible-option-title

      **src**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-certificate_pem/src" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The path to a certificate PEM file


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-client_cert"></div>

      .. _ansible_collections.evertrust.horizon.horizon_revoke_module__parameter-client_cert:

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

      .. _ansible_collections.evertrust.horizon.horizon_revoke_module__parameter-client_key:

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

      .. _ansible_collections.evertrust.horizon.horizon_revoke_module__parameter-endpoint:

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
        <div class="ansibleOptionAnchor" id="parameter-revocation_reason"></div>

      .. _ansible_collections.evertrust.horizon.horizon_revoke_module__parameter-revocation_reason:

      .. rst-class:: ansible-option-title

      **revocation_reason**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-revocation_reason" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Revocation reason


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`UNSPECIFIED`
      - :ansible-option-choices-entry:`KEYCOMPROMISE`
      - :ansible-option-choices-entry:`CACOMPROMISE`
      - :ansible-option-choices-entry:`AFFILIATIONCHANGE`
      - :ansible-option-choices-entry:`SUPERSEDED`
      - :ansible-option-choices-entry:`CESSATIONOFOPERATION`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-skip_already_revoked"></div>

      .. _ansible_collections.evertrust.horizon.horizon_revoke_module__parameter-skip_already_revoked:

      .. rst-class:: ansible-option-title

      **skip_already_revoked**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-skip_already_revoked" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Do not raise an exception when the certificate is already revoked


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-default-bold:`no` :ansible-option-default:`← (default)`
      - :ansible-option-choices-entry:`yes`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-x_api_id"></div>

      .. _ansible_collections.evertrust.horizon.horizon_revoke_module__parameter-x_api_id:

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

      .. _ansible_collections.evertrust.horizon.horizon_revoke_module__parameter-x_api_key:

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

Notes
-----

.. note::
   - Revoking a certificate requires permissions on the related profile.

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: Revoke a certificate by its content
        evertrust.horizon.horizon_revoke:
          endpoint: "https://<horizon-endpoint>"
          x_api_id: "<horizon-id>"
          x_api_key: "<horizon-password>"
          certificate_pem: "-----BEGIN CERTIFICATE----- ... -----END CERTIFICATE-----"
          skip_already_revoked: true

    - name: Revoke a certificate by its file
        evertrust.horizon.horizon_revoke:
          endpoint: "https://<horizon-endpoint>"
          x_api_id: "<horizon-id>"
          x_api_key: "<horizon-password>"
          certificate_pem:
            src: /pem/file/path




.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Evertrust R&D (@EverTrust)



.. Extra links

Collection links
~~~~~~~~~~~~~~~~

.. raw:: html

  <p class="ansible-links">
    <a href="https://github.com/EverTrust/horizon-ansible/issues" aria-role="button" target="_blank" rel="noopener external">Issue Tracker</a>
    <a href="https://github.com/EverTrust/horizon-ansible" aria-role="button" target="_blank" rel="noopener external">Repository (Sources)</a>
  </p>

.. Parsing errors

