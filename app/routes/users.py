from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from models.user import ResponseModel, SchemaUser, ErrorResponseModel

from server.database import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_users,
    update_user,
)


router = APIRouter()

@router.post("/", response_description="Add user")
async def add_user_data(User: SchemaUser = Body(...)):
    User = jsonable_encoder(User)
    new_user = await add_user(User)
    return ResponseModel(new_user, "Usuario agregado.")


@router.get("/", response_description="Get all Users")
async def get_users():
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "users data")
    return ResponseModel(users, "No data")


@router.get("/{id}", response_description="Get user by id")
async def get_user_data(id):
    User = await retrieve_user(id)
    if User:
        return ResponseModel(User, "user data")
    return ErrorResponseModel("Ocurrió un error", 404, "El User no existe.")


@router.put("/{id}")
async def update_user_data(id: str, req: SchemaUser.as_optional() = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel(
            "Se pudo actualizar el usuario con el ID: {} ".format(id),
            "Socio Actualizado correctamente",
        )
    return ErrorResponseModel(
        "Ocurrió un error",
        404,
        "Hubo una falla actualizando los datos del usuario",
    )

@router.delete("/{id}", response_description="delete user")
async def delete_user_data(id: str):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User ID: {} borrado".format(id), "Socio Borrado exitosamente"
        )
    return ErrorResponseModel(
        "Hubo un error", 404, "Socio con id {0} no existe".format(id)
    )