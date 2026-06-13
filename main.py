from fastapi import FastAPI, APIRouter
from src.api import contacts, utils

app = FastAPI()

api_router = APIRouter(prefix="/api")

api_router.include_router(utils.router)
api_router.include_router(contacts.router)

app.include_router(api_router)


def main():
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)


if __name__ == "__main__":
    main()
