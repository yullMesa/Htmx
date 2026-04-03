from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import inicializar_db, registrar_usuario_db, validar_usuario_db
import asyncio # Necesitas esto arriba

app = FastAPI()

# Inicializa la DB al arrancar el servidor
@app.on_event("startup")
def startup_event():
    inicializar_db()

templates = Jinja2Templates(directory="../Frontend")
app.mount("/static", StaticFiles(directory="../Frontend"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/login")
async def login(usuario: str = Form(...), clave: str = Form(...)):
    # Usamos la función de database.py para validar
    if validar_usuario_db(usuario, clave):
        # HX-Redirect le dice a HTMX que cambie de página
        return Response(headers={"HX-Redirect": "/Game"}) 
    
    return '<span style="color: #ff4444; font-weight: bold;">❌ Error: Usuario o clave incorrectos</span>'

@app.post("/register")
async def register(usuario: str = Form(...), clave: str = Form(...)):
    # Usamos la función de database.py para registrar
    exito = registrar_usuario_db(usuario, clave)
    
    if exito:
        return '<span style="color: #00ff00; font-weight: bold;">✅ ¡Registrado! Ya puedes iniciar sesión.</span>'
    else:
        return f'<span style="color: #ffbb33; font-weight: bold;">⚠️ El usuario "{usuario}" ya existe</span>'
    
@app.get("/Game")
async def game(request: Request):
    return templates.TemplateResponse("Game.html", {"request": request})

# Lista de contenido (esto es lo que manejará las 200 páginas)
escenas_prologo = [
    {"img": "ventana.png", "txt": "El silencio dominaba la noche .."},
    {"img": "toctoc.png", "txt": ".... De repente mi madre empezo a tocar la puerta."},
    {"img": "madre.png", "txt": "Mi madre entro en la habitación."},
    {"img": "madre-favor.png", "txt": "Pidiendome el favor de ir por mi padre que no habia aparecido en todo el día."},
    {"img": "corriendo.png", "txt": "Sali apurado buscando a mi padre en los tipicos lugares donde se mantenia."},
    {"img": "carnicero.png", "txt": "Lamentablemente la única persona que lo vio , dijo que estaba en la taberna Gaming Tool el peor lugar donde perder tu dinero."},
    {"img": "taberna.png", "txt": "Asustado , no me quedaba de otra de  ir y preguntar por él."},
    {"img": "Hablar.png", "txt": "El bartender me dijo que se lo habian llevado ya que se quedo con el dinero de un magnate millonario."},
    {"img": "cartas.png", "txt": "¿Enserio?, pero estas cartas no tienen mucho valor solo sirven para comprar lo basico"},
    {"img": "explicacion.png", "txt": "Sí , pero las cartas raran te dan poder en esta sociedad no esas comunes. !Te muestro!."}

]



@app.get("/escena/{indice}", response_class=HTMLResponse)
async def obtener_escena(indice: int):
    if 0 <= indice < len(escenas_prologo):
        escena = escenas_prologo[indice]
        siguiente = indice + 1
        
        # RUTA CONSTRUIDA: /static/ + Ink/Prologo/ + nombre.png
        return f"""
            <div id="game-content" class="fade-in">
                <div class="marco-steampunk">
                    <img src="/static/Style/Ink/Prologo/{escena['img']}" 
                        class="comic-img">
                </div>
                
                <div class="interfaz-inferior">
                    <p class="comic-text">{escena['txt']}</p>
                    
                    <button class="btn-next" 
                            hx-get="/escena/{siguiente}" 
                            hx-target="#game-content" 
                            hx-swap="outerHTML">
                        SIGUIENTE
                    </button>
                </div>
            </div>
            """
    return """
    <div id="game-content" class="interface-steampunk fade-in">
        <h2 class="titulo-sistema">MECANISMO INICIALIZADO</h2>
        <p class="comic-text">El prólogo ha terminado. ¿Deseas entrar al panel de control?</p>
        
        <button class="btn-next" 
                hx-get="/interfaz-juego" 
                hx-target="#game-content" 
                hx-swap="outerHTML">
            -- INICIAR GAMING TOOL --
        </button>
    </div>
    """

@app.get("/interfaz-juego", response_class=HTMLResponse)
async def interfaz_juego(request: Request):
    # Aquí puedes devolver un template completo o un HTML gigante
    # Se cargará dentro del mismo index/game.html sin recargar
    return templates.TemplateResponse("InterfazPrincipal.html", {"request": request})
