from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, time
from typing import Literal

# Definimos los sectores permitidos en San Antonio de los Altos
# Puedes agregar o modificar los sectores según lo necesites
SECTORES_PERMITIDOS = Literal[
    "La Morita", 
    "Las Minas", 
    "El Picacho", 
    "Los Castores", 
    "El Limón",
    "La Suiza",
    "Zona Industrial"
]

class ReservaInvitadoSchema(BaseModel):
    manicurista_id: str = Field(..., description="ID de la manicurista seleccionada")
    diseno_id: str = Field(..., description="ID del diseño del catálogo elegido")
    cliente_nombre: str = Field(..., min_length=3, max_length=100, description="Nombre de la clienta")
    cliente_telefono: str = Field(..., description="Teléfono de contacto (WhatsApp)")
    cliente_email: EmailStr = Field(..., description="Correo electrónico válido")
    sector_san_antonio: SECTORES_PERMITIDOS = Field(..., description="Sector de cobertura obligatorio")
    direccion_detail: str = Field(..., min_length=10, description="Dirección detallada o punto de referencia")
    fecha_cita: date = Field(..., description="Fecha elegida para el servicio")
    hora_cita: time = Field(..., description="Hora elegida para el servicio")

    # Validación personalizada: Evitar que reserven fechas del pasado
    @field_validator("fecha_cita")
    @classmethod
    def validar_fecha(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("No puedes agendar una cita en una fecha pasada.")
        return v
