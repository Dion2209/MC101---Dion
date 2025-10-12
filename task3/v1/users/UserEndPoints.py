from fastapi import APIRouter, HTTPException, status, Request, Depends
from sqlalchemy import func
from utils.constants import Endpoints, ResponseMessages
from .UserSchemas import UserSchema, UserLoginSchema, UserRegisterResonseSchema, VoteCountResponseSchema, VotingSchema
#from .UserDBModels import UserDBModel, get_user_by_email, add_user, UserDB
from utils.security import create_access_token, decode_access_token, hash_password, verify_password
from db.DBModels import CandidateDBModel, UserDBModel, VoteDBModel 
from db.DBConfig import get_db

UserRouter = APIRouter(prefix="/users", tags=["Users"])


@UserRouter.post(Endpoints.REGISTER, status_code=status.HTTP_201_CREATED, response_model=UserRegisterResonseSchema) #Post method
def create_user(user : UserSchema, db=Depends(get_db)): 
    #check the user exists
    existing_user = db.query(UserDBModel).filter(UserDBModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessages.USER_ALREADY_EXISTS)
    #Add user to the DB
    """    
    new_user = add_user(UserDBModel(
        name = user.name,
        email = user.email,
        hashed_password=hash_password(user.password),
        is_active=user.is_active) 
    )
    """

    new_user = UserDBModel(**user.model_dump(exclude={"password"}),hashed_password=hash_password(user.password))

    try:

        db.add(new_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    db.refresh(new_user)

    return new_user

"""
from dotenv import load_dotenv
secrets = load_dotenv(".env")
secrets["JWT_SECRET_KEY"] = "your_jwt_secret_key"
"""


# Login Endpoint
@UserRouter.post(Endpoints.LOGIN)
def login_user(user: UserLoginSchema, db=Depends(get_db)):
    # Check user exists
    existing_user = db.query(UserDBModel).filter(UserDBModel.email == user.email).first()
    if not existing_user:
        raise HTTPException(detail=ResponseMessages.USER_NOT_FOUND, status_code=status.HTTP_404_NOT_FOUND)
    # Verify password
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(detail=ResponseMessages.INVALID_PASSWORD,
                            status_code=status.HTTP_401_UNAUTHORIZED)
        # Generate JWT token
    payload = {
        "user_id": str(existing_user.id),
        "email": existing_user.email
    }
    token = create_access_token(data=payload)
    return {"message": ResponseMessages.LOGIN_SUCCESS, "token": token, "authentication_type": "later"}


"""
@UserRouter.get(Endpoints.USER_INFO)
def get_user_info(token = Depends(decode_access_token)):
    print(token)
    return{"message": "User info endpoint"}
"""

"""
@UserRouter.delete(Endpoints.DELETE, status_code=status.HTTP_200_OK)
def delete_user(token_data: dict = Depends(decode_access_token)):
    email = token_data.get("email")
    user = get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessages.USER_NOT_FOUND)

    # Fjern brukeren fra "databasen"
    user_id_to_delete = None
    for user_id, u in list(UserDB.items()):
        if u.email == email:
            user_id_to_delete = user_id
            break

    if user_id_to_delete:
        del UserDB[user_id_to_delete]
        return {"message": ResponseMessages.DELETE_SUCCESS, "status": status.HTTP_200_OK}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=ResponseMessages.USER_NOT_FOUND)
"""

from .UserSchemas import CandidateSchema
AdminRouter = APIRouter(prefix="/admin", tags=["Admin"])

# Add candidates to db
@AdminRouter.post(Endpoints.CANDIDATE, status_code=status.HTTP_201_CREATED)
def add_candidate(new_candidate: CandidateSchema, db=Depends(get_db)):
    candidate = CandidateDBModel(**new_candidate.model_dump())
    try:
        db.add(candidate)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(detail="The candidate has already been created", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    db.refresh(candidate)
    return candidate

@AdminRouter.get(Endpoints.CANDIDATE)
def get_candidates(db=Depends(get_db)):
    candidates = db.query(CandidateDBModel).all()
    return candidates


@AdminRouter.get("/votes/all-candidates/count")
def get_vote_counts(db=Depends(get_db)):
    results = db.query(VoteDBModel.candidate_id, CandidateDBModel.name, func.count(VoteDBModel.id)).join(
        CandidateDBModel, 
        VoteDBModel.candidate_id == CandidateDBModel.id
    ).group_by(VoteDBModel.candidate_id, CandidateDBModel.name).all() 
    results_ = []
    for candidate_id, candidate_name, vote_count in results:
        results_.append(VoteCountResponseSchema(
            candidate_id=candidate_id,
            candidate_name=candidate_name,
            vote_count=vote_count
        ))
    return results_ 


@UserRouter.post(Endpoints.VOTING)
def vote_candidate(candidate: VotingSchema, user = Depends(decode_access_token), db=Depends(get_db)):
    # Check for a candidate
    existing_candidate = db.query(CandidateDBModel).filter(CandidateDBModel.id == candidate.candidate_id).first()
    if not existing_candidate:
        raise HTTPException(detail="Candidate not found", status_code=status.HTTP_404_NOT_FOUND)
    # Check if the user has already voted
    existing_vote = db.query(VoteDBModel).filter(VoteDBModel.user_id == user["user_id"], VoteDBModel.candidate_id == candidate.candidate_id).first()
    if existing_vote:
        raise HTTPException(detail="User has already voted", status_code=status.HTTP_400_BAD_REQUEST)

    # If everything is fine, cast the vote
    new_vote = VoteDBModel(user_id=user["user_id"], candidate_id=candidate.candidate_id)
    try:
        db.add(new_vote)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(detail="Failed to cast vote", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    db.refresh(new_vote)

    return new_vote



