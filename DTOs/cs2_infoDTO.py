"""DTOs para CS2.

Estos modelos definen la estructura de las respuestas de la API.
"""

from pydantic import BaseModel
from typing import List, Optional


class TeamDTO(BaseModel):
    """Representa un equipo de CS2."""
    id: int
    name: str
    slug: Optional[str] = None
    short_name: Optional[str] = None

class PlayerDTO(BaseModel):
    """Representa un jugador de CS2."""
    id: int
    nickname: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    full_name: Optional[str] = None
    team: Optional[TeamDTO] = None
    age: Optional[int] = None
    birthday: Optional[str] = None
    steam_id: Optional[str] = None
    is_active: Optional[bool] = None

class PlayersResponseDTO(BaseModel):
    """Respuesta para listas de jugadores CS2.

    data: lista de jugadores.
    meta: metadatos de paginación.
    """
    data: List[PlayerDTO]
    meta: Optional[dict]