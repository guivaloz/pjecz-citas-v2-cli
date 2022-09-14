"""
CLI Materias Request API
"""
from typing import Any

import requests

from common.exceptions import CLIStatusCodeError, CLIConnectionError, CLIResponseError
from config.settings import API_KEY, BASE_URL, LIMIT, TIMEOUT


def get_materias(
    limit: int = LIMIT,
    offset: int = 0,
) -> Any:
    """Solicitar materias"""
    parametros = {"limit": limit}
    if offset > 0:
        parametros["offset"] = offset
    try:
        respuesta = requests.get(
            f"{BASE_URL}/materias",
            headers={"X-Api-Key": API_KEY},
            params=parametros,
            timeout=TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        raise CLIStatusCodeError("No hubo respuesta al solicitar materias") from error
    except requests.exceptions.HTTPError as error:
        raise CLIStatusCodeError("Error Status Code al solicitar materias: " + str(error)) from error
    except requests.exceptions.RequestException as error:
        raise CLIConnectionError("Error inesperado al solicitar materias") from error
    datos = respuesta.json()
    if "success" not in datos or datos["success"] is False or "result" not in datos:
        if "message" in datos:
            raise CLIResponseError("Error al solicitar materias: " + datos["message"])
        raise CLIResponseError("Error al solicitar materias")
    return datos["result"]
