#!/usr/bin/env python

"""Tests for `nfe.AuthProtocol` class."""

import pytest

from nfe_parser import nfe


@pytest.fixture(
    params=[
        "123456789012345",
        "1234 5678 9012 345",
        "123-456-789-012-345",
        "\n 123456789012345   stuff\n",
    ]
)
def auth_protocol_valid(request):
    return request.param


def test_create_authprotocol_valid(auth_protocol_valid):
    """Creates a valid authorization protocol"""
    auth_protocol = nfe.AuthProtocol(value=auth_protocol_valid)
    assert (  # nosec
        auth_protocol.value == "123456789012345"
    ), "Authorization Protocol does not match"


@pytest.fixture(
    params=["123456789012345678", "1234 5678", "", "non-decimal-chars"]
)
def authprotocol_wrong_size(request):
    return request.param


def test_create_cnpj_wrong_size(authprotocol_wrong_size):
    """Attempts to create an authorization protocol with wrong size, an
    exception is expected to be raised"""
    try:
        nfe.AuthProtocol(value=authprotocol_wrong_size)
        # an exception should be raised before the assert is reached
        assert False, (  # nosec
            "False negative: allowed creation of wrong sized authorization "
            "protocol"
        )
    except ValueError:
        pass
