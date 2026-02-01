"""Cliente HTTP para consumir la API BallDontLie de CS2.

Este módulo contiene una clase que centraliza las llamadas a la API externa
y maneja la autenticación y el armado de parámetros.
"""

import os, httpx
from fastapi import FastAPI, HTTPException
from appsettings import Settings

class CS2BallDontLieClient:
    """Cliente de acceso a BallDontLie (CS2).

    Se usa para solicitar equipos y jugadores a la API externa.
    """

    def __init__(self):
        """Inicializa el cliente con la API key y la URL base."""
        # Verifica que las variables de entorno estén configuradas
        if not Settings.BALLDONTLIE_API_KEY or not Settings.CS2_BALLDONTLIE_API_URL:
            raise HTTPException(
                status_code=500,
                detail="Error de configuración: Debes proporcionar la API key y la URL en el archivo .env",
            )
        # Guarda la API key y la URL base
        self.api_key = Settings.BALLDONTLIE_API_KEY
        self.api_url = Settings.CS2_BALLDONTLIE_API_URL.rstrip("/")
        # Header de autorización requerido por la API
        self.headers = {"Authorization": self.api_key}

    async def get_allteams(self, http_client: httpx.AsyncClient, cursor: int | None = None, per_page: int = 25):
        """Obtiene una página de equipos de CS2.

        Args:
            http_client: cliente HTTP asíncrono compartido.
            cursor: cursor de paginación; None para la primera página.
            per_page: cantidad de elementos por página.
        """
        try:
            # Construye parámetros (cursor es opcional)
            if cursor is not None:
                params = {"per_page": per_page, "cursor": cursor}
            else:
                params = {"per_page": per_page}
            # Llama a la API externa
            response = await http_client.get(
                f"{self.api_url}/teams",
                params=params,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error de la API BallDontLie: {exc.response.text}",
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail="Error de conexión: No se puede conectar con la API BallDontLie. Verifica tu conexión a internet.",
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Error de tiempo: La API BallDontLie tardó demasiado en responder.",
            )
    
    async def get_team(self, team_id: int, http_client: httpx.AsyncClient):
        """Obtiene un equipo específico por ID."""
        try:
            # Llama a la API externa para un equipo específico
            response = await http_client.get(
                f"{self.api_url}/teams/{team_id}", headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Equipo no encontrado: El equipo con ID {team_id} no existe.",
                )
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error de la API BallDontLie: {exc.response.text}",
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail="Error de conexión: No se puede conectar con la API BallDontLie."
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Error de tiempo: La API BallDontLie tardó demasiado en responder.",
            )
    
    async def get_allplayers(self, http_client: httpx.AsyncClient, cursor: int | None = None, per_page: int = 25):
        """Obtiene una página de jugadores de CS2.

        Args:
            http_client: cliente HTTP asíncrono compartido.
            cursor: cursor de paginación; None para la primera página.
            per_page: cantidad de elementos por página.
        """
        try:
            # Construye parámetros (cursor es opcional)
            if cursor is not None:
                params = {"per_page": per_page, "cursor": cursor}
            else:
                params = {"per_page": per_page}
            # Llama a la API externa
            response = await http_client.get(
                f"{self.api_url}/players",
                params=params,
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error de la API BallDontLie: {exc.response.text}",
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail="Error de conexión: No se puede conectar con la API BallDontLie."
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Error de tiempo: La API BallDontLie tardó demasiado en responder."
            )

    async def get_player(self, player_id: int, http_client: httpx.AsyncClient):
        """Obtiene un jugador específico por ID."""
        try:
            # Llama a la API externa para un jugador específico
            response = await http_client.get(
                f"{self.api_url}/players/{player_id}", headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise HTTPException(
                    status_code=404,
                    detail=f"Jugador no encontrado: El jugador con ID {player_id} no existe.",
                )
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error de la API BallDontLie: {exc.response.text}",
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail="Error de conexión: No se puede conectar con la API BallDontLie."
            )
        except httpx.TimeoutException:
            raise HTTPException(
                status_code=504,
                detail="Error de tiempo: La API BallDontLie tardó demasiado en responder."
            )