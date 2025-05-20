from fastapi import FastAPI

from app.core.database import engine
from app.database.base_class import Base
from app.routes.base_route import router


def init_db():
    Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI with PostgresSQL"}
