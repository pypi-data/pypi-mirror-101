import logging
import time
from datetime import datetime

from . import exceptions, utils
from .certificate_handler import CertificateHandler
from .enums import TEMPLATES
from .sat_login_handler import SATLoginHandler
from .sat_parsers import DownloadParser, QueryParser, VerifyParser

logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


class SATConnector:
    """Class to make a connection to the SAT"""

    certificate_handler: CertificateHandler
    login_handler: SATLoginHandler

    def __init__(self, cert: bytes, key: bytes, password: str) -> None:
        """Loads the certificate, key file and password to stablish the connection to the SAT

        Creates a object to manage the SAT connection.

        Args:
            cert (bytes): DER Certificate in raw binary
            key (bytes): DER Key Certificate in raw binary
            password (str): Key password in plain text (utf-8)
        """
        self.certificate_handler = CertificateHandler(cert, key, password)
        self.login_handler = SATLoginHandler(self.certificate_handler)
        _logger.info("Data correctly loaded")

    def _create_common_envelope(self, template: str, data: dict) -> str:
        _logger.debug("Creating Envelope")
        _logger.debug("%s", template)
        _logger.debug("%s", data)
        query_data, query_data_signature = utils.prepare_template(template, data)
        digest_value = utils.digest(query_data)
        signed_info = utils.prepare_template(
            TEMPLATES["SignedInfo"],
            {
                "uri": "",
                "digest_value": digest_value,
            },
        )
        key_info = utils.prepare_template(
            TEMPLATES["KeyInfo"],
            {
                "issuer_name": self.certificate_handler.certificate.issuer,
                "serial_number": self.certificate_handler.certificate.get_serial_number(),
                "certificate": self.certificate_handler.cert,
            },
        )
        signature_value = self.certificate_handler.sign(signed_info)
        signature = utils.prepare_template(
            TEMPLATES["Signature"],
            {
                "signed_info": signed_info,
                "signature_value": signature_value,
                "key_info": key_info,
            },
        )
        envelope_content = utils.prepare_template(
            query_data_signature,
            {
                "signature": signature,
            },
        )
        envelope = utils.prepare_template(
            TEMPLATES["Envelope"],
            {
                "content": envelope_content,
            },
        )
        _logger.debug("Final Envelope")
        _logger.debug("%s", envelope)
        return envelope

    def query(self, start: datetime, end: datetime, download_type: str, request_type: str) -> str:
        """Creates a Query in the SAT system"""
        request_content = self._get_query_soap_body(start, end, download_type, request_type)
        response = utils.consume(
            "http://DescargaMasivaTerceros.sat.gob.mx/ISolicitaDescargaService/SolicitaDescarga",
            "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/SolicitaDescargaService.svc",
            request_content,
            token=self.login_handler.token,
        )
        if response.status_code != 200:
            raise exceptions.RequestException(
                response.status_code, response.reason, request_content
            )
        response_clean = utils.remove_namespaces(response.content.decode("UTF-8"))
        query_id = QueryParser.parse(response_clean)
        return query_id

    def _get_query_soap_body(
        self, start: datetime, end: datetime, download_type: str, request_type: str
    ):
        """Creates the SOAP body to the query request"""
        start = start.isoformat()
        end = end.isoformat()
        data = {
            "start": start,
            "end": end,
            "rfc": self.certificate_handler.unique_identifier,
            "download_type": download_type,
            "request_type": request_type,
            "signature": "",
        }
        envelope = self._create_common_envelope(TEMPLATES["SolicitaDescarga"], data)
        return envelope

    def verify(self, query_id: str) -> dict:
        """Checks the status of a Query"""
        request_content = self._get_verify_soap_body(query_id)
        response = utils.consume(
            "http://DescargaMasivaTerceros.sat.gob.mx/IVerificaSolicitudDescargaService/VerificaSolicitudDescarga",
            "https://cfdidescargamasivasolicitud.clouda.sat.gob.mx/VerificaSolicitudDescargaService.svc",
            request_content,
            token=self.login_handler.token,
        )
        if response.status_code != 200:
            raise exceptions.RequestException(
                response.status_code, response.reason, request_content
            )
        response_clean = utils.remove_namespaces(response.content.decode("UTF-8"))
        data = VerifyParser.parse(response_clean)
        return data

    def _get_verify_soap_body(self, query_id: str) -> str:
        """Creates the SOAP body to check the query status"""
        data = {
            "rfc": self.certificate_handler.unique_identifier,
            "query_id": query_id,
            "signature": "",
        }
        envelope = self._create_common_envelope(TEMPLATES["VerificaSolicitudDescarga"], data)
        return envelope

    def download(self, package_ids: (list, str)) -> dict:
        """Checks the status of a Query"""
        if isinstance(package_ids, str):
            package_ids = [package_ids]
        downloads = {}
        for package_id in package_ids:
            request_content = self._get_download_soap_body(package_id)
            response = utils.consume(
                "http://DescargaMasivaTerceros.sat.gob.mx/IDescargaMasivaTercerosService/Descargar",
                "https://cfdidescargamasiva.clouda.sat.gob.mx/DescargaMasivaService.svc",
                request_content,
                token=self.login_handler.token,
            )
            if response.status_code != 200:
                raise exceptions.RequestException(
                    response.status_code, response.reason, request_content
                )
            response_clean = utils.remove_namespaces(response.content.decode("UTF-8"))
            downloads[package_id] = DownloadParser.parse(response_clean)
        return downloads

    def _get_download_soap_body(self, package_id: str) -> dict:
        """Creates the SOAP body to check the query status"""
        data = {
            "rfc": self.certificate_handler.unique_identifier,
            "package_id": package_id,
            "signature": "",
        }
        envelope = self._create_common_envelope(
            TEMPLATES["PeticionDescargaMasivaTercerosEntrada"], data
        )
        return envelope

    def wait_query(self, query_id: str, retries: int = 10, wait_seconds: int = 2) -> list:
        for _ in range(retries):
            verification = self.verify(query_id)
            query_state = int(verification["EstadoSolicitud"])
            if query_state > 3:
                raise exceptions.QueryException(f"EstadoSolicitud({query_state})")
            if query_state == 3:
                return verification["IdsPaquetes"]
            time.sleep(wait_seconds)
        raise TimeoutError("The query is not yet resolved")
