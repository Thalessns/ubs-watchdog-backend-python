from fastapi import APIRouter

from watchdog.routing.clientes.schemas import ClienteRequest, ClienteResponse
from watchdog.routing.clientes.service import ClientesService

clientes_router = APIRouter(prefix="/clientes")


@clientes_router.post("/", status_code=201, response_model=ClienteResponse)
async def create_cliente(user: ClienteRequest) -> ClienteResponse:
    """Create a new user
    
    Args:
        user (ClienteRequest): User to be created.

    Returns:
        ClienteResponse: Created user.
    """
    return await ClientesService.create_cliente(user)


@clientes_router.get("/", status_code=200, response_model=list[ClienteResponse])
async def get_clientes() -> list[ClienteResponse]:
    """Get all users
    
    Returns:
        list[ClienteResponse]: List of users.
    """
    return await ClientesService.get_clientes()


@clientes_router.get("/by-id", status_code=200, response_model=ClienteResponse)
async def get_user(id: str) -> ClienteResponse:
    """Get a user by ID
    
    Args:
        id (str): User ID.

    Returns:
        ClienteResponse: User with the given ID.
    """
    return await ClientesService.get_cliente_by_id(id)
