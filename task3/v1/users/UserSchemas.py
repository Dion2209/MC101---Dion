from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: EmailStr
    password: SecretStr
    #hashed_password: Optional[str] = None
    is_active: bool = True

class UserRegisterResonseSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: SecretStr


class CandidateSchema(BaseModel):
    name: str
    party: Optional[str] = "independent"


class VotingSchema(BaseModel):
    candidate_id: int


class VoteCountResponseSchema(BaseModel):
    candidate_id: int
    candidate_name: str
    vote_count: int
