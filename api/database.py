import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 1. Cargamos las variables de entorno desde el archivo .env
load_dotenv()

# 2. Leemos las credenciales que guardaste
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")

# 3. Control de seguridad: Si olvidaste configurar el archivo .env, el sistema avisa de inmediato
if not supabase_url or not supabase_key:
    raise ValueError("ERROR CRÍTICO: Falta configurar SUPABASE_URL o SUPABASE_KEY en el archivo .env")

# 4. Inicializamos el cliente oficial de Supabase
# Este objeto 'supabase' será nuestro puente para hacer inserts, selects y updates
supabase: Client = create_client(supabase_url, supabase_key)
