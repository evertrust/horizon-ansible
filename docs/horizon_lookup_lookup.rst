.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.evertrust.horizon.horizon_lookup_lookup:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

evertrust.horizon.horizon_lookup -- Horizon lookup plugin
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `evertrust.horizon collection <https://galaxy.ansible.com/evertrust/horizon>`_ (version 0.1.1).

    To install it use: :code:`ansible-galaxy collection install evertrust.horizon`.

    To use it in a playbook, specify: :code:`evertrust.horizon.horizon_lookup`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Looks up the attributes of a given certificate.


.. Aliases


.. Requirements


.. Options

Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                            <th>Configuration</th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-attributes"></div>
                    <b>attributes</b>
                    <a class="ansibleOptionLink" href="#parameter-attributes" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>                                            </div>
                                                        </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>_id</li>
                                                                                                                                                                                                <li>certificate</li>
                                                                                                                                                                                                <li>discoveredTrusted</li>
                                                                                                                                                                                                <li>dn</li>
                                                                                                                                                                                                <li>holderId</li>
                                                                                                                                                                                                <li>issuer</li>
                                                                                                                                                                                                <li>keyType</li>
                                                                                                                                                                                                <li>labels</li>
                                                                                                                                                                                                <li>metadata</li>
                                                                                                                                                                                                <li>module</li>
                                                                                                                                                                                                <li>notAfter</li>
                                                                                                                                                                                                <li>notBefore</li>
                                                                                                                                                                                                <li>owner</li>
                                                                                                                                                                                                <li>profile</li>
                                                                                                                                                                                                <li>revocationDate</li>
                                                                                                                                                                                                <li>revocationReason</li>
                                                                                                                                                                                                <li>serial</li>
                                                                                                                                                                                                <li>signingAlgorithm</li>
                                                                                                                                                                                                <li>subjectAlternateNames</li>
                                                                                                                                                                                                <li>thirdPartyData</li>
                                                                                    </ul>
                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Attributes to be retrieved from Horizon.</div>
                                            <div>If omitted, all attributes will be returned.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-ca_bundle"></div>
                    <b>ca_bundle</b>
                    <a class="ansibleOptionLink" href="#parameter-ca_bundle" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Path of a CA bundle to use when validating the server&#x27;s SSL certificate.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-client_cert"></div>
                    <b>client_cert</b>
                    <a class="ansibleOptionLink" href="#parameter-client_cert" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Path of a client side certificate.</div>
                                            <div>Required if you use certificate authentication</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-client_key"></div>
                    <b>client_key</b>
                    <a class="ansibleOptionLink" href="#parameter-client_key" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Path of a client side certificate&#x27;s key.</div>
                                            <div>Required if you use certificate authentication</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-endpoint"></div>
                    <b>endpoint</b>
                    <a class="ansibleOptionLink" href="#parameter-endpoint" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Your Horizon instance base endpoint.</div>
                                            <div>It should include the protocol (https://) and no trailing path or slash.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-pem"></div>
                    <b>pem</b>
                    <a class="ansibleOptionLink" href="#parameter-pem" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>A certificate string in the PEM format, or the path to the certificate PEM file.</div>
                                                        </td>
            </tr>
                                        <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-pem/src"></div>
                    <b>src</b>
                    <a class="ansibleOptionLink" href="#parameter-pem/src" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>The path to a certificate PEM file</div>
                                                        </td>
            </tr>
                    
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-x_api_id"></div>
                    <b>x_api_id</b>
                    <a class="ansibleOptionLink" href="#parameter-x_api_id" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Horizon identifier</div>
                                            <div>Required if you use password authentication</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-x_api_key"></div>
                    <b>x_api_key</b>
                    <a class="ansibleOptionLink" href="#parameter-x_api_key" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>Horizon password</div>
                                            <div>Required if you use password authentication</div>
                                                        </td>
            </tr>
                        </table>
    <br/>

.. Notes


.. Seealso


.. Examples

Examples
--------

.. code-block:: yaml+jinja

    
    vars:
      endpoint: "https://<api-endpoint>"
      x_api_id: "<horizon-id>"
      x_api_key: "<horizon-password>"
      # Send the certificate by specifying its content (string) 
      my_pem: <a_webra_pem_file>
      # Send the certificate by specifying its file path
      pem_path:
        src: /pem/file/path
      
      # Sets a variable containing only one attribute (module)
      with_one: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, attributes='module', endpoint=horizon_endpoint) }}"

      # Sets a variable containing a list of attributes (module, _id)
      with_list: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=my_pem, attributes=['module', '_id'], endpoint=horizon_endpoint) }}"

      # Sets a variable containing every certificate attribute.
      without: "{{ lookup('evertrust.horizon.horizon_lookup', x_api_id=x_api_id, x_api_key=x_api_key, pem=pem_path, endpoint=horizon_endpoint) }}"




.. Facts


.. Return values

Return Values
-------------
Common return values are documented :ref:`here <common_return_values>`, the following are the fields unique to this lookup:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-_id"></div>
                    <b>_id</b>
                    <a class="ansibleOptionLink" href="#return-_id" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate ID.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate"></div>
                    <b>certificate</b>
                    <a class="ansibleOptionLink" href="#return-certificate" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate content.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-discoveredTrusted"></div>
                    <b>discoveredTrusted</b>
                    <a class="ansibleOptionLink" href="#return-discoveredTrusted" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=boolean</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>True if the certificate was discovered and trusted.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-dn"></div>
                    <b>dn</b>
                    <a class="ansibleOptionLink" href="#return-dn" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate DN.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-holderId"></div>
                    <b>holderId</b>
                    <a class="ansibleOptionLink" href="#return-holderId" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate holder ID.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-issuer"></div>
                    <b>issuer</b>
                    <a class="ansibleOptionLink" href="#return-issuer" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate issuer.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-keyType"></div>
                    <b>keyType</b>
                    <a class="ansibleOptionLink" href="#return-keyType" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate key type.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-labels"></div>
                    <b>labels</b>
                    <a class="ansibleOptionLink" href="#return-labels" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate labels.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-metadata"></div>
                    <b>metadata</b>
                    <a class="ansibleOptionLink" href="#return-metadata" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=dictionary</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate metadata.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-module"></div>
                    <b>module</b>
                    <a class="ansibleOptionLink" href="#return-module" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate module.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-notAfter"></div>
                    <b>notAfter</b>
                    <a class="ansibleOptionLink" href="#return-notAfter" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=integer</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate notAfter (UNIX timestamp format).</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-notBefore"></div>
                    <b>notBefore</b>
                    <a class="ansibleOptionLink" href="#return-notBefore" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=integer</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate notBefore (UNIX timestamp format).</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-owner"></div>
                    <b>owner</b>
                    <a class="ansibleOptionLink" href="#return-owner" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate owner.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-profile"></div>
                    <b>profile</b>
                    <a class="ansibleOptionLink" href="#return-profile" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-revocationDate"></div>
                    <b>revocationDate</b>
                    <a class="ansibleOptionLink" href="#return-revocationDate" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate revocation date (UNIX timestamp format).</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-revocationReason"></div>
                    <b>revocationReason</b>
                    <a class="ansibleOptionLink" href="#return-revocationReason" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate revocation reason.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-serial"></div>
                    <b>serial</b>
                    <a class="ansibleOptionLink" href="#return-serial" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate serial number.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-signingAlgorithm"></div>
                    <b>signingAlgorithm</b>
                    <a class="ansibleOptionLink" href="#return-signingAlgorithm" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate signing algorithm.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-subjectAlternateNames"></div>
                    <b>subjectAlternateNames</b>
                    <a class="ansibleOptionLink" href="#return-subjectAlternateNames" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate subject alternate names (SAN).</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-thirdPartyData"></div>
                    <b>thirdPartyData</b>
                    <a class="ansibleOptionLink" href="#return-thirdPartyData" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=string</span>                    </div>
                                    </td>
                <td>If specifically requested.</td>
                <td>
                                            <div>Certificate third-party data.</div>
                                        <br/>
                                    </td>
            </tr>
                        </table>
    <br/><br/>

..  Status (Presently only deprecated)


.. Authors

Authors
~~~~~~~

- Evertrust R&D (@EverTrust)



.. Parsing errors

