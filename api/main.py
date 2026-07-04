from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import ReservaInvitadoSchema
# Importamos el cliente de Supabase que acabamos de configurar
from api.database import supabase

app = FastAPI(
    title="Sistema de Reservas - Manicure API",
    description="API para la gestión de citas en San Antonio de los Altos.",
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
    return {"status": "online", "message": "Conectado y operando"}

# RUTA DE RESERVAS ACTUALIZADA (AHORA GUARDA EN LA NUBE)
@app.post("/api/reservas", status_code=201)
def crear_reserva_invitado(reserva: ReservaInvitadoSchema):
    try:
        # 1. Convertimos los datos validados por Pydantic en un diccionario compatible con SQL
        data_cita = {
            "manicurista_id": reserva.manicurista_id,
            "diseno_id": reserva.diseno_id,
            "cliente_nombre": reserva.cliente_nombre,
            "cliente_telefono": reserva.cliente_telefono,
            "cliente_email": reserva.cliente_email,
            "sector_san_antonio": reserva.sector_san_antonio,
            "direccion_detalle": reserva.direccion_detail,
            "fecha_cita": str(reserva.fecha_cita), # Convertimos la fecha a texto para PostgreSQL
            "hora_cita": str(reserva.hora_cita),   # Convertimos la hora a texto para PostgreSQL
        }
        
        # 2. Insertamos los datos en la tabla 'citas' de Supabase
        resultado = supabase.table("citas").insert(data_cita).execute()
        
        # 3. Si todo sale bien, Supabase nos devuelve la fila creada (incluyendo su ID UUID único)
        cita_creada = resultado.data[0]
        
        return {
            "status": "success",
            "message": "¡Cita reservada exitosamente en San Antonio de los Altos!",
            "enlace_seguimiento": f"/citas/{cita_creada['id']}", # Este UUID será el link del cliente
            "cita": cita_creada
        }
        
    except Exception as e:
        # Manejo de errores: Si la manicurista ya está ocupada a esa hora, Supabase lanzará un error
        error_msg = str(e)
        if "unique_agenda_manicurista" in error_msg:
            raise HTTPException(
                status_code=400, 
                detail="Lo sentimos, esta manicurista ya tiene una cita agendada para esa fecha y hora."
            )
        
        # Cualquier otro error inesperado (como un ID que no existe)
        raise HTTPException(
            status_code=500, 
            detail=f"Error interno al procesar la reserva: {error_msg}"
        )
