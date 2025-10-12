from config import Settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



settings = Settings()

#Postgres engine 

def get_db_url() -> str:
    #host = "voting_db"  # Use the service name defined in docker-compose.yml
    # If we have the postgres in our local machine insted of docker we can use localhost as host
    # host = "host.docker.internal"  # For Windows and Mac to access host machine from Docker container
    # If the postgres in on another server we can use the IP address of that server
    # host = "<IP_ADDRESS>" or "db.example.com"

    # PORTS
    # If the postres in in the docker 
    # port = 5432  # Default Postgres port inside the container
    # If the postgres in ithe host machine 
    # port = 5444  # Port mapped to the host machine
    # If the postgres in on another server we can use the default port or the custom port if it is not the default one
    # port = <PORT>
    PORT = 5432
    return f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD.get_secret_value()}@{settings.POSTGRES_HOST}:{PORT}/{settings.POSTGRES_DB}"


Engine = create_engine(
    get_db_url()
)

SessionLocal = sessionmaker(bind=Engine)

Base = declarative_base()

print("Database connection is successful!")
      
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()