from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import date, time
# 1. IMPORTANTE: Asegúrate de agregar 'Optional' aquí arriba
from typing import Literal, Optional 

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
    
    # 2. CAMBIO AQUÍ: Ahora es Optional y su valor por defecto es None
    diseno_id: Optional[str] = Field(default=None, description="ID del diseño del catálogo elegido")
    
    cliente_nombre: str = Field(..., min_length=3, max_length=100, description="Nombre de la clienta")
    cliente_telefono: str = Field(..., description="Teléfono de contacto (WhatsApp)")
    cliente_email: EmailStr = Field(..., description="Correo electrónico válido")
    sector_san_antonio: SECTORES_PERMITIDOS = Field(..., description="Sector de cobertura obligatorio")
    direccion_detail: str = Field(..., min_length=10, description="Dirección detallada o punto de referencia")
    fecha_cita: date = Field(..., description="Fecha elegida para el servicio")
    hora_cita: time = Field(..., description="Hora elegida para el servicio")

    @field_validator("fecha_cita")
    @classmethod
    def validar_fecha(cls, v: date) -> date:
        if v < date.today():
            raise ValueError("No puedes agendar una cita en una fecha pasada.")
        return v

# ... (deja todo lo que ya tenías arriba intacto)
# Agregando schema para crear un diseño de uñas
class DisenoCreateSchema(BaseModel):
    manicurista_id: str = Field(..., description="ID de la manicurista que ofrece este diseño")
    titulo: str = Field(..., min_length=3, max_length=150, description="Nombre del estilo o diseño de uñas")
    descripcion: Optional[str] = Field(default=None, description="Detalles opcionales (ej. Incluye pedrería, tipo de acrílico)")
    url_imagen: str = Field(..., description="Enlace web de la foto (Instagram, Imgur, Pinterest, etc.)")
    precio: float = Field(..., gt=0, description="Precio del servicio en dólares")

 # ==========================================
# ESQUEMA DE PAGOS COMPATIBLE CON TU SQL
# ==========================================
class PagoCreateSchema(BaseModel):
    cita_id: str = Field(..., description="ID UUID de la cita que se está pagando")
    referencia: str = Field(..., min_length=4, max_length=50, description="Número de referencia bancaria")
    monto_pagado: float = Field(..., gt=0, description="Monto exacto reportado en dólares")
    # Le asignamos una URL de texto por defecto para burlar el NOT NULL provisionalmente
    url_captura: str = Field(default="https://placeholder.com/captura_provisional.jpg", description="Enlace de la captura")