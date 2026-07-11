from notificaciones import enviar_correo_notificacion

# Prueba enviar un correo directo a tu propio email personal
enviar_correo_notificacion(
    email_destino="sanantonionail@gmail.com", 
    cliente_nombre="Prueba de Sistema", 
    fecha="2026-07-22", 
    hora="14:00:00", 
    diseno="Manicura Rusa", 
    estado="pendiente"
)
