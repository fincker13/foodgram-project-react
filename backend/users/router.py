from fastapi import APIRouter


user_router = APIRouter(prefix='/users')
token_router = APIRouter(prefix='/token')


@user_router.get('/')
def get_users():
    return []
