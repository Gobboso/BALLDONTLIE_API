"""Servicio de negocio para CS2.

Contiene reglas básicas y transforma los datos de la API externa en DTOs.
"""

import httpx
from typing import List
from fastapi import HTTPException
from clients.cs2_infoclient import CS2BallDontLieClient
from DTOs.cs2_infoDTO import TeamDTO, PlayerDTO, PlayersResponseDTO



class CS2InfoService:
    """
    Este módulo contiene la clase CS2InfoService que implementa la lógica de
    negocio para obtener información de Counter-Strike 2.

    En una arquitectura de capas (Layered Architecture), este servicio actúa
    como intermediario entre:
    - Controladores (reciben las peticiones HTTP)
    - Clientes (se comunican con APIs externas)
    - DTOs (definen la estructura de los datos de respuesta)

    Responsabilidades de este servicio:
    1. Validar la entrada del usuario
    2. Coordinar las llamadas al cliente de CS2 API
    3. Transformar los datos crudos de la API en DTOs estructurados
    4. Manejar errores de configuración
    """

    def __init__(self):
        """Inicializa el servicio y el cliente externo."""
        try:
            # Inicializa el cliente que consume la API externa
            self.client = CS2BallDontLieClient()
        except HTTPException:
            # Re-lanzar excepciones HTTP del cliente
            raise
        except Exception as e:
            # Si faltan variables de entorno, lanza un error claro
            raise HTTPException(
                status_code=500,
                detail=f"Error al inicializar el servicio CS2: {str(e)}",
            )

    async def get_all_teams(self) -> List[TeamDTO]:
        """Obtiene todos los equipos de CS2 (primer page de la API externa)."""
        async with httpx.AsyncClient() as http_client:
            # Llama a la API externa
            data = await self.client.get_allteams(http_client)
            teams = data.get("data", [])
            # Convierte cada elemento a DTO
            return [TeamDTO(**team) for team in teams]

    async def get_team(self, team_id: int) -> TeamDTO:
        """Obtiene un equipo específico por ID"""
        if team_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="team_id debe ser mayor a 0",
            )
        async with httpx.AsyncClient() as http_client:
            data = await self.client.get_team(team_id, http_client)
            return TeamDTO(**data.get("data"))

    async def get_all_players(self, page: int = 1, per_page: int = 25) -> PlayersResponseDTO:
        """Obtiene jugadores (primer page de la API externa).

        Nota: La API externa usa cursor, no page numérico. Para páginas > 1
        se recomienda usar el controlador con cursor o cache.
        """
        if page < 1 or per_page < 1:
            raise HTTPException(
                status_code=400,
                detail="page y per_page deben ser mayores a 0",
            )
        async with httpx.AsyncClient() as http_client:
            # La API externa espera cursor, por eso enviamos cursor=None
            data = await self.client.get_allplayers(http_client=http_client, cursor=None, per_page=per_page)
            return PlayersResponseDTO(**data)

    async def get_player(self, player_id: int) -> PlayerDTO:
        """Obtiene un jugador específico por ID"""
        if player_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="player_id debe ser mayor a 0",
            )
        async with httpx.AsyncClient() as http_client:
            data = await self.client.get_player(player_id, http_client)
            return PlayerDTO(**data.get("data"))