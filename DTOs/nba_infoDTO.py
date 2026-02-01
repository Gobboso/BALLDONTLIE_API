"""DTOs para NBA.

Estos modelos definen la estructura de las respuestas de la API.
"""

from pydantic import BaseModel
from typing import List, Optional



class TeamDTO(BaseModel):
    """Representa un equipo de NBA."""
    id: int
    abbreviation: Optional[str] = None
    city: Optional[str] = None
    conference: Optional[str] = None
    division: Optional[str] = None
    full_name: Optional[str] = None
    name: Optional[str] = None


class PlayerDTO(BaseModel):
    """Representa un jugador de NBA."""
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    position: Optional[str] = None
    height_feet: Optional[int] = None
    height_inches: Optional[int] = None
    weight_pounds: Optional[int] = None
    team: Optional[TeamDTO] = None


class PlayersResponseDTO(BaseModel):
    """Respuesta para listas de jugadores NBA.

    data: lista de jugadores.
    meta: metadatos de paginación.
    """
    data: List[PlayerDTO]
    meta: Optional[dict]
