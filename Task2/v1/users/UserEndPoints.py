from fastapi import APIRouter, HTTPException, status, Request, Depends
from utils.constants import Endpoints, ResponseMessages
from .UserSchemas import UserSchema, UserLoginSchema
from .UserDBModels import UserDBModel, get_user_by_email, add_user, UserDB
from utils.security import create_access_token, decode_access_token, hash_password, verify_password

UserRouter = APIRouter(prefix="/users", tags=["Users"])


@UserRouter.post(Endpoints.REGISTER, status_code=status.HTTP_201_CREATED) #Post method
def create_user(user : UserSchema): 
    #check the user exists
    existing_user = get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ResponseMessages.USER_ALREADY_EXISTS)
    #Add user to the DB
    new_user = add_user(UserDBModel(
        name = user.name,
        email = user.email,
        hashed_password=hash_password(user.password),
        is_active=user.is_active) 
    )

    return {"message": ResponseMessages.USER_CREATED, "status": status.HTTP_201_CREATED}

"""
from dotenv import load_dotenv
secrets = load_dotenv(".env")
secrets["JWT_SECRET_KEY"] = "your_jwt_secret_key"
"""

# Login Endpoint
@UserRouter.post(Endpoints.LOGIN)
def login_user(user: UserLoginSchema):
    # Check user exists
    existing_user = get_user_by_email(user.email)
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



@UserRouter.get(Endpoints.USER_INFO)
def get_user_info(token = Depends(decode_access_token)):
    print(token)
    return{"message": "User info endpoint"}


@UserRouter.delete(Endpoints.DELETE, status_code=status.HTTP_200_OK)
def delete_user(token_data: dict = Depends(decode_access_token)):
    """
    Delete the authenticated user.
    """
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