import os
import motor.motor_asyncio
from bson.objectid import ObjectId


client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"])

database = client.socies

user_collection = database.get_collection("users")# helpers

def user_helper(User) -> dict:
    return {
        "id": str(User["_id"]),
        "nombre": User["nombre"],
        "apellido": User["apellido"],
        "dni": str(User["dni"]),
        "email": User["email"],
        "telefono": User["telefono"],
        "codigo_postal": User["codigo_postal"]
    }

# Buscar todes les users de la base de datos
async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users

# Agregar un user a la base de datos

async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Buscar un user a partir de un ID
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


# Actulizar un user a partir de un ID
async def update_user(id: str, data: dict):
    # Devuelve falso si el cuerpo del request está vacio
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False

# Borrar un user de la base de datos
async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True