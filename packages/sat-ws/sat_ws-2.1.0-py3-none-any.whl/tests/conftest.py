# pylint: disable=redefined-outer-name
import random
from datetime import datetime, timedelta
from importlib import resources

import pytest

import sat.enums
from sat.certificate_handler import CertificateHandler
from sat.sat_connector import SATConnector
from sat.sat_login_handler import SATLoginHandler

from . import fake_fiel

cert = resources.read_binary(fake_fiel, "EKU9003173C9.cer")
key = resources.read_binary(fake_fiel, "EKU9003173C9.key")
password = resources.read_text(fake_fiel, "EKU9003173C9.txt").encode("utf-8")


@pytest.fixture
def certificate_handler():
    new_certificate_handler = CertificateHandler(cert, key, password)
    return new_certificate_handler


@pytest.fixture
def login_handler(certificate_handler):
    _login_handler = SATLoginHandler(certificate_handler)
    return _login_handler


@pytest.fixture
def sat_connector():
    sat_obj = SATConnector(cert, key, password)
    return sat_obj


query_scenarios = [  # TODO make flexible
    (sat.enums.DownloadType.ISSUED, sat.enums.RequestType.CFDI),
    (sat.enums.DownloadType.RECEIVED, sat.enums.RequestType.CFDI),
    (sat.enums.DownloadType.ISSUED, sat.enums.RequestType.METADATA),
    (sat.enums.DownloadType.RECEIVED, sat.enums.RequestType.METADATA),
]


@pytest.fixture(params=query_scenarios)
def query(sat_connector, request):
    start = datetime.fromisoformat("2021-01-01T00:00:00")
    end = datetime.fromisoformat("2021-03-01T00:00:00") + timedelta(
        seconds=random.randint(1, 10000)
    )
    query = sat_connector.query(
        start=start,
        end=end,
        download_type=request.param[0],
        request_type=request.param[1],
    )
    return query


@pytest.fixture
def package_ids(sat_connector, query):
    package_ids = sat_connector.wait_query(query["IdSolicitud"])
    return package_ids
