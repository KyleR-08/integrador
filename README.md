# Proyecto Integrador - Tercer Semestre UIDE

Proyecto integrador correspondiente al tercer semestre de la **Universidad Internacional del Ecuador (UIDE)**, que integra los conocimientos adquiridos de todas las materias.


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
- Archivo `auth-service/.env` con las variables de entorno requeridas
- Archivo `mail-service/credentials.json` con las credenciales OAuth de Google Cloud para Gmail API

## Setup

Antes de levantar el proyecto, configura los archivos sensibles a partir de las plantillas incluidas:

### 1. Configurar `auth-service/.env`

Copia el ejemplo y rellena el valor de `AES_KEY`:

```bash
cp auth-service/.env.example auth-service/.env
```

Edita `auth-service/.env` y asigna a `AES_KEY` cualquier cadena de **32 caracteres** (se usa para el cifrado AES de credenciales).

### 2. Configurar `mail-service/credentials.json`

Copia el ejemplo y rellena con credenciales reales obtenidas desde [Google Cloud Console](https://console.cloud.google.com/):

```bash
cp mail-service/credentials.json.example mail-service/credentials.json
```

En Google Cloud Console:

1. Crea (o selecciona) un proyecto.
2. Habilita la **Gmail API**.
3. En **APIs & Services → Credentials**, crea unas credenciales de tipo **OAuth client ID** para una app de escritorio.
4. Descarga el JSON y copia los valores de `client_id`, `project_id` y `client_secret` a `mail-service/credentials.json`.

### 3. No commitear archivos sensibles

> **IMPORTANTE:** Nunca subas `auth-service/.env` ni `mail-service/credentials.json` al repositorio. Ya están ignorados por `.gitignore`; solo se versionan los archivos `*.example`.

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

## Network Infrastructure

Both services are deployed on **VLAN 10 (Microservices)** — `192.168.0.128/27` — within the organizational network infrastructure.

### Network Architecture

- **Router**: Raspberry Pi 3 Model B running OpenWrt 24.10.0 (Router-on-a-Stick)
- **Switches**: SW1 with trunk links, EtherChannel (PAgP Po1, LACP Po2), and Port Security
- **WAN**: WiFi uplink to university network (DHCP) via `phy0-sta0`
- **Services accessible at**: `http://192.168.0.130:8000` (auth) and `http://192.168.0.130:8080` (mail)

### VLAN Segmentation — VLSM Plan (192.168.0.0/16)

| VLAN | Name | Subnet | Gateway | Hosts |
|------|------|--------|---------|-------|
| VLAN 10 | Microservices | 192.168.0.128/27 | 192.168.0.129 | 30 |
| VLAN 20 | Streaming | 192.168.0.64/26 | 192.168.0.65 | 62 |
| VLAN 30 | Mail Server | 192.168.0.0/26 | 192.168.0.1 | 62 |
| VLAN 40 | Counter Strike | 192.168.0.160/27 | 192.168.0.161 | 30 |
| VLAN 50 | Users | 192.168.0.192/27 | 192.168.0.193 | 30 |

### Raspberry Pi Subinterfaces

| Interface | VLAN | IP | Description |
|-----------|------|----|-------------|
| eth0.10 | VLAN 10 | 192.168.0.129/27 | Microservices — Docker containers |
| eth0.20 | VLAN 20 | 192.168.0.65/26 | Streaming Server |
| eth0.30 | VLAN 30 | 192.168.0.1/26 | Mail Server |
| eth0.40 | VLAN 40 | 192.168.0.161/27 | Counter Strike Server |
| eth0.50 | VLAN 50 | 192.168.0.193/27 | User clients |
| phy0-sta0 | WAN | DHCP | University WiFi uplink |

### Network Features

- Inter-VLAN routing via Router-on-a-Stick (OpenWrt)
- NAT Masquerade enabled on WAN zone
- Firewall: ICMP rate limiting (1 pkt/sec), ICMP flood protection, WAN ping blocked
- Port Security on SW1: sticky MAC, max 1 MAC per port, violation restrict
- EtherChannel: PAgP (Po1 toward core) and LACP (Po2 toward SW2)
