#!/usr/bin/env python

"""Tests for `nfe.Nfe` class."""

# import pytest
from datetime import datetime

import pytz

from nfe_parser import nfe


def test_create_nfe_valid():
    nfe.Nfe(
        company=nfe.Company(
            name="ACME Co.",
            state_reg="123",
            cnpj=nfe.Cnpj(value="75.315.333/0121-15"),
            addr="Dummy St.",
        ),
        source="http://...",
        products=[
            nfe.Product(
                code="123",
                description="banana",
                qty="2.0",
                unit="UN",
                value="4.5",
                total="9.0",
            ),
            nfe.Product(
                code="124",
                description="maçã",
                qty="3.0",
                unit="UN",
                value="6.0",
                total="18.0",
            ),
        ],
        num=456,
        series=789,
        emission_date=datetime.now(tz=pytz.timezone("America/Sao_Paulo")),
        key=nfe.Key(value="43181175315333012115655130000883321048579179"),
        auth_protocol=nfe.AuthProtocol("143181369407004"),
        cpf=nfe.Cpf(value="111.222.333-44"),
        total=27.0,
        discount=0.0,
    )
