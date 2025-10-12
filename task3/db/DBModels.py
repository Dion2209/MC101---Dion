from sqlalchemy import Column, Integer, String, TIMESTAMP, func, Boolean
from db.DBConfig import Base, Engine

class TableNames:
    USERS = "users"
    CANDIDATES = "candidates"
    VOTES = "votes"

class ColumnNames:
    ID = "id"
    USER_ID = "user_id"
    CANDIDATE_ID = "candidate_id"
    EMAIL = "email"
    HASHED_PASSWORD = "hashed_password"
    Name = "name"
    IS_ACTIVE = "is_active"
    CREATED_AT = "created_at"
    PARTY = "party"

class UserDBModel(Base):
    __tablename__ = TableNames.USERS # table name in the database

    id = Column(ColumnNames.ID, Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(ColumnNames.EMAIL, String, unique=True, index=True, nullable=False)
    hashed_password = Column(ColumnNames.HASHED_PASSWORD, String, nullable=False)
    name = Column(ColumnNames.Name, String, nullable=True)
    is_active = Column(ColumnNames.IS_ACTIVE, Boolean, default=1) 
    created_at = Column(ColumnNames.CREATED_AT, TIMESTAMP(True), default=func.now(), nullable=False)

class CandidateDBModel(Base):
    __tablename__ = TableNames.CANDIDATES

    id = Column(ColumnNames.ID, Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(ColumnNames.Name, String, nullable=False, unique=True)
    party = Column(ColumnNames.PARTY, String, nullable=True)  # Party may be optional
    created_at = Column(ColumnNames.CREATED_AT, TIMESTAMP(True), default=func.now(), nullable=False)    
    

class VoteDBModel(Base):
    __tablename__ = TableNames.VOTES

    id = Column(ColumnNames.ID, Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(ColumnNames.USER_ID, Integer, nullable=False, foreign_key=f"{TableNames.USERS}.{ColumnNames.ID}")  # Foreign key to UserDBModel
    candidate_id = Column(ColumnNames.CANDIDATE_ID, Integer, nullable=False, foreign_key = f"{TableNames.CANDIDATES}.{ColumnNames.ID}")  # Foreign key to CandidateDBModel
    created_at = Column(ColumnNames.CREATED_AT, 
                        TIMESTAMP(True), 
                        default=func.now(), 
                        nullable=False)


Base.metadata.create_all(bind=Engine)

"""
class UserDBModel(BaseModel):
    id: int = 0
    name: str 
    email: EmailStr
    hashed_password: str 
    is_active: bool = True 
"""