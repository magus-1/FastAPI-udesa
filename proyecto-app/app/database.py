from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from sqlalchemy import text

# Configuración de la base de datos
db_username = 'postgres'  # Nombre de usuario de la base de datos
db_password = 'postgres'  # Contraseña de la base de datos
db_host = 'udesapostgres.crjvu3vbnafe.us-east-1.rds.amazonaws.com'  # Dirección del host de la base de datos
db_port = '5432'  # Puerto de la base de datos
db_name = 'postgres'  # Nombre de la base de datos

# Crear la URL de conexión a la base de datos
db_url = f'postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}'

# Crear el motor de la base de datos
engine = create_engine(db_url, pool_pre_ping=True, echo=True)

# Crear una clase SessionLocal para la creación de sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para obtener una conexión a la base de datos
def get_db_connection():
    db = SessionLocal()
    return db

# Crea una sesión local
session = SessionLocal()

# Ejemplo de consulta
result = session.execute(text('SELECT * FROM topproduct'))
for row in result:
    print(row)

# Cierra la sesión cuando hayas terminado
session.close()


