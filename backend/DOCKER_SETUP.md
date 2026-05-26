# Docker Setup Instructions

All services run from the `backend/` folder using Docker Compose.

## Project Structure (backend folder)

```
backend/
├── docker-compose.yaml              # Main compose file with includes
├── docker-compose.postgres.yaml     # PostgreSQL + pgAdmin services
├── docker-compose.minio.yaml        # MinIO object storage
├── docker-compose.milvus.yaml       # Milvus vector database
├── .env.example                     # Environment variables template
├── .env                             # Your configuration
├── app/                             # Python application
├── requirements.txt                 # Python dependencies
└── venv/                            # Virtual environment
```

## Quick Start

### 1. Environment Variables
```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` with your configuration:
```env
# Postgres
POSTGRES_DB=vista_db
POSTGRES_USER=vista_user
POSTGRES_PASSWORD=your_secure_password

# pgAdmin
PGADMIN_DEFAULT_EMAIL=admin@example.com
PGADMIN_DEFAULT_PASSWORD=your_secure_password

# MinIO
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=your_secure_password
MINIO_LICENSE_PATH=./minio/minio.license

# Milvus
MILVUS_DATA_PATH=./volumes/milvus
```

### 2. MinIO License (Required)
1. Download your MinIO AIStor Free Tier license from: https://min.io/pricing
2. Place the license file at: `./minio/minio.license`

### 3. Configuration Files (Auto-created)
The following files are already configured:
- `milvus/embedEtcd.yaml` - Embedded etcd configuration
- `milvus/user.yaml` - Custom Milvus overrides

## Starting Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Restart a specific service
docker-compose up -d postgres
```

## Access Services

| Service | URL/Port | Credentials |
|---------|----------|-------------|
| pgAdmin | http://localhost:5050 | Email & password from `.env` |
| MinIO Console | http://localhost:9001 | MINIO_ROOT_USER/PASSWORD |
| Milvus gRPC | localhost:19530 | No auth (local) |
| Milvus HTTP | http://localhost:9091 | No auth (local) |
| PostgreSQL | localhost:5432 | User/password from `.env` |

## Service Details

- **PostgreSQL** (postgres/): Port 5432 - Relational database
- **pgAdmin** (postgres/): Port 5050 - PostgreSQL web UI
- **MinIO** (minio/): Ports 9000 (API), 9001 (Console) - Object storage
- **Milvus** (milvus/): Ports 19530 (gRPC), 9091 (HTTP), 2379 (etcd) - Vector database

## Useful Commands

```bash
# View all running containers
docker-compose ps

# Access PostgreSQL shell
docker exec -it postgres psql -U vista_user -d vista_db

# MinIO client setup
mc alias set minio http://localhost:9000 minioadmin your_password
mc ls minio/

# Check Milvus health
curl http://localhost:9091/healthz

# View service logs
docker-compose logs postgres
docker-compose logs minio
docker-compose logs milvus
```

## Service-Specific Documentation

See the README.md files in each service folder:
- [postgres/README.md](postgres/README.md) - PostgreSQL & pgAdmin
- [minio/README.md](minio/README.md) - MinIO AIStor
- [milvus/README.md](milvus/README.md) - Milvus

## Troubleshooting

- **Milvus takes time to start**: Initial startup can take 90+ seconds. Check logs with `docker-compose logs milvus`.
- **MinIO license error**: Ensure the license file exists at `./minio/minio.license`.
- **Port conflicts**: If ports are already in use, modify port mappings in the respective `docker-compose.yaml` files.
- **Connection refused**: Ensure all services are healthy with `docker-compose ps`.
- **Volume permission errors**: On Linux, you may need to adjust volume permissions or use `sudo`.

## Modular Architecture

This setup uses Docker Compose's `include` feature to keep services modular:
- Each service has its own `docker-compose.yaml`
- The main `docker-compose.yaml` includes all service files
- Services can be deployed independently or together
- Easy to add/remove services by modifying includes in the main compose file

