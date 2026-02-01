from uuid import uuid4
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from watchdog.database.database import Database
from watchdog.database.entities import clientes_table

from watchdog.routing.clientes.exceptions import (
    ClienteNotFoundException,
    ClienteEmailAlreadyExistsException
)
from watchdog.routing.clientes.schemas import (
    ClienteRequest,
    ClienteResponse
)


class ClientesService:

    @classmethod
    async def create_cliente(cls, new_user: ClienteRequest) -> ClienteResponse:
        """Create a new cliente in the database.
        
        Args:
            new_user (ClienteRequest): The cliente data to be created.

        Returns:
            ClienteResponse: The created cliente data.

        Raises:
            ClienteEmailAlreadyExistsException: If a cliente with the same email already exists.
        """
        new_id = uuid4()
        date_created = datetime.now()

        query = clientes_table.insert().values(
            id = new_id,
            nome = new_user.nome,
            email = new_user.email,
            pais = new_user.pais,
            nivel_risco = new_user.nivel_risco.value,
            status_kyc = new_user.status_kyc.value,
            data_criacao = date_created
        )
        try:
            await Database.execute(query)
        except IntegrityError:
            raise ClienteEmailAlreadyExistsException(email=new_user.email)
        return ClienteResponse(id=new_id, **new_user.model_dump(), data_criacao=date_created)

    @classmethod
    async def get_clientes(cls) -> list[ClienteResponse]:
        """Retrieve all clientes from the database.

        Returns:
            list[ClienteResponse]: A list of all clientes.
        """
        query = clientes_table.select()
        rows = await Database.fetch_all(query)
        return [ClienteResponse(**row) for row in rows]

    @classmethod
    async def get_cliente_by_id(cls, cliente_id: str) -> ClienteResponse:
        """Retrieve a cliente by their ID.

        Args:
            cliente_id (str): The ID of the cliente to retrieve.

        Returns:
            ClienteResponse: The cliente data.

        Raises:
            ClienteNotFoundException: If no cliente with the given ID is found.
        """
        query = clientes_table.select().where(clientes_table.c.id == cliente_id)
        row = await Database.fetch_one(query)
        if not row:
            raise ClienteNotFoundException(id=cliente_id)
        return ClienteResponse(**row)
