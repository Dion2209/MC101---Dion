class Endpoints:
    ROOT = "/"
    HEALTH = "/health"
    REGISTER = "/register"
    LOGIN = "/login"
    USER_INFO = "/info"
    DELETE = "/delete"
    CANDIDATE = "/candidate"
    VOTING = "/vote"


class ResponseMessages:
    WELCOME = "Welcome to the Voting App!!"
    HEALTH_OK = "The service is up and running(YAY)!"
    LOGIN_SUCCESS = "Login successful"
    USER_CREATED = "User successfully created"
    USER_ALREADY_EXISTS = "There is already an existing user with that email"
    USER_NOT_FOUND = "User with this email does not exist."
    INVALID_PASSWORD = "The password provided is incorrect."
    DELETE_SUCCESS = "User successfully deleted."
