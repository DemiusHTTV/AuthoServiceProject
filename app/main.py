from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import cars, employees, orders, services, users
from app.database.database import Base, SessionLocal, engine
from app.seed_from_csv import seed_autoservice_from_csv

@asynccontextmanager
async def lifespan(_app: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_autoservice_from_csv(db)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="AutoServices API", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for router in (
        users.router,
        cars.router,
        orders.router,
        employees.router,
        services.router,
    ):
        app.include_router(router)

    @app.get("/")
    def read_root():
        return {"status": "ok", "message": "AutoServices API запущен"}

    return app


app = create_app()
