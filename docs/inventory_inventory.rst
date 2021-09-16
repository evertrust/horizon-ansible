.. Document meta

:orphan:

.. Anchors

.. _ansible_collections.evertrust.horizon.inventory_inventory:

.. Anchors: short name for ansible.builtin

.. Anchors: aliases



.. Title

evertrust.horizon.inventory -- Evertrust horizon inventory plugin
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

.. Collection note

.. note::
    This plugin is part of the `evertrust.horizon collection <https://galaxy.ansible.com/evertrust/horizon>`_ (version 0.1.1).

    To install it use: :code:`ansible-galaxy collection install evertrust.horizon`.

    To use it in a playbook, specify: :code:`evertrust.horizon.inventory`.

.. version_added


.. contents::
   :local:
   :depth: 1

.. Deprecated


Synopsis
--------

.. Description

- Get inventory hosts from Evertrust Horizon.
- Use a YAML configuration file that ends with ``horizon_inventory.(yml|yaml``).


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
                            <th>Configuration</th>
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
                                                                                            </td>
                                                <td>
                                            <div>The location of a CA Bundle to use when validating SSL certificates.</div>
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
                                                                                            </td>
                                                <td>
                                            <div>url of the API</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-fields"></div>
                    <b>fields</b>
                    <a class="ansibleOptionLink" href="#parameter-fields" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>a list of fields search</div>
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
                                                                                                                                                                    <b>Default:</b><br/><div style="color: blue">[]</div>
                                    </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>A list in order of precedence for hostname variables.</div>
                                            <div>To use labels as hostnames use the syntax labels.&lt;key&gt;</div>
                                                        </td>
            </tr>
                                <tr>
                                                                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-query"></div>
                    <b>query</b>
                    <a class="ansibleOptionLink" href="#parameter-query" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                                                 / <span style="color: red">required</span>                    </div>
                                                        </td>
                                <td>
                                                                                                                                                            </td>
                                                    <td>
                                                                                            </td>
                                                <td>
                                            <div>query to define a request</div>
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



.. Facts


.. Return values


..  Status (Presently only deprecated)


.. Authors



.. Parsing errors

