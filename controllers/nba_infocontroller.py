"""Controlador de endpoints NBA.

Define rutas HTTP que exponen equipos y jugadores de NBA.
"""

from fastapi import APIRouter, HTTPException
import httpx
from clients.nba_infoclient import NBABallDontLieClient
from DTOs.nba_infoDTO import PlayersResponseDTO, PlayerDTO, TeamDTO


# Router para agrupar endpoints de NBA
router = APIRouter(prefix="/nba", tags=["nba"])

# Cliente que se comunica con la API externa
client = NBABallDontLieClient()


@router.get("/teams", response_model=list[TeamDTO])
async def get_all_teams(page: int = 1, per_page: int = 25):
    """Lista equipos NBA usando paginación por cursor.

    Args:
        page: número de página solicitada (>=1).
        per_page: cantidad de elementos por página (>=1).
    """
    # Validación simple de parámetros
    if page < 1 or per_page < 1:
        raise HTTPException(
            status_code=400,
            detail="page y per_page deben ser mayores a 0",
        )

    async with httpx.AsyncClient() as http_client:
        # Cursor para paginación de la API externa
        cursor = None
        # Avanzar hasta la página solicitada (cada vuelta hace 1 request)
        for _ in range(page - 1):
            data = await client.get_allteams(http_client=http_client, cursor=cursor, per_page=per_page)
            cursor = data.get("meta", {}).get("next_cursor")
            if not cursor:
                return {"detail": "No hay más páginas disponibles"}
        # Obtener la página solicitada
        data = await client.get_allteams(http_client=http_client, cursor=cursor, per_page=per_page)
        return data.get("data", [])


@router.get("/teams/{team_id}", response_model=TeamDTO)
async def get_team(team_id: int):
    """Obtiene un equipo NBA por ID."""
    # Obtener un solo equipo por ID
    async with httpx.AsyncClient() as http_client:
        data = await client.get_team(team_id, http_client)
        return data.get("data")


@router.get("/players", response_model=PlayersResponseDTO)
async def get_all_players(page: int = 1, per_page: int = 25):
    """Lista jugadores NBA usando paginación por cursor.

    Args:
        page: número de página solicitada (>=1).
        per_page: cantidad de elementos por página (>=1).
    """
    # Validación simple de parámetros
    if page < 1 or per_page < 1:
        raise HTTPException(
            status_code=400,
            detail="page y per_page deben ser mayores a 0",
        )

    async with httpx.AsyncClient() as http_client:
        # Cursor para paginación de la API externa
        cursor = None
        # Avanzar hasta la página solicitada (cada vuelta hace 1 request)
        for _ in range(page - 1):
            data = await client.get_allplayers(http_client=http_client, cursor=cursor, per_page=per_page)
            cursor = data.get("meta", {}).get("next_cursor")
            if not cursor:
                return {"detail": "No hay más páginas disponibles"}
        # Obtener la página solicitada
        players = await client.get_allplayers(http_client=http_client, cursor=cursor, per_page=per_page)
        return players


@router.get("/players/{player_id}", response_model=PlayerDTO)
async def get_player(player_id: int):
    """Obtiene un jugador NBA por ID."""
    # Obtener un solo jugador por ID
    async with httpx.AsyncClient() as http_client:
        data = await client.get_player(player_id, http_client)
        return data.get("data")
