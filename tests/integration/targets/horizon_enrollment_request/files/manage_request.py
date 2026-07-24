#!/usr/bin/env python

"""Validate and resolve a pending WebRA enrollment request with the Horizon SDK."""

from __future__ import annotations

import os
import sys

import horizon


def unwrap(response):
    while getattr(response, "actual_instance", None) is not None:
        response = response.actual_instance
    return response


def field(response, name):
    response = unwrap(response)
    if isinstance(response, dict):
        value = response.get(name)
    else:
        value = getattr(response, "id" if name == "_id" else name)
    return getattr(value, "value", value)


def editable_template(response_template):
    source = (
        response_template
        if isinstance(response_template, dict)
        else response_template.to_dict()
    )
    template = {}
    for name in ("subject", "sans", "extensions", "labels", "metadata"):
        values = [
            value
            for value in source.get(name) or []
            if value.get("editable") is True
        ]
        if values:
            template[name] = values
    return template


def subject_value(response_template, element):
    source = (
        response_template
        if isinstance(response_template, dict)
        else response_template.to_dict()
    )
    for subject_element in source.get("subject") or []:
        if subject_element.get("element") == element:
            return subject_element.get("value")
    return None


def main():
    if len(sys.argv) != 5 or sys.argv[1] not in ("approve", "deny"):
        raise SystemExit(
            "Usage: manage_request.py {approve|deny} REQUEST_ID EXPECTED_CN EXPECTED_COMMENT"
        )

    action, request_id, expected_cn, expected_comment = sys.argv[1:]
    configuration = horizon.Configuration(host=os.environ["HORIZON_ENDPOINT"])
    configuration.api_key["apiId"] = os.environ["HORIZON_API_ID"]
    configuration.api_key["apiKey"] = os.environ["HORIZON_API_KEY"]
    configuration.debug = False

    with horizon.ApiClient(configuration) as client:
        request_api = horizon.RequestApi(client)
        pending = request_api.request_get(request_id)
        expected = {
            "_id": request_id,
            "module": "webra",
            "workflow": "enroll",
            "status": "pending",
            "profile": "Ansible",
            "requester_comment": expected_comment,
        }
        observed = {name: field(pending, name) for name in expected}
        if observed != expected:
            raise SystemExit(
                "Unexpected enrollment request before approval: %r" % observed
            )

        response_template = field(pending, "template")
        if response_template is None:
            raise SystemExit("The pending enrollment request has no template")
        observed_cn = subject_value(response_template, "cn.1")
        if observed_cn != expected_cn:
            raise SystemExit(
                "Unexpected enrollment request CN: %r (expected %r)"
                % (observed_cn, expected_cn)
            )

        if action == "approve":
            approval = horizon.WebRAEnrollRequestOnApprove(
                _id=request_id,
                module="webra",
                workflow="enroll",
                template=editable_template(response_template),
                approverComment="Approved by the Ansible integration test",
            )
            request_api.request_approve(horizon.RequestApproveRequest(approval))
        else:
            denial = horizon.RequestDenyRequest(
                _id=request_id,
                module="webra",
                workflow="enroll",
                approverComment="Denied by the Ansible integration test",
            )
            request_api.request_deny(denial)


if __name__ == "__main__":
    main()
