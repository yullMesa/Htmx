from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import inicializar_db, registrar_usuario_db, validar_usuario_db

app = FastAPI()

# Inicializa la DB al arrancar el servidor
@app.on_event("startup")
def startup_event():
    inicializar_db()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="../Frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(usuario: str = Form(...), clave: str = Form(...)):
    # Usamos la función de database.py para validar
    if validar_usuario_db(usuario, clave):
        # HX-Redirect le dice a HTMX que cambie de página
        return Response(headers={"HX-Redirect": "/dashboard"}) 
    
    return '<span style="color: #ff4444; font-weight: bold;">❌ Error: Usuario o clave incorrectos</span>'

@app.post("/register")
async def register(usuario: str = Form(...), clave: str = Form(...)):
    # Usamos la función de database.py para registrar
    exito = registrar_usuario_db(usuario, clave)
    
    if exito:
        return '<span style="color: #00ff00; font-weight: bold;">✅ ¡Registrado! Ya puedes iniciar sesión.</span>'
    else:
        return f'<span style="color: #ffbb33; font-weight: bold;">⚠️ El usuario "{usuario}" ya existe</span>'
    
@app.get("/dashboard")
async def dashboard():
    return "¡Bienvenido al área secreta de Gaming Tool! (Página en blanco por ahora)"