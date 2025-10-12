#from pydantic import BaseModel, EmailStr

#class UserDBModel(BaseModel):
#    id: int = 0
#    name: str 
#    email: EmailStr
#    hashed_password: str 
#    is_active: bool = True 


#UserDB = {} #Key: an uid, value: UserDBModel #Remember "=", easy to forget ;)
"""
def get_user_by_email(email: str):
    return UserDB.get(email)


#This functions gets the next user ID
def get_the_next_user_id():
    if UserDB: #returns false if empty
        return max(UserDB.keys()) + 1 #The second ID will be 2 and so on
    return 1 #the first ID will be 1



#This function gets user based on their email adress
def get_user_by_email(email: str):
    for user in UserDB.values():
        if user.email == email:
            return user
        

def add_user(user: UserDBModel):
    user.id = get_the_next_user_id()
    UserDB[user.id] = user
    return user
"""