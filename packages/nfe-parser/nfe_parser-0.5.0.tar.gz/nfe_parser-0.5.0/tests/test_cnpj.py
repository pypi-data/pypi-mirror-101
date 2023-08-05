#!/usr/bin/env python

"""Tests for `nfe.Cnpj` class."""

import pytest

from nfe_parser import nfe


@pytest.fixture(
    params=[
        "75.315.333/0121-15",
        "75315.333/0121-15",
        "75.315333/0121-15",
        "75.315.3330121-15",
        "75.315.333/012115",
        "75315333012115",
        " 75..315.333///0121-15",
    ]
)
def cnpj_valid(request):
    return request.param


def test_create_cnpj_valid(cnpj_valid):
    """Creates a valid CNPJ"""
    cnpj = nfe.Cnpj(value=cnpj_valid)
    assert cnpj.value == "75.315.333/0121-15", "CNPJ does not match"  # nosec


@pytest.fixture(
    params=[
        "75.315.333/0121",
        "75.315.333/0121-1",
        "",
        "non-decimal-chars",
        "75.315.333/0121-15-16",
    ]
)
def cnpj_wrong_size(request):
    return request.param


def test_create_cnpj_wrong_size(cnpj_wrong_size):
    """Attempts to create a CNPJ with wrong size, an exception is expected to
    be raised"""
    try:
        nfe.Cnpj(value=cnpj_wrong_size)
        # an exception should be raised before the assert is reached
        assert (  # nosec
            False
        ), "False negative: allowed creation of wrong sized CNPJ"
    except ValueError:
        pass


@pytest.fixture(
    params=["75.315.333/0121-19", "65.315.333/0121-19"]
)  # missing last two digits
def cnpj_invalid(request):
    return request.param


def test_create_cnpj_invalid(cnpj_invalid):
    """Attempts to create an invalid CNPJ, an exception is expected to be
    raised"""
    try:
        nfe.Cnpj(value=cnpj_invalid)
        # an exception should be raised before the assert is reached
        assert False  # nosec
    except ValueError:
        pass
