import sqlite3
import hashlib

def inicializar_db():
    # Crea el archivo si no existe y se conecta
    conexion = sqlite3.connect("usuarios_gaming.db")
    cursor = conexion.cursor()
    
    # Creamos la tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL
        )
    ''')
    
    conexion.commit()
    conexion.close()
    print("✅ Base de datos lista y conectada.")

# Funciones auxiliares para usar en el Backend
def registrar_usuario_db(nombre, clave):
    clave_segura = hashlib.sha256(clave.encode()).hexdigest()
    try:
        conn = sqlite3.connect("usuarios_gaming.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, clave) VALUES (?, ?)", (nombre, clave_segura))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False # El usuario ya existe

def validar_usuario_db(nombre, clave):
    clave_hasheada = hashlib.sha256(clave.encode()).hexdigest()
    conn = sqlite3.connect("usuarios_gaming.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE nombre = ? AND clave = ?", (nombre, clave_hasheada))
    usuario = cursor.fetchone()
    conn.close()
    return usuario is not None