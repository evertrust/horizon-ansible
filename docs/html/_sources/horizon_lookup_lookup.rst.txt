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

.. _ansible_collections.evertrust.horizon.horizon_lookup_lookup:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

evertrust.horizon.horizon_lookup lookup -- Horizon lookup plugin
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This lookup plugin is part of the `evertrust.horizon collection <https://galaxy.ansible.com/evertrust/horizon>`_ (version 1.1.0).

    You might already have this collection installed if you are using the ``ansible`` package.
    It is not included in ``ansible-core``.
    To check whether it is installed, run :code:`ansible-galaxy collection list`.

    To install it, use: :code:`ansible-galaxy collection install evertrust.horizon`.

    To use it in a playbook, specify: :code:`evertrust.horizon.horizon_lookup`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Retrieve certificate's information from Horizon.


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

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__parameter-ca_bundle:

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

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__parameter-certificate_pem:

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

      A certificate in PEM format, or the path to the certificate PEM file.


      .. raw:: html

        </div>
    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="parameter-certificate_pem/src"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__parameter-certificate_pem/src:

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

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__parameter-client_cert:

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

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__parameter-client_key:

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

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__parameter-endpoint:

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

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__parameter-fields:

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
        <div class="ansibleOptionAnchor" id="parameter-x_api_id"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__parameter-x_api_id:

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

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__parameter-x_api_key:

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

    
    vars:
      endpoint: "https://<horizon-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      # Send the certificate by specifying its content (string) 
      my_pem: <a_webra_pem_file>
      # Send the certificate by specifying its file path
      pem_path:
        src: /pem/file/path
      
      # Sets a variable containing only one field (module)
      with_one: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, certificate_pem=my_pem, fields='module', endpoint=horizon_endpoint, wantlist=True) }}"

      # Sets a variable containing a list of fields (module, _id)
      with_list: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, certificate_pem=my_pem, fields=['module', '_id'], endpoint=horizon_endpoint, wantlist=True) }}"

      # Sets a variable containing every certificate field.
      without: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, certificate_pem=pem_path, endpoint=horizon_endpoint, wantlist=True) }}"




.. Facts


.. Return values

Return Value
------------

.. rst-class:: ansible-option-table

.. list-table::
  :width: 100%
  :widths: auto
  :header-rows: 1

  * - Key
    - Description

  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-_id"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-_id:

      .. rst-class:: ansible-option-title

      **_id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-_id" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Horizon internal certificate ID.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-certificate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-certificate:

      .. rst-class:: ansible-option-title

      **certificate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-certificate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate in PEM format.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-crlSynchronized"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-crlsynchronized:

      .. rst-class:: ansible-option-title

      **crlSynchronized**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-crlSynchronized" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      True if the revocation status was reconciled from the CRL


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveredTrusted"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoveredtrusted:

      .. rst-class:: ansible-option-title

      **discoveredTrusted**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveredTrusted" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      True if the certificate was discovered and trusted.

      False if the certificate was discovered.

      Absent if the certificate was not discovered.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryData"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoverydata:

      .. rst-class:: ansible-option-title

      **discoveryData**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryData" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate discovery data.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Only if the certificate was discovered.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryData/hostnames"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoverydata/hostnames:

      .. rst-class:: ansible-option-title

      **hostnames**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryData/hostnames" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Host hostnames.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryData/ip"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoverydata/ip:

      .. rst-class:: ansible-option-title

      **ip**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryData/ip" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Host IP address


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryData/operatingSystems"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoverydata/operatingsystems:

      .. rst-class:: ansible-option-title

      **operatingSystems**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryData/operatingSystems" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Host operating systems


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryData/paths"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoverydata/paths:

      .. rst-class:: ansible-option-title

      **paths**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryData/paths" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Host paths.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryData/tlsPorts"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoverydata/tlsports:

      .. rst-class:: ansible-option-title

      **tlsPorts**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryData/tlsPorts" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Host TLS ports.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryData/tlsPorts/port"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoverydata/tlsports/port:

      .. rst-class:: ansible-option-title

      **port**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryData/tlsPorts/port" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Port number.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryData/tlsPorts/version"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoverydata/tlsports/version:

      .. rst-class:: ansible-option-title

      **version**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryData/tlsPorts/version" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      TLS version.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryData/usages"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoverydata/usages:

      .. rst-class:: ansible-option-title

      **usages**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryData/usages" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate usages.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryInfo"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoveryinfo:

      .. rst-class:: ansible-option-title

      **discoveryInfo**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryInfo" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate's discovery info


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryInfo/campaign"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoveryinfo/campaign:

      .. rst-class:: ansible-option-title

      **campaign**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryInfo/campaign" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Campaign name.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryInfo/identifier"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoveryinfo/identifier:

      .. rst-class:: ansible-option-title

      **identifier**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryInfo/identifier" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Horizon user that discovered the certificate.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-discoveryInfo/lastDiscoveryDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-discoveryinfo/lastdiscoverydate:

      .. rst-class:: ansible-option-title

      **lastDiscoveryDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-discoveryInfo/lastDiscoveryDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Last discovery date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-dn"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-dn:

      .. rst-class:: ansible-option-title

      **dn**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-dn" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate DN.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-holderId"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-holderid:

      .. rst-class:: ansible-option-title

      **holderId**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-holderId" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate holder ID.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-issuer"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-issuer:

      .. rst-class:: ansible-option-title

      **issuer**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-issuer" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate issuer DN.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-keyType"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-keytype:

      .. rst-class:: ansible-option-title

      **keyType**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-keyType" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate key type.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-labels"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-labels:

      .. rst-class:: ansible-option-title

      **labels**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-labels" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate labels.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-labels/key"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-labels/key:

      .. rst-class:: ansible-option-title

      **key**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-labels/key" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Label key


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-labels/value"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-labels/value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-labels/value" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Label value


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-metadata"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-metadata:

      .. rst-class:: ansible-option-title

      **metadata**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-metadata" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate metadata.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-metadata/key"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-metadata/key:

      .. rst-class:: ansible-option-title

      **key**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-metadata/key" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Metadata key


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-metadata/value"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-metadata/value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-metadata/value" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Metadata value


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-module"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-module:

      .. rst-class:: ansible-option-title

      **module**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-module" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate module.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-notAfter"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-notafter:

      .. rst-class:: ansible-option-title

      **notAfter**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-notAfter" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate expiration date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-notBefore"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-notbefore:

      .. rst-class:: ansible-option-title

      **notBefore**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-notBefore" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate issuance date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-owner"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-owner:

      .. rst-class:: ansible-option-title

      **owner**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-owner" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate's owner.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-profile"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-profile:

      .. rst-class:: ansible-option-title

      **profile**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-profile" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate profile.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-publicKeyThumbprint"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-publickeythumbprint:

      .. rst-class:: ansible-option-title

      **publicKeyThumbprint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-publicKeyThumbprint" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate public key thumbprint.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-revocationDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-revocationdate:

      .. rst-class:: ansible-option-title

      **revocationDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-revocationDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate revocation date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-revocationReason"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-revocationreason:

      .. rst-class:: ansible-option-title

      **revocationReason**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-revocationReason" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate revocation reason.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-selfSigned"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-selfsigned:

      .. rst-class:: ansible-option-title

      **selfSigned**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-selfSigned" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`boolean`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      True if the certificate is self-signed.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-serial"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-serial:

      .. rst-class:: ansible-option-title

      **serial**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-serial" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate serial number (hexadecimal format).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-signingAlgorithm"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-signingalgorithm:

      .. rst-class:: ansible-option-title

      **signingAlgorithm**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-signingAlgorithm" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate signing algorithm.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-subjectAlternateNames"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-subjectalternatenames:

      .. rst-class:: ansible-option-title

      **subjectAlternateNames**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-subjectAlternateNames" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate subject alternate names (SANs).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-subjectAlternateNames/sanType"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-subjectalternatenames/santype:

      .. rst-class:: ansible-option-title

      **sanType**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-subjectAlternateNames/sanType" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      SAN type


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-subjectAlternateNames/value"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-subjectalternatenames/value:

      .. rst-class:: ansible-option-title

      **value**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-subjectAlternateNames/value" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      SAN value


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-thirdPartyData"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-thirdpartydata:

      .. rst-class:: ansible-option-title

      **thirdPartyData**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-thirdPartyData" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate third-party data.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-thirdPartyData/connector"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-thirdpartydata/connector:

      .. rst-class:: ansible-option-title

      **connector**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-thirdPartyData/connector" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Third party connector name.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-thirdPartyData/fingerprint"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-thirdpartydata/fingerprint:

      .. rst-class:: ansible-option-title

      **fingerprint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-thirdPartyData/fingerprint" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Third party object fingerprint.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-thirdPartyData/id"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-thirdpartydata/id:

      .. rst-class:: ansible-option-title

      **id**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-thirdPartyData/id" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Third party object ID.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-thirdPartyData/pushDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-thirdpartydata/pushdate:

      .. rst-class:: ansible-option-title

      **pushDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-thirdPartyData/pushDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate's push date in the third party (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-thirdPartyData/removeDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-thirdpartydata/removedate:

      .. rst-class:: ansible-option-title

      **removeDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-thirdPartyData/removeDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Certificate's remove date in the third party (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>



  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-thumbprint"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-thumbprint:

      .. rst-class:: ansible-option-title

      **thumbprint**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-thumbprint" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate public key thumbprint.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If specifically requested.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-triggerResults"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-triggerresults:

      .. rst-class:: ansible-option-title

      **triggerResults**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-triggerResults" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`list` / :ansible-option-elements:`elements=dictionary`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-cell">

      Certificate trigger results.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present and specifically requested.


      .. raw:: html

        </div>

    
  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-triggerResults/detail"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-triggerresults/detail:

      .. rst-class:: ansible-option-title

      **detail**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-triggerResults/detail" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Execution details.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-triggerResults/event"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-triggerresults/event:

      .. rst-class:: ansible-option-title

      **event**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-triggerResults/event" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Trigger event type.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-triggerResults/lastExecutionDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-triggerresults/lastexecutiondate:

      .. rst-class:: ansible-option-title

      **lastExecutionDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-triggerResults/lastExecutionDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Last trigger execution date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-triggerResults/name"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-triggerresults/name:

      .. rst-class:: ansible-option-title

      **name**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-triggerResults/name" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Trigger name.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-triggerResults/nextDelay"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-triggerresults/nextdelay:

      .. rst-class:: ansible-option-title

      **nextDelay**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-triggerResults/nextDelay" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Duration until next try.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-triggerResults/nextExecutionDate"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-triggerresults/nextexecutiondate:

      .. rst-class:: ansible-option-title

      **nextExecutionDate**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-triggerResults/nextExecutionDate" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Next trigger execution date (UNIX timestamp in millis).


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-triggerResults/retries"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-triggerresults/retries:

      .. rst-class:: ansible-option-title

      **retries**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-triggerResults/retries" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`integer`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Trigger retries count.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` If present.


      .. raw:: html

        </div>


  * - .. raw:: html

        <div class="ansible-option-indent"></div><div class="ansible-option-cell">
        <div class="ansibleOptionAnchor" id="return-triggerResults/status"></div>

      .. _ansible_collections.evertrust.horizon.horizon_lookup_lookup__return-triggerresults/status:

      .. rst-class:: ansible-option-title

      **status**

      .. raw:: html

        <a class="ansibleOptionLink" href="#return-triggerResults/status" title="Permalink to this return value"></a>

      .. rst-class:: ansible-option-type-line

      :ansible-option-type:`string`

      .. raw:: html

        </div>

    - .. raw:: html

        <div class="ansible-option-indent-desc"></div><div class="ansible-option-cell">

      Trigger type.


      .. rst-class:: ansible-option-line

      :ansible-option-returned-bold:`Returned:` Always.


      .. raw:: html

        </div>




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

