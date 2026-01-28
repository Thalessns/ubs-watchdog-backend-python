from uuid import UUID4
from datetime import datetime
from sqlalchemy import IntegrityError

from watchdog.database.database import Database
from watchdog.database.entities import users_table

from watchdog.routing.users.exceptions import (
    UserNotFoundException,
    UserEmailAlreadyExistsException
)
from watchdog.routing.users.schemas import (
    UserRequest,
    UserResponse
)


class UsersService:

    @classmethod
    async def create_user(cls, new_user: UserRequest) -> UserResponse:
        """Create a new user in the database.
        
        Args:
            new_user (UserRequest): The user data to be created.

        Returns:
            UserResponse: The created user data.

        Raises:
            UserEmailAlreadyExistsException: If a user with the same email already exists.
        """
        new_id = UUID4()
        date_created = datetime.now()

        query = users_table.insert().values(
            id = new_id,
            name = new_user.name,
            email = new_user.email,
            nivel_risco = new_user.nivel_risco,
            status_kyc = new_user.status_kyc,
            data_criacao = date_created
        )
        try:
            await Database.execute(query)
        except IntegrityError:
            raise UserEmailAlreadyExistsException(id=new_user.email)
        return UserResponse(id=new_id, **new_user.model_dump(), data_criacao=date_created)

    @classmethod
    async def get_users(cls) -> list[UserResponse]:
        """Retrieve all users from the database.

        Returns:
            list[UserResponse]: A list of all users.
        """
        query = users_table.select()
        rows = await Database.fetch_all(query)
        return [UserResponse(**row) for row in rows]

    @classmethod
    async def get_user_by_id(cls, user_id: UUID4) -> UserResponse:
        """Retrieve a user by their ID.

        Args:
            user_id (UUID4): The ID of the user to retrieve.

        Returns:
            UserResponse: The user data.

        Raises:
            UserNotFoundException: If no user with the given ID is found.
        """
        query = users_table.select().where(users_table.c.id == user_id)
        row = await Database.fetch_one(query)
        if not row:
            raise UserNotFoundException(id=user_id)
        return UserResponse(**row)
