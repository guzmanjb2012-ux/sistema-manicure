from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import ReservaInvitadoSchema, DisenoCreateSchema, PagoCreateSchema
from api.database import supabase
from typing import Optional
from datetime import date 

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


# ==========================================
# RUTA: RESERVA DE CLIENTES INVITADOS
# ==========================================
@app.post("/api/reservas", status_code=201)
def crear_reserva_invitado(reserva: ReservaInvitadoSchema):
    try:
        data_cita = {
            "manicurista_id": reserva.manicurista_id,
            "diseno_id": reserva.diseno_id,
            "cliente_nombre": reserva.cliente_nombre,
            "cliente_telefono": reserva.cliente_telefono,
            "cliente_email": reserva.cliente_email,
            "sector_san_antonio": reserva.sector_san_antonio,
            "direccion_detalle": reserva.direccion_detail,
            "fecha_cita": str(reserva.fecha_cita), 
            "hora_cita": str(reserva.hora_cita),   
        }
        resultado = supabase.table("citas").insert(data_cita).execute()
        cita_creada = resultado.data[0]
        return {
            "status": "success",
            "message": "¡Cita reservada exitosamente en San Antonio de los Altos!",
            "enlace_seguimiento": f"/citas/{cita_creada['id']}", 
            "cita": cita_creada
        }
    except Exception as e:
        error_msg = str(e)
        if "unique_agenda_manicurista" in error_msg:
            raise HTTPException(status_code=400, detail="Lo sentimos, esta manicurista ya tiene una cita agendada para esa fecha y hora.")
        raise HTTPException(status_code=500, detail=f"Error interno al procesar la reserva: {error_msg}")


# ==========================================
# RUTAS: CATÁLOGO DE DISEÑOS
# ==========================================
@app.post("/api/disenos", status_code=201)
def crear_diseno(diseno: DisenoCreateSchema):
    try:
        data_diseno = {
            "manicurista_id": diseno.manicurista_id,
            "titulo": diseno.titulo,
            "descripcion": diseno.descripcion,
            "url_imagen": diseno.url_imagen,
            "precio": diseno.precio
        }
        resultado = supabase.table("catalogo_disenos").insert(data_diseno).execute()
        return {
            "status": "success",
            "message": "Diseño agregado al catálogo exitosamente.",
            "diseno": resultado.data[0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al registrar el diseño: {str(e)}")

@app.get("/api/disenos")
def obtener_catalogo(manicurista_id: Optional[str] = Query(None, description="Filtrar catálogo por el ID de una manicurista específica")):
    try:
        query = supabase.table("catalogo_disenos").select("*")
        if manicurista_id:
            query = query.eq("manicurista_id", manicurista_id)
        resultado = query.execute()
        return resultado.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar el catálogo: {str(e)}")


# ==========================================
# RUTA: AGENDA DE LA MANICURISTA
# ==========================================
@app.get("/api/agenda")
def obtener_agenda_manicurista(
    manicurista_id: str = Query(..., description="ID de la manicurista de la cual queremos ver la agenda"),
    fecha: date = Query(..., description="Fecha específica a consultar (Formato: YYYY-MM-DD)")
):
    try:
        query = supabase.table("citas").select("*")
        query = query.eq("manicurista_id", manicurista_id)
        query = query.eq("fecha_cita", str(fecha))
        query = query.order("hora_cita", desc=False)
        resultado = query.execute()
        return {
            "status": "success",
            "manicurista_id": manicurista_id,
            "fecha_consultada": str(fecha),
            "total_citas": len(resultado.data),
            "agenda": resultado.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al consultar la agenda: {str(e)}")


# ==========================================
# RUTA: REGISTRO DE PAGOS
# ==========================================
@app.post("/api/pagos", status_code=201)
def registrar_pago_cita(pago: PagoCreateSchema):
    try:
        data_pago = {
            "cita_id": pago.cita_id,
            "referencia": pago.referencia,
            "monto_pagado": pago.monto_pagado,
            "url_captura": pago.url_captura 
        }
        resultado_pago = supabase.table("pagos").insert(data_pago).execute()
        supabase.table("citas").update({"estado": "confirmada"}).eq("id", pago.cita_id).execute()
        
        return {
            "status": "success",
            "message": "¡Pago registrado y cita confirmada exitosamente!",
            "pago": resultado_pago.data[0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el pago y actualizar la cita: {str(e)}")


# ==========================================
# NUEVA RUTA: DETALLE DE CITA (RECIBO DIGITAL)
# ==========================================

@app.get("/api/reservas/{cita_id}")
def obtener_detalle_cita(cita_id: str):
    """
    Busca una cita específica por su ID. 
    Trae de forma automática los datos del diseño asociado desde la tabla 'catalogo_disenos'.
    """
    try:
        # La magia relacional: Usamos 'catalogo_disenos(*)' dentro del select.
        # Supabase detecta la llave foránea y hace el JOIN automáticamente en la nube.
        resultado = supabase.table("citas").select("*, catalogo_disenos(*)").eq("id", cita_id).execute()
        
        # Si la lista de datos viene vacía, significa que ese UUID no existe en la tabla
        if not resultado.data:
            raise HTTPException(
                status_code=404, 
                detail="Lo sentimos, el código de cita proporcionado no es válido o ya no existe."
            )
            
        # Como buscamos por ID único, extraemos el primer (y único) resultado
        cita_detalle = resultado.data[0]
        
        return {
            "status": "success",
            "message": "Recibo digital obtenido correctamente.",
            "datos_recibo": cita_detalle
        }
        
    except HTTPException as http_err:
        # Re-lanzamos el 404 para que no se convierta en un error 500 genérico
        raise http_err
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error en el servidor al generar el recibo digital: {str(e)}"
        )
