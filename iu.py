# Importamos las librerías necesarias para que el juego funcione
import tkinter as tk           # esta es la que nos deja hacer ventanas, botones y todo lo visual
from PIL import Image, ImageTk # esta es para cargar y redimensionar las imágenes de los pokemones
import random                  # para todo lo aleatorio, como el equipo del rival
import json                    # para guardar y leer el leaderboard en un archivo
import os                      # para revisar si el archivo del leaderboard ya existe en la compu

# ============================================
# VENTANA PRINCIPAL - EL MENÚ DEL JUEGO
# ============================================

Inicio = tk.Tk()                  # creamos la ventana principal, la primera que aparece
Inicio.title("Pokekirk")          # le ponemos el nombre que aparece arriba de la ventana
Inicio.geometry("1280x720")       # tamaño de la ventana: 1280 ancho x 720 alto en píxeles

# ============================================
# STATS DE TODOS LOS POKEMONES
# Cada pokemon tiene tres valores:
#   hp  = vida (cuánto aguanta antes de caer)
#   atk = ataque (cuánto daño le hace al rival)
#   def = defensa (cuánto reduce el daño que recibe)
# ============================================

POKEMONES_STATS = {
    # --- DEFENSA: estos aguantan muchísimo pero pegan suave ---
    "Aurotitan":  {"hp": 150, "atk": 20, "def": 40},  # mech azul y dorado, el tanque principal
    "Cibernak":   {"hp": 140, "atk": 22, "def": 38},  # monstruo espinoso azul con luces cyan
    "Petroguard": {"hp": 130, "atk": 18, "def": 35},  # reptil rocoso con armadura de metal

    # --- ATAQUE: estos pegan durísimo pero se caen rápido ---
    "Voltombra":  {"hp": 80,  "atk": 65, "def": 15},  # robot negro con rayo azul, muy veloz
    "Lobrak":     {"hp": 75,  "atk": 70, "def": 12},  # lobo gris feroz, el que más daño hace
    "Oxidrax":    {"hp": 85,  "atk": 60, "def": 14},  # robot oxidado con grietas de energía roja

    # --- BALANCEADOS: ni muy fuertes ni muy débiles, buenos en todo ---
    "Violetron":  {"hp": 100, "atk": 35, "def": 25},  # mech morado oscuro con luces púrpura
    "Lunaciervo": {"hp": 95,  "atk": 38, "def": 22},  # criatura blanca elegante con ojos cyan
    "Azuldrake":  {"hp": 105, "atk": 33, "def": 27},  # dragón azul con alas enormes
    "Escamdrax":  {"hp": 100, "atk": 36, "def": 24},  # dragón naranja escamoso con ojos turquesa
}

# ============================================
# CARGAMOS LAS IMÁGENES DE LOS POKEMONES
# Las cargamos una sola vez aquí arriba para no repetir el proceso en cada botón
# IMPORTANTE: los archivos .png tienen que estar en la misma carpeta que este archivo
# ============================================

def cargar_imagen_pokemon(nombre_archivo, tamaño=(80, 80)):
    # intentamos cargar la imagen del pokemon
    try:
        img = Image.open(nombre_archivo).convert("RGBA")  # abrimos el archivo y lo convertimos a RGBA (para transparencia)
        img = img.resize(tamaño, Image.LANCZOS)           # le cambiamos el tamaño al que necesitamos
        return ImageTk.PhotoImage(img)                    # lo convertimos al formato que entiende tkinter
    except:
        return None  # si el archivo no existe o falla, devolvemos None y el botón queda solo con texto

# acá guardamos la imagen de cada pokemon ya cargada y lista para usar en los botones
IMAGENES_POKEMONES = {
    "Aurotitan":  cargar_imagen_pokemon("aurotitan.png"),
    "Cibernak":   cargar_imagen_pokemon("cibernak.png"),
    "Petroguard": cargar_imagen_pokemon("petroguard.png"),
    "Voltombra":  cargar_imagen_pokemon("voltombra.png"),
    "Lobrak":     cargar_imagen_pokemon("lobrak.png"),
    "Oxidrax":    cargar_imagen_pokemon("oxidrax.png"),
    "Violetron":  cargar_imagen_pokemon("violetron.png"),
    "Lunaciervo": cargar_imagen_pokemon("lunaciervo.png"),
    "Azuldrake":  cargar_imagen_pokemon("azuldrake.png"),
    "Escamdrax":  cargar_imagen_pokemon("escamdrax.png"),
}

# ============================================
# CARGAMOS LAS IMÁGENES DE LOS PERSONAJES/AVATARES
# Cada personaje tiene su propia imagen de referencia para mostrarse en la pantalla de selección
# Los archivos deben estar en la misma carpeta que este archivo .py
# ============================================

# nombre del archivo de imagen de cada personaje
IMAGENES_PERSONAJES_ARCHIVOS = {
    "Jeffrey":  "jeffrey.png",   # personaje estilo tribal/urbano con dreads blancos
    "Carlos K": "carlosk.png",   # personaje estilo oscuro/misterioso con sombrero
    "Sean":     "sean.png",      # personaje estilo steampunk con abrigo marrón
}

# ============================================
# VARIABLES GLOBALES DEL JUEGO
# Estas las puede leer y modificar cualquier función del código
# ============================================

coleccion_jugador = []  # lista con todos los pokemones que el jugador va consiguiendo
hp_guardado = {}        # diccionario que guarda cuánta vida le quedó a cada pokemon al terminar una batalla
puntaje_actual = 0      # el puntaje del jugador, empieza en cero

# ============================================
# LEADERBOARD - TABLA DE MEJORES PUNTAJES
# ============================================

ARCHIVO_LB = "leaderboard.json"  # nombre del archivo donde guardamos los puntajes permanentemente
# estos son los rivales ficticios que aparecen en el leaderboard cuando terminás el juego
NOMBRES_RIVALES = ["Gary", "Giovanni", "Misty", "Brock", "Lance", "Sabrina", "Surge", "Erika"]

def cargar_leaderboard():
    # revisamos si el archivo de puntajes ya existe en la compu
    if os.path.exists(ARCHIVO_LB):
        with open(ARCHIVO_LB, "r") as f:
            return json.load(f)  # si existe, lo leemos y devolvemos la lista de puntajes
    return []  # si no existe todavía, devolvemos una lista vacía

def guardar_puntaje(nombre, puntaje):
    datos = cargar_leaderboard()                           # cargamos los puntajes que ya están guardados
    datos.append({"nombre": nombre, "puntaje": puntaje})  # agregamos el nuevo puntaje a la lista
    datos.sort(key=lambda x: x["puntaje"], reverse=True)  # ordenamos de mayor a menor
    with open(ARCHIVO_LB, "w") as f:
        json.dump(datos, f)  # guardamos todo en el archivo (sobreescribe lo anterior)

def abrir_leaderboard():
    lb = tk.Toplevel(Inicio)         # abrimos una ventana nueva encima del menú
    lb.title("Leaderboard")          # título de la ventana
    lb.geometry("600x500")           # tamaño de la ventana

    # texto grande arriba de todo
    tk.Label(lb, text="Mejores Entrenadores", font=("Arial", 24, "bold")).pack(pady=20)

    datos = cargar_leaderboard()  # obtenemos los puntajes guardados
    frame = tk.Frame(lb)          # contenedor invisible para organizar la tabla
    frame.pack(pady=10)

    # primera fila de la tabla con los títulos de cada columna
    tk.Label(frame, text="Posición",   font=("Arial", 14, "bold"), width=10).grid(row=0, column=0, padx=10)
    tk.Label(frame, text="Entrenador", font=("Arial", 14, "bold"), width=20).grid(row=0, column=1, padx=10)
    tk.Label(frame, text="Puntaje",    font=("Arial", 14, "bold"), width=10).grid(row=0, column=2, padx=10)

    if not datos:
        # si no hay puntajes guardados todavía, mostramos este aviso
        tk.Label(lb, text="No hay puntajes aún", font=("Arial", 14), fg="gray").pack(pady=20)
    else:
        for i, entrada in enumerate(datos):  # recorremos cada puntaje con su número de posición
            # el primero va en dorado, el segundo en plateado, los demás en blanco
            color = "gold" if i == 0 else "silver" if i == 1 else "white"
            tk.Label(frame, text=f"#{i+1}",               font=("Arial", 13), bg=color, width=10).grid(row=i+1, column=0, padx=10, pady=5)
            tk.Label(frame, text=entrada["nombre"],        font=("Arial", 13), bg=color, width=20).grid(row=i+1, column=1, padx=10, pady=5)
            tk.Label(frame, text=str(entrada["puntaje"]), font=("Arial", 13), bg=color, width=10).grid(row=i+1, column=2, padx=10, pady=5)

# ============================================
# SISTEMA DE BATALLA
# ============================================

def crear_equipo_rival(mi_coleccion):
    todos = list(POKEMONES_STATS.keys())                        # lista con todos los pokemones del juego
    disponibles = [p for p in todos if p not in mi_coleccion]  # filtramos los que vos no tenés todavía
    tamaño = len(mi_coleccion)                                  # el rival va a tener la misma cantidad de pokemones que vos

    if len(disponibles) >= tamaño:
        return random.sample(disponibles, tamaño)  # elegimos pokemones aleatorios que no sean los tuyos
    else:
        # si no hay suficientes pokemones diferentes, completamos con algunos que ya tienen
        equipo = disponibles.copy()
        resto = [p for p in todos if p not in equipo]
        equipo += random.sample(resto, tamaño - len(equipo))
        return equipo

def calcular_daño(atacante_stats, defensor_stats):
    # fórmula del daño: ataque del atacante menos la mitad de la defensa del defensor
    daño = max(1, atacante_stats["atk"] - (defensor_stats["def"] // 2))
    # le agregamos variación aleatoria de ±20% para que nunca sea exactamente igual
    return random.randint(int(daño * 0.8), int(daño * 1.2))

def abrir_batalla():
    global puntaje_actual, hp_guardado, coleccion_jugador

    batalla = tk.Toplevel(Inicio)      # creamos la ventana de la batalla
    batalla.title("Batalla Pokemon!")  # título de la ventana
    batalla.geometry("1280x720")       # tamaño de la ventana

    # armamos el equipo del jugador usando el hp guardado de la batalla anterior
    # si es la primera batalla, usamos el hp máximo de cada pokemon
    equipo_jugador = {}
    for nombre in coleccion_jugador:
        stats = POKEMONES_STATS[nombre]
        equipo_jugador[nombre] = {
            "hp_actual": hp_guardado.get(nombre, stats["hp"]),  # hp guardado o máximo si es la primera vez
            "hp_max":    stats["hp"],   # vida máxima del pokemon
            "atk":       stats["atk"], # ataque
            "def":       stats["def"]  # defensa
        }

    # armamos el equipo del rival con pokemones aleatorios que vos no tenés
    equipo_rival = {}
    for nombre in crear_equipo_rival(coleccion_jugador):
        stats = POKEMONES_STATS[nombre]
        equipo_rival[nombre] = {
            "hp_actual": stats["hp"],  # el rival siempre empieza con vida completa
            "hp_max":    stats["hp"],
            "atk":       stats["atk"],
            "def":       stats["def"]
        }

    pokemones_derrotados_rival = []  # lista donde vamos guardando los pokemones del rival que derrotamos
    batalla_terminada = [False]      # usamos una lista para poder modificarla dentro de las funciones internas

    # ---- ARMAMOS LA INTERFAZ VISUAL DE LA BATALLA ----

    # barra azul arriba con el título de la batalla
    tk.Label(batalla, text="BATALLA POKEMON!", font=("Arial", 20, "bold"), bg="lightblue").pack(fill="x", pady=10)

    # contenedor que divide la pantalla en tres paneles (rival | log | jugador)
    frame_medio = tk.Frame(batalla)
    frame_medio.pack(fill="both", expand=True)

    # panel izquierdo amarillo donde se ven los pokemones del rival
    frame_rival = tk.Frame(frame_medio, bg="lightyellow")
    frame_rival.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    tk.Label(frame_rival, text="RIVAL", font=("Arial", 16, "bold"), bg="lightyellow").pack()

    # panel central blanco donde aparecen los mensajes de la batalla (el log)
    frame_log = tk.Frame(frame_medio, bg="white")
    frame_log.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    tk.Label(frame_log, text="Log", font=("Arial", 14, "bold")).pack()
    log = tk.Text(frame_log, font=("Arial", 11), state="disabled", wrap="word")  # caja de texto donde van los mensajes
    log.pack(fill="both", expand=True)

    # panel derecho verde donde están los botones de tus pokemones
    frame_jugador = tk.Frame(frame_medio, bg="lightgreen")
    frame_jugador.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    tk.Label(frame_jugador, text="TU EQUIPO", font=("Arial", 16, "bold"), bg="lightgreen").pack()

    # etiqueta que muestra el puntaje actual mientras peleás
    label_puntaje = tk.Label(batalla, text=f"Puntaje: {puntaje_actual}", font=("Arial", 14, "bold"))
    label_puntaje.pack()

    botones_jugador = {}  # diccionario que guarda los botones de tus pokemones para actualizarlos después

    def agregar_log(msg):
        # función para agregar un mensaje al log de batalla
        log.config(state="normal")       # habilitamos la caja para escribir
        log.insert("end", msg + "\n")    # agregamos el mensaje al final
        log.see("end")                   # hacemos scroll automático para ver el último mensaje
        log.config(state="disabled")     # volvemos a deshabilitarla para que el jugador no pueda escribir ahí

    # creamos las etiquetas de HP para cada pokemon del rival en el panel amarillo
    labels_rival = {}
    for nombre in equipo_rival:
        f = tk.Frame(frame_rival, bg="lightyellow")  # mini contenedor por cada pokemon del rival
        f.pack(pady=3, fill="x", padx=5)
        tk.Label(f, text=nombre, font=("Arial", 12), bg="lightyellow", width=12, anchor="w").pack(side="left")  # nombre del pokemon
        lbl = tk.Label(f, text=f"HP: {equipo_rival[nombre]['hp_actual']}/{equipo_rival[nombre]['hp_max']}", font=("Arial", 11), bg="lightyellow")
        lbl.pack(side="left")       # vida actual del pokemon del rival
        labels_rival[nombre] = lbl  # guardamos la referencia para poder actualizarla después

    def actualizar_ui():
        # esta función refresca lo que se ve en pantalla después de cada ataque
        for nombre, lbl in labels_rival.items():
            hp = max(0, equipo_rival[nombre]["hp_actual"])  # nos aseguramos que no muestre hp negativo
            lbl.config(text=f"HP: {hp}/{equipo_rival[nombre]['hp_max']}")  # actualizamos el texto del rival
        for nombre, btn in botones_jugador.items():
            hp = max(0, equipo_jugador[nombre]["hp_actual"])
            hp_max = equipo_jugador[nombre]["hp_max"]
            if hp <= 0:
                btn.config(text=f"{nombre}\nHP: 0/{hp_max}", state="disabled", bg="gray")  # si cayó, lo ponemos gris y lo bloqueamos
            else:
                btn.config(text=f"{nombre}\nHP: {hp}/{hp_max}")  # si sigue vivo, actualizamos su hp

    def verificar_fin():
        global puntaje_actual
        vivos_rival   = [n for n in equipo_rival   if equipo_rival[n]["hp_actual"]   > 0]  # pokemones vivos del rival
        vivos_jugador = [n for n in equipo_jugador if equipo_jugador[n]["hp_actual"] > 0]  # pokemones vivos tuyos

        if not vivos_rival:
            # si el rival no tiene pokemones vivos, ganaste la batalla
            batalla_terminada[0] = True
            puntaje_actual += 50  # sumamos 50 puntos por ganar la batalla
            label_puntaje.config(text=f"Puntaje: {puntaje_actual}")
            agregar_log("¡GANASTE! +50 puntos por victoria")

            for n in equipo_jugador:
                hp_guardado[n] = max(0, equipo_jugador[n]["hp_actual"])  # guardamos el hp que le quedó a cada pokemon tuyo

            for p in pokemones_derrotados_rival:
                if p not in coleccion_jugador:
                    coleccion_jugador.append(p)  # los pokemones derrotados del rival pasan a tu colección

            # esperamos 2 segundos, cerramos la ventana y revisamos si ya ganaste el juego completo
            batalla.after(2000, lambda: [batalla.destroy(), verificar_victoria_juego()])
            return True

        if not vivos_jugador:
            # si vos no tenés pokemones vivos, perdiste la batalla
            batalla_terminada[0] = True
            agregar_log("Perdiste la batalla...")
            for btn in botones_jugador.values():
                btn.config(state="disabled")  # bloqueamos todos tus botones
            tk.Button(batalla, text="Volver al menu", font=("Arial", 14),
                      command=batalla.destroy).pack(pady=10)  # botón para volver al menú
            return True

        return False  # si llegamos acá, la batalla sigue en pie

    def turno_rival():
        # función que maneja el turno del rival
        if batalla_terminada[0]:
            return  # si la batalla ya terminó no hacemos nada

        vivos_rival   = [n for n in equipo_rival   if equipo_rival[n]["hp_actual"]   > 0]
        vivos_jugador = [n for n in equipo_jugador if equipo_jugador[n]["hp_actual"] > 0]

        if not vivos_rival or not vivos_jugador:
            verificar_fin()  # si alguno quedó sin pokemones, verificamos el resultado
            return

        # el rival elige al azar qué pokemon usa y a quién le pega
        atacante = random.choice(vivos_rival)
        objetivo = random.choice(vivos_jugador)
        daño = calcular_daño(equipo_rival[atacante], equipo_jugador[objetivo])
        equipo_jugador[objetivo]["hp_actual"] -= daño  # le restamos el daño al pokemon que recibió el ataque
        agregar_log(f"Rival: {atacante} ataca a {objetivo} por {daño} daño!")

        if equipo_jugador[objetivo]["hp_actual"] <= 0:
            agregar_log(f"{objetivo} fue derrotado!")  # avisamos si el pokemon cayó

        actualizar_ui()  # refrescamos lo que se ve en pantalla
        if not verificar_fin():
            agregar_log("--- Tu turno ---")
            for nombre, btn in botones_jugador.items():
                if equipo_jugador[nombre]["hp_actual"] > 0:
                    btn.config(state="normal")  # volvemos a habilitar tus botones para que puedas atacar

    def atacar_con(nombre_jugador):
        # esta función se activa cuando hacés clic en uno de tus pokemones para atacar
        if batalla_terminada[0]:
            return  # si la batalla ya terminó, no hacemos nada

        # deshabilitamos todos tus botones mientras elegís el objetivo
        for btn in botones_jugador.values():
            btn.config(state="disabled")

        vivos_rival = [n for n in equipo_rival if equipo_rival[n]["hp_actual"] > 0]  # pokemones vivos del rival

        # abrimos una ventanita pequeña para que elijas a quién atacar
        elegir = tk.Toplevel(batalla)
        elegir.title("Elige objetivo")
        elegir.geometry("300x300")
        tk.Label(elegir, text="¿A quién atacas?", font=("Arial", 14)).pack(pady=10)

        def cancelar():
            # si cerrás la ventana con la X sin elegir, volvemos a habilitar tus botones
            elegir.destroy()
            for nombre, btn in botones_jugador.items():
                if equipo_jugador[nombre]["hp_actual"] > 0:
                    btn.config(state="normal")  # re-habilitamos los botones que siguen vivos

        elegir.protocol("WM_DELETE_WINDOW", cancelar)  # asignamos la función cancelar al botón X de la ventanita

        def confirmar(objetivo):
            global puntaje_actual
            elegir.destroy()  # cerramos la ventanita de selección de objetivo
            daño = calcular_daño(equipo_jugador[nombre_jugador], equipo_rival[objetivo])
            equipo_rival[objetivo]["hp_actual"] -= daño  # le restamos el daño al pokemon del rival
            agregar_log(f"Tu {nombre_jugador} ataca a {objetivo} por {daño} daño!")

            if equipo_rival[objetivo]["hp_actual"] <= 0:
                agregar_log(f"{objetivo} fue derrotado!")
                pokemones_derrotados_rival.append(objetivo)  # lo agregamos a la lista de derrotados
                puntaje_actual += 10  # sumamos 10 puntos por derrotar un pokemon
                label_puntaje.config(text=f"Puntaje: {puntaje_actual}")

            actualizar_ui()  # refrescamos la pantalla
            if not verificar_fin():
                agregar_log("--- Turno del rival ---")
                batalla.after(1000, turno_rival)  # esperamos 1 segundo y le damos el turno al rival

        # creamos un botón por cada pokemon vivo del rival para que elijas a quién atacar
        for nombre_rival in vivos_rival:
            hp = equipo_rival[nombre_rival]["hp_actual"]
            hp_max = equipo_rival[nombre_rival]["hp_max"]
            tk.Button(elegir, text=f"{nombre_rival}  HP: {hp}/{hp_max}",
                      font=("Arial", 12), width=25,
                      command=lambda obj=nombre_rival: confirmar(obj)).pack(pady=5)

    # creamos los botones de tus pokemones en el panel verde
    for nombre in equipo_jugador:
        hp = equipo_jugador[nombre]["hp_actual"]
        hp_max = equipo_jugador[nombre]["hp_max"]
        img = IMAGENES_POKEMONES.get(nombre)  # obtenemos la imagen del pokemon si existe

        # creamos el botón con o sin imagen dependiendo de si se cargó bien
        if img:
            btn = tk.Button(frame_jugador,
                            text=f"{nombre}\nHP: {hp}/{hp_max}",
                            image=img, compound="top",  # imagen arriba, texto abajo
                            font=("Arial", 11), width=100,
                            command=lambda n=nombre: atacar_con(n))
            btn.image = img  # guardamos la referencia para que Python no borre la imagen
        else:
            btn = tk.Button(frame_jugador,
                            text=f"{nombre}\nHP: {hp}/{hp_max}",
                            font=("Arial", 12), width=15, height=3,
                            command=lambda n=nombre: atacar_con(n))

        btn.pack(pady=5, padx=5)
        botones_jugador[nombre] = btn  # guardamos el botón en el diccionario para poder actualizarlo
        if hp <= 0:
            btn.config(state="disabled", bg="gray")  # si ya está caído, lo bloqueamos desde el inicio

    agregar_log("¡La batalla comienza! Es tu turno.")  # primer mensaje del log

# ============================================
# VERIFICAMOS SI EL JUGADOR GANÓ EL JUEGO COMPLETO
# ============================================

def verificar_victoria_juego():
    todos = list(POKEMONES_STATS.keys())  # lista con todos los pokemones que existen en el juego
    if all(p in coleccion_jugador for p in todos):
        abrir_pantalla_ganaste()  # si tenés todos, ganaste el juego
    else:
        faltantes = [p for p in todos if p not in coleccion_jugador]  # los que todavía te faltan
        abrir_entre_batallas(faltantes)  # mostramos cuáles faltan y seguimos jugando

def abrir_entre_batallas(faltantes):
    # ventana que aparece entre batallas mostrando el progreso del jugador
    ventana = tk.Toplevel(Inicio)
    ventana.title("Resultado")
    ventana.geometry("600x400")

    tk.Label(ventana, text="¡Batalla ganada!", font=("Arial", 22, "bold"), fg="green").pack(pady=20)
    tk.Label(ventana, text=f"Tu colección: {', '.join(coleccion_jugador)}", font=("Arial", 12), wraplength=500).pack(pady=10)
    tk.Label(ventana, text=f"Te faltan: {', '.join(faltantes)}", font=("Arial", 12), fg="red", wraplength=500).pack(pady=10)
    tk.Label(ventana, text=f"Puntaje actual: {puntaje_actual}", font=("Arial", 14, "bold")).pack(pady=10)

    # botón para ir a la siguiente batalla
    tk.Button(ventana, text="Siguiente batalla",
              font=("Arial", 16), bg="blue", fg="white",
              command=lambda: [ventana.destroy(), abrir_batalla()]).pack(pady=20)

def abrir_pantalla_ganaste():
    # pantalla final cuando el jugador consiguió todos los pokemones
    global puntaje_actual

    fin = tk.Toplevel(Inicio)
    fin.title("¡Ganaste!")
    fin.geometry("600x500")

    tk.Label(fin, text="¡ERES EL MEJOR ENTRENADOR!", font=("Arial", 22, "bold"), fg="gold").pack(pady=20)
    tk.Label(fin, text=f"Puntaje final: {puntaje_actual}", font=("Arial", 18)).pack(pady=10)

    nombre_var = tk.StringVar()  # variable que guarda lo que el jugador escribe
    tk.Label(fin, text="Ingresa tu nombre:", font=("Arial", 14)).pack(pady=10)
    tk.Entry(fin, textvariable=nombre_var, font=("Arial", 14)).pack(pady=5)  # caja de texto para escribir el nombre

    def guardar_y_salir():
        nombre = nombre_var.get().strip()  # obtenemos el nombre y quitamos espacios sobrantes
        if not nombre:
            nombre = "Entrenador"  # si no escribió nada, usamos este nombre por defecto

        guardar_puntaje(nombre, puntaje_actual)  # guardamos el puntaje del jugador

        # agregamos los rivales ficticios al leaderboard si todavía no están guardados
        datos_existentes = cargar_leaderboard()
        nombres_ya_guardados = [d["nombre"] for d in datos_existentes]

        for rival in NOMBRES_RIVALES:
            if rival not in nombres_ya_guardados:
                # le asignamos un puntaje aleatorio siempre menor al del jugador
                puntaje_rival = random.randint(10, max(10, puntaje_actual - 10))
                guardar_puntaje(rival, puntaje_rival)

        fin.destroy()        # cerramos la ventana de ganaste
        abrir_leaderboard()  # abrimos el leaderboard con todos los puntajes

    tk.Button(fin, text="Guardar puntaje", font=("Arial", 14), bg="green", fg="white",
              command=guardar_y_salir).pack(pady=20)

# ============================================
# SELECCIÓN DE PERSONAJE Y POKEMONES
# ============================================

personaje_elegido = None  # guarda el personaje que el jugador elige, empieza vacío
pokemones_elegidos = []   # guarda los 3 pokemones iniciales que el jugador elige

def abrir_seleccion():
    Inicio.withdraw()  # escondemos el menú principal mientras el jugador elige
    seleccion = tk.Toplevel(Inicio)   # abrimos la ventana de selección
    seleccion.title("seleccion")      # título de la ventana
    seleccion.geometry("1280x720")    # tamaño de la ventana

    # texto de bienvenida arriba de todo
    tk.Label(seleccion, text="Bienvenido! escoge tu personaje y tus pokemones", font=("Arial", 20)).pack(pady=20)

    personajes = ["Jeffrey", "Carlos K", "Sean"]  # los tres personajes disponibles para elegir

    # ============================================
    # CARGAMOS LAS IMÁGENES DE REFERENCIA DE CADA PERSONAJE
    # Las redimensionamos a 200x300 píxeles para que quepan bien en los botones
    # ============================================
    imagenes_avatares = {}
    for nombre_personaje, archivo in IMAGENES_PERSONAJES_ARCHIVOS.items():
        img = cargar_imagen_pokemon(archivo, tamaño=(200, 300))  # usamos la misma función pero con tamaño más grande
        imagenes_avatares[nombre_personaje] = img

    def elegir_personaje(nombre, botones):
        global personaje_elegido
        personaje_elegido = nombre  # guardamos el personaje que el jugador eligió
        for b in botones:
            b.config(relief="raised", bg="SystemButtonFace")  # reseteamos todos los botones al color normal
        botones[personajes.index(nombre)].config(relief="sunken", bg="lightblue")  # resaltamos el elegido en azul

    frame_personajes = tk.Frame(seleccion)  # contenedor invisible para organizar los botones de personajes
    frame_personajes.pack(pady=20)

    botones_personaje = []  # lista donde vamos a guardar los botones
    for p in personajes:
        img_avatar = imagenes_avatares.get(p)  # obtenemos la imagen de referencia del personaje

        if img_avatar:
            # si tenemos imagen, la mostramos dentro del botón con el nombre abajo
            b = tk.Button(
                frame_personajes,
                text=p,
                image=img_avatar,
                compound="top",    # imagen arriba, nombre abajo
                font=("Arial", 14, "bold"),
                width=200
            )
            b.image = img_avatar  # guardamos la referencia para que Python no elimine la imagen de memoria
        else:
            # si no se encontró la imagen, mostramos solo el nombre en un botón grande
            b = tk.Button(frame_personajes, text=p, font=("Arial", 16), width=15, height=8)

        b.pack(side="left", padx=20)   # los ponemos uno al lado del otro con espacio entre ellos
        botones_personaje.append(b)    # lo agregamos a la lista

    for b in botones_personaje:
        nombre = b.cget("text")  # obtenemos el nombre que tiene el botón
        # le asignamos la función elegir_personaje cuando hagan clic
        # usamos lambda para poder pasarle el nombre como parámetro
        b.config(command=lambda n=nombre: elegir_personaje(n, botones_personaje))

    def ir_a_pokemones():
        if not personaje_elegido:
            tk.Label(seleccion, text="¡Elige un personaje primero!", fg="red").pack()  # mensaje de error en rojo
            return  # paramos la función acá si no eligieron personaje
        seleccion.withdraw()       # escondemos esta ventana
        abrir_pokemones(seleccion) # abrimos la ventana de pokemones

    # botón para pasar a la siguiente pantalla
    tk.Button(seleccion, text="Siguiente →", font=("Arial", 16), command=ir_a_pokemones).pack(pady=30)

def abrir_pokemones(ventana_anterior):
    Poke = tk.Toplevel(Inicio)         # abrimos la ventana de selección de pokemones
    Poke.title("Elige tus Pokémon")    # título de la ventana
    Poke.geometry("1280x720")          # tamaño de la ventana

    tk.Label(Poke, text="Elige 3 Pokémon:", font=("Arial", 24)).pack(pady=20)  # instrucción arriba

    # lista con todos los pokemones disponibles para elegir
    pokemones = list(POKEMONES_STATS.keys())

    frame_poke = tk.Frame(Poke)  # contenedor invisible para la grilla de botones
    frame_poke.pack(pady=10)

    # texto que muestra cuántos pokemones lleva elegidos el jugador
    label_info = tk.Label(Poke, text="Seleccionados: 0/3", font=("Arial", 14))
    label_info.pack(pady=10)

    botones_poke = []  # lista donde guardamos los botones de pokemones

    def elegir_pokemon(nombre, boton):
        global pokemones_elegidos
        if nombre in pokemones_elegidos:
            pokemones_elegidos.remove(nombre)                       # si ya estaba elegido, lo quitamos
            boton.config(bg="SystemButtonFace", relief="raised")    # lo regresamos al color normal
        elif len(pokemones_elegidos) < 3:
            pokemones_elegidos.append(nombre)                       # si hay menos de 3, lo agregamos
            boton.config(bg="lightgreen", relief="sunken")          # lo ponemos verde y hundido

        for b in botones_poke:
            n = b.cget("text")  # obtenemos el nombre de cada botón
            if n not in pokemones_elegidos and len(pokemones_elegidos) >= 3:
                b.config(state="disabled")  # bloqueamos los que no fueron elegidos cuando ya hay 3
            else:
                b.config(state="normal")    # los dejamos disponibles si todavía se puede elegir

        label_info.config(text=f"Seleccionados: {len(pokemones_elegidos)}/3")  # actualizamos el contador

    # creamos los botones en una grilla de 5 columnas x 2 filas
    for i, p in enumerate(pokemones):
        img = IMAGENES_POKEMONES.get(p)  # obtenemos la imagen del pokemon

        if img:
            # si tiene imagen, la mostramos arriba y el nombre abajo
            b = tk.Button(frame_poke, text=p, image=img, compound="top",
                          font=("Arial", 11), width=100)
            b.image = img  # guardamos la referencia para que Python no borre la imagen
        else:
            # si no tiene imagen, solo mostramos el nombre
            b = tk.Button(frame_poke, text=p, font=("Arial", 14), width=12, height=3)

        b.grid(row=i//5, column=i%5, padx=10, pady=10)  # lo colocamos en la grilla (fila y columna calculadas automáticamente)
        botones_poke.append(b)  # lo agregamos a la lista

    for b in botones_poke:
        nombre = b.cget("text")  # obtenemos el nombre del pokemon del botón
        b.config(command=lambda n=nombre, btn=b: elegir_pokemon(n, btn))  # asignamos la función de elegir

    def ir_a_juego():
        if len(pokemones_elegidos) < 3:
            tk.Label(Poke, text="¡Elige 3 Pokémon primero!", fg="red").pack()  # error si eligieron menos de 3
            return
        Poke.withdraw()  # escondemos esta ventana
        abrir_juego()    # arrancamos el juego

    # botón verde para comenzar el juego
    tk.Button(Poke, text="¡Comenzar!", font=("Arial", 16), bg="green", fg="white",
              command=ir_a_juego).pack(pady=20)

def abrir_juego():
    global coleccion_jugador
    coleccion_jugador = pokemones_elegidos.copy()  # la colección inicial son los 3 pokemones que elegiste
    abrir_batalla()                                # arrancamos la primera batalla

def abrir_creditos():
    Inicio.withdraw()  # escondemos el menú principal
    creditos = tk.Toplevel(Inicio)      # abrimos la ventana de créditos
    creditos.title("Creditos")          # título
    creditos.geometry("1280x720")       # tamaño
    tk.Label(creditos, text="Todo gracias a Luis", font=("Arial", 20)).pack(pady=20)  # texto de créditos

# ============================================
# MENÚ PRINCIPAL - LO QUE VE EL JUGADOR AL ABRIR EL JUEGO
# ============================================

fotoinicio   = tk.PhotoImage(file="Iniciar.png")   # cargamos la imagen del botón de inicio
fotocreditos = tk.PhotoImage(file="Creditos.png")  # cargamos la imagen del botón de créditos

# botón de inicio del juego con su imagen
boton = tk.Button(Inicio, image=fotoinicio, command=abrir_seleccion, bg="yellow", fg="red")
boton.pack(pady=10)

# botón de créditos con su imagen
boton2 = tk.Button(Inicio, image=fotocreditos, command=abrir_creditos, bg="yellow", fg="red")
boton2.pack(pady=0)

# botón del leaderboard con texto y emoji
boton_lb = tk.Button(Inicio, text="🏆 Leaderboard", font=("Arial", 14), command=abrir_leaderboard)
boton_lb.pack(pady=10)

Inicio.mainloop()  # esta línea mantiene la ventana abierta y escuchando lo que hace el usuario