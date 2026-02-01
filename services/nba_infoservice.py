"""Servicio de negocio para NBA.

Contiene reglas básicas y transforma los datos de la API externa en DTOs.
"""

import httpx
from typing import List
from fastapi import HTTPException
from clients.nba_infoclient import NBABallDontLieClient
from DTOs.nba_infoDTO import TeamDTO, PlayerDTO, PlayersResponseDTO



class NBAInfoService:
    """
    Servicio de lógica de negocio para la API de la NBA.
    """

    def __init__(self):
        """Inicializa el servicio y el cliente externo."""
        try:
            # Inicializa el cliente que consume la API externa
            self.client = NBABallDontLieClient()
        except HTTPException:
            # Re-lanzar excepciones HTTP del cliente
            raise
        except Exception as e:
            # Si faltan variables de entorno, lanza un error claro
            raise HTTPException(
                status_code=500,
                detail=f"Error al inicializar el servicio NBA: {str(e)}",
            )

    async def get_all_teams(self) -> List[TeamDTO]:
        """Obtiene equipos de NBA (primera página de la API externa)."""
        async with httpx.AsyncClient() as http_client:
            # Llama a la API externa
            data = await self.client.get_allteams(http_client)
            teams = data.get("data", [])
            # Convierte cada elemento a DTO
            return [TeamDTO(**team) for team in teams]

    async def get_team(self, team_id: int) -> TeamDTO:
        """Obtiene un equipo NBA por ID."""
        if team_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="team_id debe ser mayor a 0",
            )
        async with httpx.AsyncClient() as http_client:
            data = await self.client.get_team(team_id, http_client)
            return TeamDTO(**data.get("data"))

    async def get_all_players(self, page: int = 1, per_page: int = 25) -> PlayersResponseDTO:
        """Obtiene jugadores de NBA (primera página de la API externa)."""
        if page < 1 or per_page < 1:
            raise HTTPException(
                status_code=400,
                detail="page y per_page deben ser mayores a 0",
            )
        async with httpx.AsyncClient() as http_client:
            # La API externa usa cursor, por eso enviamos cursor=None
            data = await self.client.get_allplayers(http_client=http_client, cursor=None, per_page=per_page)
            return PlayersResponseDTO(**data)

    async def get_player(self, player_id: int) -> PlayerDTO:
        """Obtiene un jugador NBA por ID."""
        if player_id <= 0:
            raise HTTPException(
                status_code=400,
                detail="player_id debe ser mayor a 0",
            )
        async with httpx.AsyncClient() as http_client:
            data = await self.client.get_player(player_id, http_client)
            return PlayerDTO(**data.get("data"))
