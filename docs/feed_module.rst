.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.evertrust.horizon.feed_module:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

evertrust.horizon.feed -- Evertrust horizon feed plugin
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `evertrust.horizon collection <https://galaxy.ansible.com/evertrust/horizon>`_ (version 0.1.1).

    To install it use: :code:`ansible-galaxy collection install evertrust.horizon`.

    To use it in a playbook, specify: :code:`evertrust.horizon.feed`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Feed a certificate to Horizon.

.. note::
    This module has a corresponding :ref:`action plugin <action_plugins>`.

.. Aliases


.. Requirements


.. Options

Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                        <th width="100%">Comments</th>
        </tr>
                    <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-ca_bundle"></div>
                    <b>ca_bundle</b>
                    <a class="ansibleOptionLink" href="#parameter-ca_bundle" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>The location of a CA Bundle to use when validating SSL certificates.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-campaign"></div>
                    <b>campaign</b>
                    <a class="ansibleOptionLink" href="#parameter-campaign" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Name of the discovery campaign.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-certificate"></div>
                    <b>certificate</b>
                    <a class="ansibleOptionLink" href="#parameter-certificate" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>A certificate pem, or the path to the certificate pem file.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-client_cert"></div>
                    <b>client_cert</b>
                    <a class="ansibleOptionLink" href="#parameter-client_cert" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>The location of a client side certificate.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-client_key"></div>
                    <b>client_key</b>
                    <a class="ansibleOptionLink" href="#parameter-client_key" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>The location of a client side certificate&#x27;s key.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
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
                                            <div>url of the API</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-hostnames"></div>
                    <b>hostnames</b>
                    <a class="ansibleOptionLink" href="#parameter-hostnames" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>                                            </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Hostname of the discovered host.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-ip"></div>
                    <b>ip</b>
                    <a class="ansibleOptionLink" href="#parameter-ip" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>IP adress</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-operating_systems"></div>
                    <b>operating_systems</b>
                    <a class="ansibleOptionLink" href="#parameter-operating_systems" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=string</span>                                            </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Operating system of the discovered host.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-paths"></div>
                    <b>paths</b>
                    <a class="ansibleOptionLink" href="#parameter-paths" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Path where the certificate was discovered.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-usages"></div>
                    <b>usages</b>
                    <a class="ansibleOptionLink" href="#parameter-usages" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                                <td>
                                            <div>Free field usally used to indicate configuration files making use of the certificate.</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
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
                                            <div>Horizon identifiant</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
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

    
    - name: test discovery
        evertrust.horizon.feed:
          x_api_id: "myId"
          x_api_key: "myKey"
          endpoint: "https://url-of-the-api"
          campaign: campaign1
          ip: localhost
          certificate: <certificate_in_pem>

    - name: test discovery
        evertrust.horizon.feed:
          x_api_id: "myId"
          x_api_key: "myKey"
          endpoint: "https://url-of-the-api"
          campaign: campaign1
          ip: localhost
          certificate:
            src: pem/file/path




.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors



.. Parsing errors

