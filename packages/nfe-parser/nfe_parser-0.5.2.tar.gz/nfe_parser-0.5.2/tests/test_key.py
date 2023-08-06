#!/usr/bin/env python

"""Tests for `nfe.Key` class."""

import pytest

from nfe_parser import nfe


@pytest.fixture(
    params=[
        "1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 1234",
        "12345678901234567890123456789012345678901234",
        "1234-5678-9012-3456-7890-1234-5678-9012-3456-7890-1234",
        "\n 12345678 9012 3456 7890 1234 5678 9012 3456 7890 1234   asd\n",
    ]
)
def key_valid(request):
    return request.param


def test_create_key_valid(key_valid):
    """Creates a valid access key"""
    key = nfe.Key(value=key_valid)
    assert (  # nosec
        key.value == "1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 1234"
    ), "Access Key does not match"


@pytest.fixture(
    params=[
        "1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 1234 5678",
        "1234 5678",
        "",
        "non-decimal-chars",
    ]
)
def key_wrong_size(request):
    return request.param


def test_create_cnpj_wrong_size(key_wrong_size):
    """Attempts to create an access key with wrong size, an exception is
    expected to be raised"""
    try:
        nfe.Key(value=key_wrong_size)
        # an exception should be raised before the assert is reached
        assert (  # nosec
            False
        ), "False negative: allowed creation of wrong sized access key"
    except ValueError:
        pass
