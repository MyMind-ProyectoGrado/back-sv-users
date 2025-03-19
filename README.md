# MyMind - Backend

## 📌 Descripción
**MyMind** es una aplicación diseñada para ayudar a los estudiantes universitarios a gestionar sus emociones mediante el análisis de notas de voz. Este repositorio contiene el backend basado en **FastAPI**, que maneja la autenticación y recepción de peticiones del usuario.

## 🚀 Instalación y Configuración
## 🐳 Despliegue con Docker

###  Ejecutar el contenedor
```bash
docker-compose up --build
```

## 🔑 Autenticación
El sistema usa **JWT con OAuth2** para la autenticación. Se generan dos tokens:
- **Access Token** (expira en 1 hora)
- **Refresh Token** (expira en 7 días)

## 📡 Endpoints principales (ACTUALES)

| Método | Ruta               | Descripción |
|--------|--------------------|-------------|
| POST   | `/auth/login`      | Inicia sesión y devuelve tokens JWT |
| POST   | `/auth/refresh`    | Renueva el Access Token usando el Refresh Token |
| POST   | `/users/register`  | Registro de usuario |
| GET    | `/analysis/report` | Obtiene un reporte de análisis emocional |



## 📜 Licencia
Este proyecto es propiedad intelectual de los miembros del grupo myMind.
