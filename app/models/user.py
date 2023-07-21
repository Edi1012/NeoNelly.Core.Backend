from typing import Optional
from pydantic import BaseModel, EmailStr, Field, constr, conint, create_model


class SchemaUser(BaseModel):
    
    nombre: constr(strict=True) = Field(...)
    apellido: constr(strict=True) = Field(...)
    dni: conint(strict=True) = Field(...)
    email: EmailStr = Field(...)
    telefono: constr(strict=True) = Field(None)
    direccion: constr(strict=True) = Field(None)
    codigo_postal: constr(strict=True) = Field(None)

    class config:
        schema_extra = {
            "ejemplo": {
                "nombre": "Juana",
                "apellido": "Pilo",
                "dni": 27358783,
                "email": "jpilo@x.ar",
                "telefono": "+54 9 456789",
                "direccion": "calle pública S/n",
                "codigo_postal": "5823"
            }
        }

    @classmethod
    def as_optional(cls):
        annonations = cls.__fields__
        fields = {
            attribute: (Optional[data_type.type_], None)
            for attribute, data_type in annonations.items()
        }
        OptionalModel = create_model(f"Optional{cls.__name__}", **fields)
        return OptionalModel


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}