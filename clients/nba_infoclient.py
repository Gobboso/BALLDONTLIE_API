"""Cliente HTTP para consumir la API BallDontLie de NBA.

Este módulo contiene una clase que centraliza las llamadas a la API externa
y maneja la autenticación y el armado de parámetros.
"""

import httpx
from fastapi import HTTPException
from appsettings import Settings



class NBABallDontLieClient:
    """Cliente de acceso a BallDontLie (NBA)."""

    def __init__(self):
        """Inicializa el cliente con la API key y la URL base."""
        # Verifica que las variables de entorno estén configuradas
        if not Settings.BALLDONTLIE_API_KEY or not Settings.NBA_BALLDONTLIE_API_URL:
            raise HTTPException(
                status_code=500,
                detail="Error de configuración: Debes proporcionar la API key y la URL en el archivo .env",
            )
        # Guarda la API key y la URL base
        self.api_key = Settings.BALLDONTLIE_API_KEY
        self.api_url = Settings.NBA_BALLDONTLIE_API_URL.rstrip("/")
        # Header de autorización requerido por la API
        self.headers = {"Authorization": self.api_key}

    async def get_allteams(self, http_client: httpx.AsyncClient, cursor: int | None = None, per_page: int = 25):
        """Obtiene una página de equipos de NBA."""
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
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error de la API BallDontLie: {exc.response.text}",
            )

    async def get_allplayers(self, http_client: httpx.AsyncClient, cursor: int | None = None, per_page: int = 25):
        """Obtiene una página de jugadores de NBA."""
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
            raise HTTPException(
                status_code=exc.response.status_code,
                detail=f"Error de la API BallDontLie: {exc.response.text}",
            )