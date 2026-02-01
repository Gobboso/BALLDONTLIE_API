"""Configuración central de la aplicación.

Carga variables de entorno desde un archivo .env.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Contenedor de variables de entorno usadas por la app."""
    BALLDONTLIE_API_KEY: str | None = os.getenv("API_KEY")
    CS2_BALLDONTLIE_API_URL: str | None = os.getenv("CS2_BALLDONTLIE_API_URL")
    NBA_BALLDONTLIE_API_URL: str | None = os.getenv("NBA_BALLDONTLIE_API_URL")