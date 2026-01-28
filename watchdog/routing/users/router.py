from fastapi import APIRouter

from watchdog.routing.users.schemas import UserRequest, UserResponse
from watchdog.routing.users.service import UsersService

router = APIRouter(prefix="/users")


@router.post("/", status_code=201, response_model=UserResponse)
async def create_user(user: UserRequest) -> UserResponse:
    """Create a new user
    
    Args:
        user (UserRequest): User to be created.

    Returns:
        UserResponse: Created user.
    """
    return await UsersService.create_user(user)


@router.get("/", status_code=200, response_model=list[UserResponse])
async def get_users() -> list[UserResponse]:
    """Get all users
    
    Returns:
        list[UserResponse]: List of users.
    """
    return await UsersService.get_users()


@router.get("/by-id", status_code=200, response_model=UserResponse)
async def get_user(id: str) -> UserResponse:
    """Get a user by ID
    
    Args:
        id (str): User ID.

    Returns:
        UserResponse: User with the given ID.
    """
    return await UsersService.get_user_by_id(id)
