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

.. _ansible_collections.evertrust.horizon.horizon_enroll_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

evertrust.horizon.horizon_enroll module -- Horizon enrollment plugin
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This module is part of the `evertrust.horizon collection <https://galaxy.ansible.com/evertrust/horizon>`_ (version 1.1.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install evertrust.horizon`.

    To use it in a playbook, specify: :code:`evertrust.horizon.horizon_enroll`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Performs an enrollment against the Horizon API.

.. note::
    This module has a corresponding :ref:`action plugin <action_plugins>`.

.. Aliases


.. Requirements

Requirements
------------
The below requirements are needed on the host that executes this module.

- cryptography>=3.4.0






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

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-ca_bundle:

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

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-client_cert:

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

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-client_key:

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
        <div class="ansibleOptionAnchor" id="parameter-csr"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-csr:

      .. rst-class:: ansible-option-title

      **csr**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-csr" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      A certificate signing request, or the path to the CSR file.

      If none is provided, one will be generated on-the-fly.


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-csr/src"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-csr/src:

      .. rst-class:: ansible-option-title

      **src**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-csr/src" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`path`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      The path to a CSR file


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-endpoint"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-endpoint:

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
        <div class="ansibleOptionAnchor" id="parameter-key_type"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-key_type:

      .. rst-class:: ansible-option-title

      **key_type**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-key_type" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Key type.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`rsa-256`
      - :ansible-option-choices-entry:`rsa-512`
      - :ansible-option-choices-entry:`rsa-1024`
      - :ansible-option-choices-entry:`rsa-2048`
      - :ansible-option-choices-entry:`rsa-3072`
      - :ansible-option-choices-entry:`rsa-4096`
      - :ansible-option-choices-entry:`rsa-8192`
      - :ansible-option-choices-entry:`ec-secp256r1`
      - :ansible-option-choices-entry:`ec-secp384r1`
      - :ansible-option-choices-entry:`ec-secp521r1`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-labels"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-labels:

      .. rst-class:: ansible-option-title

      **labels**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-labels" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate's labels.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-mode"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-mode:

      .. rst-class:: ansible-option-title

      **mode**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-mode" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enrollment mode.

      If empty, will be inferred from the Horizon certificate profile configuration.


      .. rst-class:: ansible-option-line

      :ansible-option-choices:`Choices:`

      - :ansible-option-choices-entry:`centralized`
      - :ansible-option-choices-entry:`decentralized`

      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-owner"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-owner:

      .. rst-class:: ansible-option-title

      **owner**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-owner" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate's owner


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-password"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-password:

      .. rst-class:: ansible-option-title

      **password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Security password for the certificate.

      Password policies will be applied to check validity.

      Required only if the enrollement is centralized and the password generation mode is not random.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-profile"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-profile:

      .. rst-class:: ansible-option-title

      **profile**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-profile" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Name of the profile that will be used to enroll the certificate.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-sans"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-sans:

      .. rst-class:: ansible-option-title

      **sans**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-sans" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate's subject alternative names (SANs) of the certificate.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-subject"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-subject:

      .. rst-class:: ansible-option-title

      **subject**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-subject" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary` / :ansible-option-required:`required`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate's subject.

      You can either give the description of the subject, or the full DN.

      If you give the dn, other values won't be used.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-team"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-team:

      .. rst-class:: ansible-option-title

      **team**

      .. raw:: html

        <a class="ansibleOptionLink" href="#parameter-team" title="Permalink to this option"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate's team.


      .. raw:: html

        </div>

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-x_api_id"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-x_api_id:

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

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__parameter-x_api_key:

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
   - Enrolling a certificate requires permissions on the related profile.
   - Be sure to use the "Enroll API" permission instead of "Enroll".

.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    - name: Enrolling a certificate in a centralized way
      evertrust.horizon.horizon_enroll:
        endpoint: "https://<horizon-endpoint>"
        x_api_id: "<horizon-id>"
        x_api_key: "<horizon-password>"
        mode: "centralized"
        password: "examplePassword"
        key_type: "rsa-2048"
        profile: "exampleProfile"
        subject:
          cn.1: "exampleCN"
        sans:
          dnsname.1: "exampleDnsname"
        labels:
          snow_id: "value1"
          exp_tech: "value2"

    - name: Enrolling a certificate in a decentralized way with a CSR
      evertrust.horizon.horizon_enroll:
        endpoint: "https://<horizon-endpoint>"
        x_api_id: "<horizon-id>"
        x_api_key: "<horizon-password>"
        mode: "decentralized"
        csr: "CSR content"
        password: "examplePassword"
        key_type: "rsa-2048"
        profile: "exampleProfile"
        subject:
          cn.1: "exampleCN"
          ou.1: "exampleFirstOU"
          ou.2: "exampleSecondOU"
        sans:
          dnsname:
            - "exampleDnsName1"
            - "exampleDnsName2"
        labels:
          snow_id: "value1"
          exp_tech: "value2"

    - name: Enrolling a certificate in a decentralized way without CSR
      evertrust.horizon.horizon_enroll:
        endpoint: "https://<horizon-endpoint>"
        x_api_id: "<horizon-id>"
        x_api_key: "<horizon-password>"
        mode: "decentralized"
        password: "examplePassword"
        key_type: "rsa-2048"
        profile: "exampleProfile"
        subject:
          cn.1: "exampleCN"
          ou:
            - "exampleFirstOU"
            - "exampleSecondOU"
        sans:
          dnsname.1: "exampleDnsName"
        labels:
          label1: "value1"
          label2: "value2"




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this module:

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate:

      .. rst-class:: ansible-option-title

      **certificate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Enrolled certificate object


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/_id"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/_id:

      .. rst-class:: ansible-option-title

      **_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/_id" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Horizon internal certificate ID.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/certificate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/certificate:

      .. rst-class:: ansible-option-title

      **certificate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/certificate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate in PEM format.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/crlSynchronized"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/crlsynchronized:

      .. rst-class:: ansible-option-title

      **crlSynchronized**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/crlSynchronized" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      True if the revocation status was reconciled from the CRL


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveredTrusted"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoveredtrusted:

      .. rst-class:: ansible-option-title

      **discoveredTrusted**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveredTrusted" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      True if the certificate was discovered and trusted.

      False if the certificate was discovered.

      Absent if the certificate was not discovered.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryData"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoverydata:

      .. rst-class:: ansible-option-title

      **discoveryData**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryData" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate discovery data.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Only if the certificate was discovered.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryData/hostnames"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoverydata/hostnames:

      .. rst-class:: ansible-option-title

      **hostnames**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryData/hostnames" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Host hostnames.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryData/ip"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoverydata/ip:

      .. rst-class:: ansible-option-title

      **ip**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryData/ip" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Host IP address


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryData/operatingSystems"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoverydata/operatingsystems:

      .. rst-class:: ansible-option-title

      **operatingSystems**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryData/operatingSystems" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Host operating systems


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryData/paths"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoverydata/paths:

      .. rst-class:: ansible-option-title

      **paths**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryData/paths" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Host paths.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryData/tlsPorts"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoverydata/tlsports:

      .. rst-class:: ansible-option-title

      **tlsPorts**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryData/tlsPorts" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Host TLS ports.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryData/tlsPorts/port"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoverydata/tlsports/port:

      .. rst-class:: ansible-option-title

      **port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryData/tlsPorts/port" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Port number.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryData/tlsPorts/version"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoverydata/tlsports/version:

      .. rst-class:: ansible-option-title

      **version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryData/tlsPorts/version" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      TLS version.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryData/usages"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoverydata/usages:

      .. rst-class:: ansible-option-title

      **usages**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryData/usages" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate usages.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryInfo"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoveryinfo:

      .. rst-class:: ansible-option-title

      **discoveryInfo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryInfo" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate's discovery info


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryInfo/campaign"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoveryinfo/campaign:

      .. rst-class:: ansible-option-title

      **campaign**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryInfo/campaign" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Campaign name.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryInfo/identifier"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoveryinfo/identifier:

      .. rst-class:: ansible-option-title

      **identifier**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryInfo/identifier" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Horizon user that discovered the certificate.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/discoveryInfo/lastDiscoveryDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/discoveryinfo/lastdiscoverydate:

      .. rst-class:: ansible-option-title

      **lastDiscoveryDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/discoveryInfo/lastDiscoveryDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Last discovery date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/dn"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/dn:

      .. rst-class:: ansible-option-title

      **dn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/dn" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate DN.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/holderId"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/holderid:

      .. rst-class:: ansible-option-title

      **holderId**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/holderId" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate holder ID.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/issuer"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/issuer:

      .. rst-class:: ansible-option-title

      **issuer**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/issuer" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate issuer DN.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/keyType"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/keytype:

      .. rst-class:: ansible-option-title

      **keyType**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/keyType" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate key type.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/labels"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/labels:

      .. rst-class:: ansible-option-title

      **labels**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/labels" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate labels.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/labels/key"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/labels/key:

      .. rst-class:: ansible-option-title

      **key**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/labels/key" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Label key


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/labels/value"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/labels/value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/labels/value" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Label value


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/metadata"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/metadata:

      .. rst-class:: ansible-option-title

      **metadata**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/metadata" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate metadata.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/metadata/key"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/metadata/key:

      .. rst-class:: ansible-option-title

      **key**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/metadata/key" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Metadata key


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/metadata/value"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/metadata/value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/metadata/value" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Metadata value


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/module"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/module:

      .. rst-class:: ansible-option-title

      **module**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/module" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate module.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/notAfter"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/notafter:

      .. rst-class:: ansible-option-title

      **notAfter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/notAfter" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate expiration date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/notBefore"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/notbefore:

      .. rst-class:: ansible-option-title

      **notBefore**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/notBefore" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate issuance date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/owner"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/owner:

      .. rst-class:: ansible-option-title

      **owner**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/owner" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate's owner.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/profile"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/profile:

      .. rst-class:: ansible-option-title

      **profile**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/profile" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate profile.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/publicKeyThumbprint"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/publickeythumbprint:

      .. rst-class:: ansible-option-title

      **publicKeyThumbprint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/publicKeyThumbprint" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate public key thumbprint.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/revocationDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/revocationdate:

      .. rst-class:: ansible-option-title

      **revocationDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/revocationDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate revocation date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/revocationReason"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/revocationreason:

      .. rst-class:: ansible-option-title

      **revocationReason**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/revocationReason" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate revocation reason.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/selfSigned"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/selfsigned:

      .. rst-class:: ansible-option-title

      **selfSigned**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/selfSigned" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      True if the certificate is self-signed.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/serial"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/serial:

      .. rst-class:: ansible-option-title

      **serial**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/serial" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate serial number (hexadecimal format).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/signingAlgorithm"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/signingalgorithm:

      .. rst-class:: ansible-option-title

      **signingAlgorithm**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/signingAlgorithm" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate signing algorithm.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/subjectAlternateNames"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/subjectalternatenames:

      .. rst-class:: ansible-option-title

      **subjectAlternateNames**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/subjectAlternateNames" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate subject alternate names (SANs).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/subjectAlternateNames/sanType"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/subjectalternatenames/santype:

      .. rst-class:: ansible-option-title

      **sanType**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/subjectAlternateNames/sanType" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      SAN type


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/subjectAlternateNames/value"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/subjectalternatenames/value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/subjectAlternateNames/value" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      SAN value


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/team"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/team:

      .. rst-class:: ansible-option-title

      **team**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/team" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate's team.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/thirdPartyData"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/thirdpartydata:

      .. rst-class:: ansible-option-title

      **thirdPartyData**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/thirdPartyData" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate third-party data.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/thirdPartyData/connector"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/thirdpartydata/connector:

      .. rst-class:: ansible-option-title

      **connector**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/thirdPartyData/connector" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Third party connector name.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/thirdPartyData/fingerprint"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/thirdpartydata/fingerprint:

      .. rst-class:: ansible-option-title

      **fingerprint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/thirdPartyData/fingerprint" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Third party object fingerprint.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/thirdPartyData/id"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/thirdpartydata/id:

      .. rst-class:: ansible-option-title

      **id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/thirdPartyData/id" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Third party object ID.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/thirdPartyData/pushDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/thirdpartydata/pushdate:

      .. rst-class:: ansible-option-title

      **pushDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/thirdPartyData/pushDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate's push date in the third party (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/thirdPartyData/removeDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/thirdpartydata/removedate:

      .. rst-class:: ansible-option-title

      **removeDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/thirdPartyData/removeDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate's remove date in the third party (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/thumbprint"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/thumbprint:

      .. rst-class:: ansible-option-title

      **thumbprint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/thumbprint" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate public key thumbprint.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/triggerResults"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/triggerresults:

      .. rst-class:: ansible-option-title

      **triggerResults**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/triggerResults" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate trigger results.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/triggerResults/detail"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/triggerresults/detail:

      .. rst-class:: ansible-option-title

      **detail**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/triggerResults/detail" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Execution details.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/triggerResults/event"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/triggerresults/event:

      .. rst-class:: ansible-option-title

      **event**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/triggerResults/event" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Trigger event type.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/triggerResults/lastExecutionDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/triggerresults/lastexecutiondate:

      .. rst-class:: ansible-option-title

      **lastExecutionDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/triggerResults/lastExecutionDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Last trigger execution date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/triggerResults/name"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/triggerresults/name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/triggerResults/name" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Trigger name.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/triggerResults/nextDelay"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/triggerresults/nextdelay:

      .. rst-class:: ansible-option-title

      **nextDelay**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/triggerResults/nextDelay" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Duration until next try.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/triggerResults/nextExecutionDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/triggerresults/nextexecutiondate:

      .. rst-class:: ansible-option-title

      **nextExecutionDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/triggerResults/nextExecutionDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Next trigger execution date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/triggerResults/retries"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/triggerresults/retries:

      .. rst-class:: ansible-option-title

      **retries**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/triggerResults/retries" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Trigger retries count.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate/triggerResults/status"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-certificate/triggerresults/status:

      .. rst-class:: ansible-option-title

      **status**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate/triggerResults/status" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Trigger type.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>




  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-chain"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-chain:

      .. rst-class:: ansible-option-title

      **chain**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-chain" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate's trust chain


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-key"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-key:

      .. rst-class:: ansible-option-title

      **key**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-key" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate's private key


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If enrollement mode is "centralized" or if a key pair was generated on-the-fly


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-p12"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-p12:

      .. rst-class:: ansible-option-title

      **p12**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-p12" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Base64-encoded PKCS#12


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If enrollement mode is "centralized" or if a key pair was generated on-the-fly


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-p12_password"></div>

      .. _ansible_collections.evertrust.horizon.horizon_enroll_module__return-p12_password:

      .. rst-class:: ansible-option-title

      **p12_password**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-p12_password" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      PKCS#12 password


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If enrollement mode is "centralized" or if a key pair was generated on-the-fly


      .. raw:: html

        </div>



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

