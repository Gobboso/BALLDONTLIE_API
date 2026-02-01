# Códigos de Estado HTTP Utilizados en la API

Este documento describe los códigos de estado HTTP estándar que utiliza la API según el estándar REST y HTTP.

---

## 🟢 Respuestas Exitosas (2xx)

### 200 OK
- **Uso:** La solicitud fue exitosa y el servidor devolvió los datos solicitados.
- **Ejemplo:**
  ```
  GET /cs2/teams
  → 200 OK
  {
    "data": [...]
  }
  ```

---

## 🔴 Errores del Cliente (4xx)

### 400 Bad Request
- **Uso:** La solicitud contiene parámetros inválidos o malformados.
- **Causas comunes:**
  - `page` o `per_page` menor a 1
  - `team_id` o `player_id` menor a 1
  - Parámetros de tipo incorrecto
- **Ejemplo:**
  ```
  GET /cs2/teams?page=0
  → 400 Bad Request
  {
    "detail": "page y per_page deben ser mayores a 0"
  }
  ```

### 404 Not Found
- **Uso:** El recurso solicitado no existe en la API externa.
- **Causas comunes:**
  - Equipo con ID inexistente
  - Jugador con ID inexistente
- **Ejemplo:**
  ```
  GET /cs2/teams/99999
  → 404 Not Found
  {
    "detail": "Equipo no encontrado: El equipo con ID 99999 no existe."
  }
  ```

### 429 Too Many Requests
- **Uso:** Se excedió el límite de rate limit (5 requests/minuto con BallDontLie).
- **Nota:** Aunque la API interna respeta el rate limit automáticamente, si ocurre puede mostrar este error.
- **Ejemplo:**
  ```
  → 429 Too Many Requests
  {
    "detail": "Límite de solicitudes superado. Espera 1 minuto e intenta de nuevo."
  }
  ```

---

## 🔴 Errores del Servidor (5xx)

### 500 Internal Server Error
- **Uso:** Error de configuración del servidor o excepción no manejada.
- **Causas comunes:**
  - Variables de entorno faltantes (.env)
  - Errores en la inicialización del cliente
  - Excepción no esperada en el código
- **Ejemplo:**
  ```
  → 500 Internal Server Error
  {
    "detail": "Error de configuración: Debes proporcionar la API key y la URL en el archivo .env"
  }
  ```

### 503 Service Unavailable
- **Uso:** No se puede conectar con la API externa (BallDontLie).
- **Causas comunes:**
  - Falta de conexión a internet
  - API externa caída o no disponible
  - URL incorrecta en .env
- **Ejemplo:**
  ```
  → 503 Service Unavailable
  {
    "detail": "Error de conexión: No se puede conectar con la API BallDontLie. Verifica tu conexión a internet."
  }
  ```

### 504 Gateway Timeout
- **Uso:** La API externa tardó demasiado en responder.
- **Causas comunes:**
  - API externa lenta
  - Problemas de red
  - Timeout en la conexión
- **Ejemplo:**
  ```
  → 504 Gateway Timeout
  {
    "detail": "Error de tiempo: La API BallDontLie tardó demasiado en responder."
  }
  ```

---

## 📋 Tabla de Referencia Rápida

| Código | Estado | Significado | Categoría |
|--------|--------|-------------|-----------|
| **200** | OK | Solicitud exitosa | ✅ Éxito |
| **400** | Bad Request | Parámetros inválidos | ❌ Error del cliente |
| **404** | Not Found | Recurso no encontrado | ❌ Error del cliente |
| **429** | Too Many Requests | Rate limit superado | ❌ Error del cliente |
| **500** | Internal Server Error | Error de configuración/servidor | ❌ Error del servidor |
| **503** | Service Unavailable | API externa no disponible | ❌ Error del servidor |
| **504** | Gateway Timeout | Timeout en la conexión | ❌ Error del servidor |

---

## 🔄 Flujo de Manejo de Errores

```
Solicitud HTTP
    ↓
[Validación de Parámetros]
    ├─ ❌ Inválidos → 400 Bad Request
    └─ ✅ Válidos
        ↓
    [Llamada a API Externa]
        ├─ ❌ No encontrado → 404 Not Found
        ├─ ❌ Sin conexión → 503 Service Unavailable
        ├─ ❌ Timeout → 504 Gateway Timeout
        ├─ ❌ Error HTTP → (código original de BallDontLie)
        └─ ✅ Éxito → 200 OK + datos
```

**Última actualización:** 31 Enero 2026  
**Versión:** 1.0