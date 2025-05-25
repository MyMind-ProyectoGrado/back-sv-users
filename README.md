# MyMind - Backend 🧠

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/)
[![MongoDB](https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

## 📌 Descripción

**MyMind** es una aplicación diseñada para ayudar a estudiantes universitarios a gestionar sus emociones mediante el análisis de notas de voz. Este repositorio contiene el **microservicio de usuarios** basado en **FastAPI**, que maneja la gestión de usuarios, autenticación y almacenamiento de transcripciones con análisis emocional.

### ✨ Características principales

- **Gestión de usuarios**: Registro, perfiles, configuraciones y eliminación de cuentas
- **Autenticación JWT**: Integración con Auth0 para manejo seguro de tokens
- **Transcripciones**: Almacenamiento y consulta de análisis de audio con datos emocionales
- **Filtros avanzados**: Búsqueda por emoción, sentimiento, tema, fecha y hora
- **Monitoreo**: Métricas con Prometheus para observabilidad
- **Arquitectura de microservicios**: Integración con APISIX como API Gateway

## 🛠️ Stack Tecnológico

- **Framework**: FastAPI 
- **Base de datos**: MongoDB con Motor (driver asíncrono)
- **Autenticación**: JWT tokens con Auth0
- **Contenedores**: Docker & Docker Compose
- **Monitoreo**: Prometheus + métricas personalizadas
- **Validación**: Pydantic schemas
- **Ambiente**: Python 3.10+

## 🚀 Instalación y Configuración

### Prerrequisitos

- Docker y Docker Compose instalados
- Python 3.10+ (para desarrollo local)
- Conexión a MongoDB (local o en la nube)

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd mymind-backend
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# MongoDB
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/

# Entorno
ENVIRONMENT=development  # o production

# APISIX (para producción)
APISIX_PROD=<ip-del-gateway-en-produccion>
```

### 3. Despliegue con Docker

```bash
# Construir y ejecutar el contenedor
docker-compose up --build

# En modo detached (segundo plano)
docker-compose up -d --build
```

La aplicación estará disponible en: `http://localhost:8000`

### 4. Desarrollo local (opcional)

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 Endpoints de la API

### 👤 Gestión de Usuarios (`/users`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/users/register` | Registrar nuevo usuario |
| `GET` | `/users/profile` | Obtener perfil completo |
| `GET` | `/users/name` | Obtener nombre del usuario |
| `PATCH` | `/users/update-name` | Actualizar nombre |
| `GET` | `/users/email` | Obtener email del usuario |
| `PATCH` | `/users/update-email` | Actualizar email |
| `GET` | `/users/notifications` | Obtener configuración de notificaciones |
| `PATCH` | `/users/update-notifications` | Alternar notificaciones |
| `GET` | `/users/profile-pic` | Obtener URL de foto de perfil |
| `PATCH` | `/users/update-profile-pic` | Actualizar foto de perfil |
| `GET` | `/users/privacy` | Obtener configuración de privacidad |
| `PATCH` | `/users/privacy` | Alternar configuración de privacidad |
| `DELETE` | `/users/delete` | Eliminar cuenta de usuario |

### 📝 Transcripciones (`/users/transcriptions`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/users/transcriptions/` | Obtener todas las transcripciones |
| `GET` | `/users/transcriptions/{id}` | Obtener transcripción específica |
| `GET` | `/users/transcriptions/by-emotion/{emotion}` | Filtrar por emoción |
| `GET` | `/users/transcriptions/by-sentiment/{sentiment}` | Filtrar por sentimiento |
| `GET` | `/users/transcriptions/by-topic/{topic}` | Filtrar por tema |
| `GET` | `/users/transcriptions/by-date/{date}` | Filtrar por fecha |
| `GET` | `/users/transcriptions/by-hour/{start}-{end}` | Filtrar por rango de horas |
| `GET` | `/users/transcriptions/filter` | Filtros múltiples combinados |
| `DELETE` | `/users/transcriptions/delete-transcription/{id}` | Eliminar transcripción específica |
| `DELETE` | `/users/transcriptions/delete-all-transcriptions` | Eliminar todas las transcripciones |

### 🎤 Audio (`/audio`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/audio/test` | Endpoint de prueba |

## 🔑 Autenticación

El sistema utiliza **JWT tokens** con integración a **Auth0**:

- Los tokens son validados por el API Gateway (APISIX)
- El backend extrae el `user_id` del token sin validar la firma
- Cada usuario se identifica por el `sub` claim del JWT

### Estructura del token JWT esperado:

```json
{
  "sub": "auth0|usuario123",  // ID único del usuario
  "exp": 1640995200,          // Timestamp de expiración
  "iat": 1640991600           // Timestamp de emisión
}
```

## 📊 Monitoreo y Métricas

El servicio expone métricas de Prometheus en `/metrics` incluyendo:

- **Contadores de requests**: Total de peticiones por endpoint
- **Contadores de respuestas**: Respuestas por código de estado
- **Contadores de excepciones**: Errores y excepciones
- **Gauge de requests activos**: Peticiones en progreso
- **Histograma de latencia**: Tiempo de respuesta por endpoint

### Métricas disponibles:

- `fastapi_requests_total`
- `fastapi_responses_total` 
- `fastapi_exceptions_total`
- `fastapi_requests_in_progress`
- `fastapi_request_duration_seconds`

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   APISIX     │───▶│  Backend Users  │
│   (React/Vue)   │    │  (Gateway)   │    │   (FastAPI)     │
└─────────────────┘    └──────────────┘    └─────────────────┘
                              │                       │
                              │                       ▼
                              │              ┌─────────────────┐
                              │              │    MongoDB      │
                              │              │   (Database)    │
                              │              └─────────────────┘
                              ▼
                    ┌──────────────────┐
                    │   Prometheus     │
                    │  (Monitoring)    │
                    └──────────────────┘
```

## 📦 Modelos de Datos

### Usuario (UserSchema)

```python
{
  "_id": "auth0|usuario123",        # ID único de Auth0
  "name": "Juan Pérez",
  "email": "juan@email.com",
  "profilePic": "https://...",
  "birthdate": "1995-05-15",
  "city": "Bogotá",
  "personality": "Introvertido",
  "university": "Universidad Nacional",
  "degree": "Ingeniería de Sistemas",
  "gender": "Masculino",
  "notifications": true,
  "privacy": {
    "allow_anonimized_usage": false
  },
  "data_treatment": {
    "accept_policies": true,
    "acceptance_date": "2024-01-15T10:30:00",
    "acceptance_ip": "192.168.1.1",
    "privacy_preferences": {
      "allow_anonimized_usage": false
    }
  },
  "transcriptions": [...]
}
```

### Transcripción (Transcription)

```python
{
  "_id": "transcription_id_123",
  "date": "2024-01-15",
  "time": "14:30",
  "text": "Hoy me siento muy ansioso por el examen...",
  "emotion": "ansiedad",
  "emotionProbabilities": {
    "ansiedad": 0.85,
    "tristeza": 0.10,
    "alegría": 0.05
  },
  "sentiment": "negativo",
  "sentimentProbabilities": {
    "positivo": 0.15,
    "negativo": 0.75,
    "neutral": 0.10
  },
  "topic": "estudios"
}
```

## 🔒 Seguridad

- **Validación de origen**: Solo acepta peticiones del API Gateway
- **Autenticación JWT**: Tokens validados por Auth0
- **Validación de datos**: Schemas de Pydantic para todos los inputs
- **Variables de entorno**: Configuración sensible en archivos `.env`
- **CORS configurado**: Para permitir requests del frontend

## 🧪 Testing

```bash
# Ejecutar tests (cuando estén implementados)
pytest

# Verificar que el servicio está funcionando
curl http://localhost:8000/
```

## 📈 Desarrollo y Contribución

### Estructura del proyecto

```
app/
├── core/
│   ├── auth.py          # Lógica de autenticación
│   └── database.py      # Conexión a MongoDB
├── routes/
│   ├── users.py         # Endpoints de usuarios
│   ├── transcriptions.py # Endpoints de transcripciones
│   └── audio.py         # Endpoints de audio
├── schemas/
│   ├── user_schema.py   # Modelos de usuario
│   └── transcription_schema.py # Modelos de transcripción
└── main.py              # Aplicación principal
```

### Pasos para contribuir

1. Fork del repositorio
2. Crear una rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Hacer commits descriptivos: `git commit -m "Add: nueva funcionalidad"`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear un Pull Request

## 📋 TODO / Roadmap

- [ ] Implementar tests unitarios e integración
- [ ] Añadir documentación con Swagger/OpenAPI
- [ ] Implementar cache con Redis
- [ ] Añadir logs estructurados
- [ ] Implementar rate limiting
- [ ] Añadir backup automático de MongoDB
- [ ] Mejorar manejo de errores y excepciones

## 🐛 Troubleshooting

### Problemas comunes

**Error de conexión a MongoDB:**
```bash
# Verificar la variable MONGO_URI en .env
echo $MONGO_URI
```

**Error 403 Forbidden:**
- Verificar que las peticiones vienen del API Gateway correcto
- Revisar la configuración de ENVIRONMENT y APISIX_PROD

**El contenedor no inicia:**
```bash
# Ver logs del contenedor
docker-compose logs backend
```

## 📄 Licencia

Este proyecto es propiedad intelectual de los miembros del grupo **MyMind**.

---

## 👥 Equipo

Desarrollado con ❤️ por el equipo MyMind para apoyar el bienestar emocional de estudiantes universitarios.

---

**¿Necesitas ayuda?** Abre un issue en el repositorio o contacta al equipo de desarrollo.
