# API de Equipos y Jugadores

API REST desarrollada con FastAPI que proporciona información sobre equipos y jugadores de **Counter-Strike 2 (CS2)** y **NBA** desde el proveedor externo **BallDontLie**.

---

## 📋 Tabla de Contenidos

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Endpoints](#endpoints)
  - [CS2](#cs2)
  - [NBA](#nba)
- [Ejemplos de Uso](#ejemplos-de-uso)
- [Gestión de Rate Limit](#gestión-de-rate-limit)
- [Arquitectura](#arquitectura)
- [Troubleshooting](#troubleshooting)

---

## ✨ Características

- ✅ **Dual API**: Consume datos de CS2 y NBA desde BallDontLie
- ✅ **Async/Await**: Operaciones asíncronas con httpx
- ✅ **Validación de Datos**: DTOs con Pydantic
- ✅ **Paginación por Cursor**: Navega grandes volúmenes de datos
- ✅ **Rate Limit Handling**: Respeta límites de 5 requests/minuto
- ✅ **Documentación Interactiva**: Swagger UI integrada
- ✅ **Arquitectura en Capas**: Separación clara de responsabilidades

---

## 🔧 Requisitos

- **Python 3.10+**
- **pip** (gestor de paquetes)
- **Virtual environment** (recomendado)
- **Variables de entorno**: API key de BallDontLie y URLs base

---

## 📦 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd "c:\Users\Gabriel\Desktop\Documentos Universidad\Diplomado\myapi"
```

### 2. Crear y activar virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

Si no existe `requirements.txt`, instala manualmente:
```bash
pip install fastapi uvicorn httpx python-dotenv pydantic
```

---

## ⚙️ Configuración

### 1. Crear archivo `.env`

En la raíz del proyecto, crea un archivo `.env`:

```env
# API Key de BallDontLie (obtén tu key en https://www.balldontlie.io/)
API_KEY=tu_api_key_aqui

# URLs base de las APIs
CS2_BALLDONTLIE_API_URL=https://api.balldontlie.io/v1/cs2
NBA_BALLDONTLIE_API_URL=https://api.balldontlie.io/v1
```

### 2. Verificar configuración

El archivo `appsettings.py` cargará automáticamente estas variables:

```python
class Settings:
    BALLDONTLIE_API_KEY: str | None = os.getenv("API_KEY")
    CS2_BALLDONTLIE_API_URL: str | None = os.getenv("CS2_BALLDONTLIE_API_URL")
    NBA_BALLDONTLIE_API_URL: str | None = os.getenv("NBA_BALLDONTLIE_API_URL")
```

---

## 📁 Estructura del Proyecto

```
myapi/
│
├── main.py                          # Punto de entrada principal
├── appsettings.py                   # Configuración y variables de entorno
├── requirements.txt                 # Dependencias del proyecto
├── .env                             # Variables de entorno (no incluir en Git)
│
├── clients/                         # Clientes HTTP para APIs externas
│   ├── cs2_infoclient.py           # Cliente para BallDontLie CS2
│   └── nba_infoclient.py           # Cliente para BallDontLie NBA
│
├── controllers/                     # Routers y endpoints HTTP
│   ├── cs2_infocontroller.py       # Endpoints de CS2
│   └── nba_infocontroller.py       # Endpoints de NBA
│
├── DTOs/                            # Data Transfer Objects (modelos de respuesta)
│   ├── cs2_infoDTO.py              # Modelos para CS2
│   └── nba_infoDTO.py              # Modelos para NBA
│
├── services/                        # Lógica de negocio
│   ├── cs2_infoservice.py          # Servicio de CS2
│   └── nba_infoservice.py          # Servicio de NBA
│
└── __pycache__/                     # Caché de Python (ignorar)
```

### Descripción de Capas

| Capa | Archivo | Responsabilidad |
|------|---------|-----------------|
| **Entrada** | `main.py` | Crea app FastAPI, registra routers |
| **Routing** | `controllers/` | Define rutas HTTP, parámetros, validación |
| **Lógica** | `services/` | Reglas de negocio, transformaciones |
| **Integración** | `clients/` | Consume API externa, maneja autenticación |
| **Modelos** | `DTOs/` | Define estructura de datos |
| **Config** | `appsettings.py` | Variables de entorno |

---

## 🔌 Endpoints

### CS2

**Prefijo Base:** `/cs2`

#### 1. Listar Equipos

```
GET /cs2/teams?page=1&per_page=100
```

**Parámetros:**
- `page` (int, default=1): Número de página
- `per_page` (int, default=100): Elementos por página

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "name": "Natus Vincere",
    "slug": "natus-vincere",
    "short_name": "Na'Vi"
  },
  {
    "id": 2,
    "name": "FaZe Clan",
    "slug": "faze-clan",
    "short_name": "FaZe"
  }
]
```

#### 2. Obtener Equipo por ID

```
GET /cs2/teams/{team_id}
```

**Ejemplo:** `GET /cs2/teams/1`

**Respuesta (200):**
```json
{
  "id": 1,
  "name": "Natus Vincere",
  "slug": "natus-vincere",
  "short_name": "Na'Vi"
}
```

#### 3. Listar Jugadores

```
GET /cs2/players?page=1&per_page=25
```

**Parámetros:**
- `page` (int, default=1): Número de página
- `per_page` (int, default=25): Elementos por página

**Respuesta (200):**
```json
{
  "data": [
    {
      "id": 101,
      "nickname": "s1mple",
      "first_name": "Oleksandr",
      "last_name": "Kostyliev",
      "full_name": "Oleksandr Kostyliev",
      "team": {
        "id": 1,
        "name": "Natus Vincere",
        "slug": "natus-vincere",
        "short_name": "Na'Vi"
      },
      "age": 25,
      "birthday": "1997-10-02",
      "steam_id": "76561198034628576",
      "is_active": true
    }
  ],
  "meta": {
    "page": 1,
    "total": 500,
    "next_cursor": "abc123def456"
  }
}
```

#### 4. Obtener Jugador por ID

```
GET /cs2/players/{player_id}
```

**Ejemplo:** `GET /cs2/players/101`

**Respuesta (200):**
```json
{
  "id": 101,
  "nickname": "s1mple",
  "first_name": "Oleksandr",
  "last_name": "Kostyliev",
  "full_name": "Oleksandr Kostyliev",
  "team": { ... },
  "age": 25,
  "birthday": "1997-10-02",
  "steam_id": "76561198034628576",
  "is_active": true
}
```

---

### NBA

**Prefijo Base:** `/nba`

Los endpoints NBA tienen la misma estructura que CS2, pero con datos de la NBA:

#### 1. Listar Equipos NBA

```
GET /nba/teams?page=1&per_page=25
```

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "abbreviation": "ATL",
    "city": "Atlanta",
    "conference": "East",
    "division": "Southeast",
    "full_name": "Atlanta Hawks",
    "name": "Hawks"
  }
]
```

#### 2. Obtener Equipo NBA por ID

```
GET /nba/teams/{team_id}
```

#### 3. Listar Jugadores NBA

```
GET /nba/players?page=1&per_page=25
```

**Respuesta (200):**
```json
{
  "data": [
    {
      "id": 201,
      "first_name": "LeBron",
      "last_name": "James",
      "position": "Forward",
      "height_feet": 6,
      "height_inches": 9,
      "weight_pounds": 250,
      "team": { ... }
    }
  ],
  "meta": { ... }
}
```

#### 4. Obtener Jugador NBA por ID

```
GET /nba/players/{player_id}
```

---

## 💻 Ejemplos de Uso

### Con cURL

```bash
# Obtener equipos CS2
curl -X GET "http://localhost:8000/cs2/teams?page=1&per_page=10"

# Obtener un jugador específico
curl -X GET "http://localhost:8000/cs2/players/101"

# Obtener equipos NBA
curl -X GET "http://localhost:8000/nba/teams"
```

### Con Python (requests)

```python
import requests

# URL base
BASE_URL = "http://localhost:8000"

# 1. Obtener equipos CS2
response = requests.get(f"{BASE_URL}/cs2/teams?page=1&per_page=10")
teams = response.json()
print(teams)

# 2. Obtener jugador por ID
response = requests.get(f"{BASE_URL}/cs2/players/101")
player = response.json()
print(f"Jugador: {player['full_name']}")

# 3. Obtener equipos NBA
response = requests.get(f"{BASE_URL}/nba/teams")
nba_teams = response.json()
print(nba_teams)
```

### Con JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000";

// Obtener equipos CS2
fetch(`${BASE_URL}/cs2/teams?page=1&per_page=10`)
  .then(res => res.json())
  .then(teams => console.log(teams));

// Obtener jugador
fetch(`${BASE_URL}/cs2/players/101`)
  .then(res => res.json())
  .then(player => console.log(`Jugador: ${player.full_name}`));
```

---

## 🔄 Gestión de Rate Limit

### ⚠️ Limitación de la API Externa

BallDontLie permite **5 requests por minuto**. Esta API maneja esto automáticamente:

```python
# En controllers/cs2_infocontroller.py
await asyncio.sleep(12)  # Espera ~12 segundos entre requests
```

### Ejemplo de Comportamiento

```
Solicitud: GET /cs2/teams?page=3
└─ Va a página 1 (request 1) → espera 12s
└─ Va a página 2 (request 2) → espera 12s
└─ Va a página 3 (request 3) → devuelve respuesta
Tiempo total: ~24 segundos
```

### Recomendaciones

1. **Evita solicitar páginas muy altas** (ej: page=100)
2. **Cachea resultados** si necesitas consultas frecuentes
3. **Aumenta el sleep** si aún tienes errores 429

---

## 🏗️ Arquitectura

### Flujo de una Solicitud

```
Cliente HTTP
    ↓
[main.py] ← Crea app FastAPI
    ↓
[router] ← Valida parámetros
    ↓
[controller] ← Procesa lógica de paginación
    ↓
[client] ← Llama API externa
    ↓
BallDontLie (API externa)
    ↓ (respuesta)
[DTO] ← Transforma datos
    ↓
Cliente (JSON)
```

### Patrón de Capas

| Nivel | Qué Hace | Archivo |
|-------|----------|---------|
| **HTTP** | Recibe peticiones, devuelve JSON | `controllers/` |
| **Negocio** | Valida, transforma datos | `services/` |
| **Integración** | Consume API externa | `clients/` |
| **Modelo** | Define estructura | `DTOs/` |

---

## 🚀 Ejecutar la Aplicación

### Modo Desarrollo (con recarga automática)

```bash
uvicorn main:app --reload
```

Accede a:
- **API:** http://localhost:8000
- **Docs (Swagger UI):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Modo Producción

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Con Python directo

```bash
python main.py
```

---

## 📊 Modelos de Datos (DTOs)

### TeamDTO (CS2)

```python
class TeamDTO(BaseModel):
    id: int
    name: str
    slug: Optional[str] = None
    short_name: Optional[str] = None
```

### PlayerDTO (CS2)

```python
class PlayerDTO(BaseModel):
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
```

### PlayersResponseDTO

```python
class PlayersResponseDTO(BaseModel):
    data: List[PlayerDTO]
    meta: Optional[dict]
```

Los modelos de NBA son similares pero con campos específicos del baloncesto (height_feet, weight_pounds, etc.)

---

## 🐛 Troubleshooting

### Error: "API key and URL must be provided"

**Causa:** Faltan variables de entorno

**Solución:**
1. Verifica que existe el archivo `.env`
2. Confirma que tiene las 3 variables requeridas
3. Reinicia la aplicación después de crear `.env`

```bash
# Verifica
echo $env:API_KEY  # PowerShell
echo $API_KEY      # Bash
```

### Error: 429 Too Many Requests

**Causa:** Superaste el límite de 5 requests/minuto

**Soluciones:**
- Aumenta el valor de `asyncio.sleep()` en los controladores
- Implementa caché local
- Solicita menos páginas
- Espera 1 minuto antes de reintentar

### Error: Connection refused

**Causa:** La API externa no está disponible o las URLs son incorrectas

**Solución:**
1. Verifica que las URLs en `.env` son correctas
2. Prueba conectividad: `ping api.balldontlie.io`
3. Verifica que tienes internet

### Error: 401 Unauthorized

**Causa:** API key inválida o expirada

**Solución:**
1. Obtén una nueva key en https://www.balldontlie.io/
2. Actualiza el archivo `.env`
3. Reinicia la aplicación

---

## 📚 Referencias

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [BallDontLie API](https://www.balldontlie.io/)
- [Pydantic Docs](https://docs.pydantic.dev/)
- [httpx Docs](https://www.python-httpx.org/)

---

## 📝 Notas de Desarrollo

### Posibles Mejoras Futuras

1. **Implementar Caché Persistente** (Redis/SQLite)
2. **Agregar Autenticación** (JWT tokens)
3. **Agregar Búsqueda Avanzada** (filtros, ordenamiento)
4. **Implementar Websockets** (actualización en tiempo real)
5. **Agregar Tests Unitarios** (pytest)
6. **Documentar en OpenAPI 3.0**

### Stack Tecnológico

- **Framework:** FastAPI 0.100+
- **Servidor:** Uvicorn
- **Cliente HTTP:** httpx
- **Validación:** Pydantic
- **Python:** 3.10+

---

## ✅ Checklist de Instalación

- [ ] Python 3.10+ instalado
- [ ] Virtual environment creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` creado con 3 variables
- [ ] API key válida de BallDontLie
- [ ] URLs base correctas en `.env`
- [ ] Aplicación corriendo (`uvicorn main:app --reload`)
- [ ] Accedible en http://localhost:8000
- [ ] Swagger UI funciona en http://localhost:8000/docs

---

**Última actualización:** 31 Enero 2026  
**Autor:** Gabriel  
**Licencia:** MIT
