#!/usr/bin/env python

"""Tests for `nfe.Cpf` class."""

import pytest

from nfe_parser import nfe


@pytest.fixture(
    params=["111.222.333-44", "111 222 333 44", "\n 111.222.333-44   stuff\n"]
)
def cpf_valid(request):
    return request.param


def test_create_cpf_valid(cpf_valid):
    """Creates a valid CPF"""
    cpf = nfe.Cpf(value=cpf_valid)
    assert cpf.value == "111.222.333-44", "CPF does not match"  # nosec


@pytest.fixture(
    params=["111.222.333-44-55", "111.222", "", "non-decimal-chars"]
)
def cpf_wrong_size(request):
    return request.param


def test_create_cpf_wrong_size(cpf_wrong_size):
    """Attempts to create a CPF with wrong size, an exception is expected to "
    "be raised"""
    try:
        nfe.Cpf(value=cpf_wrong_size)
        # an exception should be raised before the assert is reached
        assert (  # nosec
            False
        ), "False negative: allowed creation of wrong sized CPF"
    except ValueError:
        pass
