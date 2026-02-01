"""Punto de entrada principal de la aplicación FastAPI."""

from fastapi import FastAPI
from controllers.cs2_infocontroller import router as cs2_router
from controllers.nba_infocontroller import router as nba_router
import uvicorn

app = FastAPI()

# Include the CS2 router
app.include_router(cs2_router)
app.include_router(nba_router)

@app.get("/")
async def root():
    """Endpoint básico de bienvenida."""
    return {"mensaje": "Bienvenido a la API de CS2 y NBA"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)