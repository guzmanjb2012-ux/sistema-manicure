import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración directa (Asegúrate de que tus datos estén aquí escritos)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # Usaremos el puerto 587 que es el más compatible
SMTP_USER = "sanantonionail@gmail.com"  # <-- Tu Gmail del negocio
SMTP_PASSWORD = "gekmlzclhodzqija"        # <-- Tus 16 letras sin espacios

def enviar_correo_notificacion(email_destino: str, cliente_nombre: str, fecha: str, hora: str, diseno: str, estado: str):
    """
    Envía un correo electrónico estilizado a la clienta usando el puerto 587 y STARTTLS.
    """
    if SMTP_USER == "tu_nuevo_correo@gmail.com" or not SMTP_PASSWORD:
        print("⚠️ Alerta: Servidor SMTP no configurado en las variables.")
        return False

    # Crear el contenedor del mensaje
    msg = MIMEMultipart("alternative")
    msg["From"] = f"San Antonio Nails <{SMTP_USER}>"
    msg["To"] = email_destino

    # Definir asunto y diseño según el estado
    if estado == "pendiente":
        msg["Subject"] = "💅 ¡Cita Solicitada con Éxito! - San Antonio Nails"
        titulo_banner = "¡Tu solicitud está en camino!"
        color_banner = "#db2777"
        mensaje_cuerpo = f"Hola <strong>{cliente_nombre}</strong>,<br><br>Hemos recibido tu solicitud de reserva correctamente. La manicurista está verificando la disponibilidad y tu comprobante de pago para confirmar tu cupo."
    elif estado == "confirmada":
        msg["Subject"] = "✨ ¡Tu Cita ha sido Confirmada! - San Antonio Nails"
        titulo_banner = "¡Todo Listo para Consentirte!"
        color_banner = "#10b981"
        mensaje_cuerpo = f"Hola <strong>{cliente_nombre}</strong>,<br><br>¡Excelentes noticias! Tu pago ha sido verificado y tu cita se encuentra <strong>CONFIRMADA</strong>. Prepárate para lucir unas uñas espectaculares."
    else:
        msg["Subject"] = "📢 Actualización de tu Cita - San Antonio Nails"
        titulo_banner = "Cita Cancelada"
        color_banner = "#ef4444"
        mensaje_cuerpo = f"Hola <strong>{cliente_nombre}</strong>,<br><br>Te informamos que tu cita ha sido cancelada en nuestro sistema. Si crees que se trata de un error, por favor ponte en contacto."

    # HTML del correo
    html_content = f"""
    <html>
    <body style="font-family: sans-serif; background-color: #fdf2f8; margin: 0; padding: 20px;">
        <div style="max-width: 500px; margin: 0 auto; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="background-color: {color_banner}; padding: 24px; text-align: center; color: #ffffff;">
                <h2 style="margin: 0; font-size: 20px;">{titulo_banner}</h2>
            </div>
            <div style="padding: 24px; color: #374151; line-height: 1.6;">
                <p style="font-size: 15px;">{mensaje_cuerpo}</p>
                
                <div style="background-color: #f9fafb; border: 1px solid #f3f4f6; border-radius: 12px; padding: 16px; margin: 20px 0;">
                    <h3 style="margin-top: 0; font-size: 14px; color: #9ca3af; text-transform: uppercase;">Detalles del Servicio</h3>
                    <p style="margin: 4px 0; font-size: 14px;"><strong>Fecha:</strong> {fecha}</p>
                    <p style="margin: 4px 0; font-size: 14px;"><strong>Hora:</strong> {hora[:5]} hrs</p>
                    <p style="margin: 4px 0; font-size: 14px;"><strong>Estilo:</strong> {diseno}</p>
                </div>
                <p style="font-size: 12px; color: #9ca3af; text-align: center; margin-top: 30px;">
                    Este es un correo automático del Sistema de Reservas de San Antonio Nails.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        # CREACIÓN DE CONTEXTO SEGURO PERO TOLERANTE A ANTIVIRUS LOCALES
        contexto_ssl = ssl._create_unverified_context()
        
        # 1. Nos conectamos en texto plano usando el puerto 587
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        
        # 2. Saludamos al servidor
        server.ehlo()
        
        # 3. Solicitamos elevar la conexión a Encriptación Segura (STARTTLS)
        server.starttls(context=contexto_ssl)
        
        # 4. Volvemos a saludar ya de forma encriptada
        server.ehlo()
        
        # 5. Iniciamos sesión y enviamos
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(SMTP_USER, email_destino, msg.as_string())
        server.quit()
        
        print(f"📧 Correo de notificación enviado con éxito a {email_destino}")
        return True
    except Exception as e:
        print(f"❌ Error crítico enviando correo: {str(e)}")
        return False
