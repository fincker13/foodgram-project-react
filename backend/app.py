import uvicorn

from fastapi import FastAPI

from users.router import user_router


app = FastAPI()

app.include_router(user_router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
