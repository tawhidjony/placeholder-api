from fastapi import APIRouter

route = APIRouter()


@route.get("/")
def list_users_controller():
    return "hello world-----------------------"
