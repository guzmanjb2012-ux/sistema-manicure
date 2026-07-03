from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# Importamos nuestro esquema de validación
from api.schemas import ReservaInvitadoSchema

app = FastAPI(
    title="Sistema de Reservas - Manicure API",
    description="API modular para la gestión de citas de manicure en San Antonio de los Altos.",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "online", "message": "El servidor de manicure está operando correctamente a costo $0"}

# NUEVA RUTA: Recibir la reserva del invitado
@app.post("/api/reservas", status_code=201)
def crear_reserva_invitado(reserva: ReservaInvitadoSchema):
    """
    Simula la creación de una reserva. 
    FastAPI validará automáticamente que cumpla con todas las reglas de schemas.py
    """
    # Por ahora, como no tenemos la base de datos conectada, devolvemos un éxito simulado
    return {
        "message": "¡Validaciones aprobadas con éxito!",
        "data_recibida": reserva,
        "nota": "Próximo paso: Guardar esto en Supabase"
    }
