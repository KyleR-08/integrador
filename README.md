# Proyecto Integrador - Tercer Semestre UIDE

Proyecto integrador correspondiente al tercer semestre de la **Universidad Internacional del Ecuador (UIDE)**, que integra los conocimientos adquiridos en las siguientes materias:

- **Fundamentos de la Seguridad** — Ing. Darío Cabezas
- **Programación Orientada a Objetos** — Ing. Ivan Reyes

## Arquitectura

El proyecto está compuesto por dos microservicios independientes:

| Servicio | Lenguaje | Puerto | Descripción |
|----------|----------|--------|-------------|
| `auth-service` | Python (FastAPI) | `8000` | Servicio de autenticación con hashing bcrypt + pepper, SQLModel y SQLite. |
| `mail-service` | Go (Gin) | `8080` | Gestor de correos integrado con la API de Gmail. |

## Estructura

```
proyecto-integrador/
├── auth-service/        # Microservicio de autenticación (Python/FastAPI)
├── mail-service/        # Microservicio de correo (Go/Gin)
├── docker-compose.yml   # Orquestación de ambos servicios
└── README.md
```

## Requisitos previos

- [Docker](https://www.docker.com/) y Docker Compose
- Archivo `auth-service/.env` con las variables de entorno requeridas (incluyendo `PEPPER_SECRET`)
- Archivo `mail-service/credentials.json` con las credenciales OAuth de Google Cloud para Gmail API

## Levantar el proyecto

Desde la raíz `proyecto-integrador/`:

```bash
docker-compose up --build
```

Esto construirá las imágenes de ambos servicios y los expondrá en:

- Auth Service → http://localhost:8000
- Mail Service → http://localhost:8080

## Detener el proyecto

```bash
docker-compose down
```

## Notas de seguridad

- Los archivos sensibles (`.env`, `credentials.json`, tokens OAuth, base de datos) están excluidos del control de versiones mediante `.gitignore`.
- Las contraseñas de usuarios se almacenan utilizando `bcrypt` con un secreto adicional (pepper) cargado por variable de entorno.
