.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.evertrust.horizon.horizon_enroll_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

evertrust.horizon.horizon_enroll -- Horizon enrollment plugin
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `evertrust.horizon collection <https://galaxy.ansible.com/evertrust/horizon>`_ (version 1.0.0).

    To install it use: :code:`ansible-galaxy collection install evertrust.horizon`.

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

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
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
                                            <div>Path of a CA bundle used to validate the Horizon instance SSL certificate.</div>
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
                                            <div>Path of a client certificate.</div>
                                            <div>Required if you use certificate based authentication</div>
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
                                            <div>Path of a client certificate&#x27;s key.</div>
                                            <div>Required if you use certificate based authentication</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-csr"></div>
                    <b>csr</b>
                    <a class="ansibleOptionLink" href="#parameter-csr" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>A certificate signing request, or the path to the CSR file.</div>
                                            <div>If none is provided, one will be generated on-the-fly.</div>
                                                        </td>
            </tr>
                                        <tr>
                                                    <td class="elbow-placeholder"></td>
                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-csr/src"></div>
                    <b>src</b>
                    <a class="ansibleOptionLink" href="#parameter-csr/src" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>The path to a CSR file</div>
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
                                            <div>Your Horizon instance base endpoint.</div>
                                            <div>It must include the protocol (https://) and no trailing slash nor path.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-key_type"></div>
                    <b>key_type</b>
                    <a class="ansibleOptionLink" href="#parameter-key_type" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>rsa-256</li>
                                                                                                                                                                                                <li>rsa-512</li>
                                                                                                                                                                                                <li>rsa-1024</li>
                                                                                                                                                                                                <li>rsa-2048</li>
                                                                                                                                                                                                <li>rsa-3072</li>
                                                                                                                                                                                                <li>rsa-4096</li>
                                                                                                                                                                                                <li>rsa-8192</li>
                                                                                                                                                                                                <li>ec-secp256r1</li>
                                                                                                                                                                                                <li>ec-secp384r1</li>
                                                                                                                                                                                                <li>ec-secp521r1</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                            <div>Key type.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-labels"></div>
                    <b>labels</b>
                    <a class="ansibleOptionLink" href="#parameter-labels" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Certificate&#x27;s labels.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-mode"></div>
                    <b>mode</b>
                    <a class="ansibleOptionLink" href="#parameter-mode" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                            <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                                                                                                                                                <li>centralized</li>
                                                                                                                                                                                                <li>decentralized</li>
                                                                                    </ul>
                                                                            </td>
                                                                <td>
                                            <div>Enrollment mode.</div>
                                            <div>If empty, will be inferred from the Horizon certificate profile configuration.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-password"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-password" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Security password for the certificate.</div>
                                            <div>Password policies will be applied to check validity.</div>
                                            <div>Required only if the enrollement is centralized and the password generation mode is not random.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-profile"></div>
                    <b>profile</b>
                    <a class="ansibleOptionLink" href="#parameter-profile" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Name of the profile that will be used to enroll the certificate.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-sans"></div>
                    <b>sans</b>
                    <a class="ansibleOptionLink" href="#parameter-sans" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Certificate&#x27;s subject alternative names (SANs) of the certificate.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-subject"></div>
                    <b>subject</b>
                    <a class="ansibleOptionLink" href="#parameter-subject" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Certificate&#x27;s subject.</div>
                                            <div>You can either give the description of the subject, or the full DN.</div>
                                            <div>If you give the dn, other values won&#x27;t be used.</div>
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
                                            <div>Horizon identifier</div>
                                            <div>Required if you use credentials authentication</div>
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
                                            <div>Horizon password</div>
                                            <div>Required if you use credentials authentication</div>
                                                        </td>
            </tr>
                        </table>
    <br/>

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

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
                    <tr>
                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-certificate"></div>
                    <b>certificate</b>
                    <a class="ansibleOptionLink" href="#return-certificate" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Enrolled certificate object</div>
                                        <br/>
                                    </td>
            </tr>
                                        <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/_id"></div>
                    <b>_id</b>
                    <a class="ansibleOptionLink" href="#return-certificate/_id" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Horizon internal certificate ID.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/certificate"></div>
                    <b>certificate</b>
                    <a class="ansibleOptionLink" href="#return-certificate/certificate" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate in PEM format.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/dn"></div>
                    <b>dn</b>
                    <a class="ansibleOptionLink" href="#return-certificate/dn" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate DN.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/holderId"></div>
                    <b>holderId</b>
                    <a class="ansibleOptionLink" href="#return-certificate/holderId" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate holder ID.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/issuer"></div>
                    <b>issuer</b>
                    <a class="ansibleOptionLink" href="#return-certificate/issuer" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate issuer DN.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/keyType"></div>
                    <b>keyType</b>
                    <a class="ansibleOptionLink" href="#return-certificate/keyType" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate key type.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/labels"></div>
                    <b>labels</b>
                    <a class="ansibleOptionLink" href="#return-certificate/labels" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=dictionary</span>                    </div>
                                    </td>
                <td>If present</td>
                <td>
                                            <div>Certificate labels.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/metadata"></div>
                    <b>metadata</b>
                    <a class="ansibleOptionLink" href="#return-certificate/metadata" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=dictionary</span>                    </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate metadata.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/module"></div>
                    <b>module</b>
                    <a class="ansibleOptionLink" href="#return-certificate/module" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate module.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/notAfter"></div>
                    <b>notAfter</b>
                    <a class="ansibleOptionLink" href="#return-certificate/notAfter" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">integer</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate expiration date (UNIX timestamp in millis).</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/notBefore"></div>
                    <b>notBefore</b>
                    <a class="ansibleOptionLink" href="#return-certificate/notBefore" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">integer</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate issuance date (UNIX timestamp in millis).</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/owner"></div>
                    <b>owner</b>
                    <a class="ansibleOptionLink" href="#return-certificate/owner" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate owner.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/profile"></div>
                    <b>profile</b>
                    <a class="ansibleOptionLink" href="#return-certificate/profile" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate profile.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/serial"></div>
                    <b>serial</b>
                    <a class="ansibleOptionLink" href="#return-certificate/serial" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate serial number (hexadecimal format).</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/signingAlgorithm"></div>
                    <b>signingAlgorithm</b>
                    <a class="ansibleOptionLink" href="#return-certificate/signingAlgorithm" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate signing algorithm.</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                    <td class="elbow-placeholder">&nbsp;</td>
                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-certificate/subjectAlternateNames"></div>
                    <b>subjectAlternateNames</b>
                    <a class="ansibleOptionLink" href="#return-certificate/subjectAlternateNames" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                       / <span style="color: purple">elements=dictionary</span>                    </div>
                                    </td>
                <td>If present</td>
                <td>
                                            <div>Certificate subject alternate names (SAN).</div>
                                        <br/>
                                    </td>
            </tr>
                    
                                <tr>
                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-chain"></div>
                    <b>chain</b>
                    <a class="ansibleOptionLink" href="#return-chain" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>Always</td>
                <td>
                                            <div>Certificate&#x27;s trust chain</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-key"></div>
                    <b>key</b>
                    <a class="ansibleOptionLink" href="#return-key" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>If enrollement mode is &quot;centralized&quot; or if a key pair was generated on-the-fly</td>
                <td>
                                            <div>Certificate&#x27;s private key</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-p12"></div>
                    <b>p12</b>
                    <a class="ansibleOptionLink" href="#return-p12" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>If enrollement mode is &quot;centralized&quot; or if a key pair was generated on-the-fly</td>
                <td>
                                            <div>Base64-encoded PKCS#12</div>
                                        <br/>
                                    </td>
            </tr>
                                <tr>
                                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-p12_password"></div>
                    <b>p12_password</b>
                    <a class="ansibleOptionLink" href="#return-p12_password" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                                          </div>
                                    </td>
                <td>If enrollement mode is &quot;centralized&quot; or if a key pair was generated on-the-fly</td>
                <td>
                                            <div>PKCS#12 password</div>
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

