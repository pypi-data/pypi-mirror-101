from abc import ABC, abstractmethod
from collections import UserDict

import xmltodict


class SATParser(ABC):
    @abstractmethod
    def parse(self, response: str) -> UserDict:
        """Parse an event from a source in XML representation."""


class VerifyParser(SATParser):
    @classmethod
    def parse(cls, response: str) -> UserDict:
        """Gets the Query ID from the raw response"""
        response_dict = xmltodict.parse(response)
        result = response_dict["Envelope"]["Body"]["VerificaSolicitudDescargaResponse"][
            "VerificaSolicitudDescargaResult"
        ]
        data = {
            "EstadoSolicitud": result["@EstadoSolicitud"],
            "CodEstatus": result["@CodEstatus"],
            "Mensaje": result["@Mensaje"],
            "CodigoEstadoSolicitud": result["@CodigoEstadoSolicitud"],
            "NumeroCFDIs": result["@NumeroCFDIs"],
            "IdsPaquetes": [result["IdsPaquetes"]]
            if result["@EstadoSolicitud"] == "3"
            else "",  # TODO Check what happens when multiple ids
        }
        return data


class QueryParser(SATParser):
    @classmethod
    def parse(cls, response: str) -> UserDict:
        """Gets the Query ID from the raw response"""
        response_dict = xmltodict.parse(response)
        result = response_dict["Envelope"]["Body"]["SolicitaDescargaResponse"][
            "SolicitaDescargaResult"
        ]
        data = {
            "CodEstatus": result["@CodEstatus"],
            "IdSolicitud": result.get("@IdSolicitud"),
        }
        return data


class DownloadParser(SATParser):
    @classmethod
    def parse(cls, response: str) -> UserDict:
        """Gets the Download data from the raw response"""
        response_dict = xmltodict.parse(response)
        package = response_dict["Envelope"]["Body"]["RespuestaDescargaMasivaTercerosSalida"][
            "Paquete"
        ]
        data = {
            "Content": package,
        }
        return data


class LoginParser(SATParser):
    @classmethod
    def parse(cls, response: str) -> UserDict:
        """Gets the token from the raw response"""
        response_dict = xmltodict.parse(response)
        data = {
            "token": response_dict["Envelope"]["Body"]["AutenticaResponse"]["AutenticaResult"],
        }
        return data
