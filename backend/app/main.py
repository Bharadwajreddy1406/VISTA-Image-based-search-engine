from fastapi import FastAPI
from app.api.router import router
from fastapi.middleware.cors import CORSMiddleware
from app.core.settings import settings
from app.core.databases import engine, Base
from app.providers.object_storages.minio_provider import MinIOProvider
import psycopg2
from psycopg2 import sql

# Ensure models are imported so metadata is available for create_all()
import app.models.image_registry  # noqa: F401


def ensure_database_exists() -> None:
    if settings.POSTGRES_DB == "postgres":
        return

    connection = psycopg2.connect(
        dbname="postgres",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
    )
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (settings.POSTGRES_DB,),
        )
        if cursor.fetchone() is None:
            cursor.execute(
                sql.SQL("CREATE DATABASE {}")
                .format(sql.Identifier(settings.POSTGRES_DB))
            )

    connection.close()


async def lifespan(app: FastAPI):
    ensure_database_exists()
    Base.metadata.create_all(bind=engine)
    MinIOProvider.create_bucket_if_not_exists()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

