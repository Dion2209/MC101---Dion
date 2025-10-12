from fastapi import FastAPI, status
from utils.constants import Endpoints, ResponseMessages
from v1.users.UserEndPoints import AdminRouter, UserRouter
from logger import get_logger
import uvicorn 

logger = get_logger()

#instance of FastAPI for voting_app
voting_app = FastAPI(
    title="Voting App",
    description="A simple voting application API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

voting_app.include_router(UserRouter)
voting_app.include_router(AdminRouter)
logger.info("User router included in the main app")

@voting_app.get(Endpoints.ROOT)
def read_root():
    """
    This comment wil show up in /docs as well
    """
    return {"message": ResponseMessages.WELCOME, "status": status.HTTP_200_OK}


@voting_app.get(Endpoints.HEALTH)
def read_health():
    return {"message": ResponseMessages.HEALTH_OK, "status": status.HTTP_200_OK}

logger.info("Health check endpoint is set up")
logger.info("Application setup complete. Going to start the server.")