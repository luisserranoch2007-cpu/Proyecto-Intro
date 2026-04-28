import tkinter as tk
import random
import json
import os

# Abrir el menu del juego
Inicio = tk.Tk()
Inicio.title("Pokekirk")
Inicio.geometry("1280x720")

# ============================================
# STATS DE TODOS LOS POKEMONES
# ============================================

POKEMONES_STATS = {
    # DEFENSA (mucha vida y defensa, poco ataque)
    "Snorlax":    {"hp": 150, "atk": 20, "def": 40},
    "Squirtle":   {"hp": 140, "atk": 22, "def": 38},
    "Jigglypuff": {"hp": 130, "atk": 18, "def": 35},
    # ATAQUE (mucho daño, poca vida y defensa)
    "Charmander": {"hp": 80,  "atk": 65, "def": 15},
    "Gengar":     {"hp": 75,  "atk": 70, "def": 12},
    "Pikachu":    {"hp": 85,  "atk": 60, "def": 14},
    # BALANCEADOS
    "Bulbasaur":  {"hp": 100, "atk": 35, "def": 25},
    "Meowth":     {"hp": 95,  "atk": 38, "def": 22},
    "Psyduck":    {"hp": 105, "atk": 33, "def": 27},
    "Eevee":      {"hp": 100, "atk": 36, "def": 24},
}

# ============================================
# VARIABLES GLOBALES DEL JUEGO
# ============================================

coleccion_jugador = []  # todos los pokemones que tiene el jugador
hp_guardado = {}        # hp que le quedó a cada pokemon tras la batalla
puntaje_actual = 0      # puntaje acumulado

# ============================================
# LEADERBOARD
# ============================================

ARCHIVO_LB = "leaderboard.json"
NOMBRES_RIVALES = ["Gary", "Giovanni", "Misty", "Brock", "Lance", "Sabrina", "Surge", "Erika"]

def cargar_leaderboard():
    # si el archivo existe lo carga, si no devuelve lista vacía
    if os.path.exists(ARCHIVO_LB):
        with open(ARCHIVO_LB, "r") as f:
            return json.load(f)
    return []

def guardar_puntaje(nombre, puntaje):
    datos = cargar_leaderboard()
    datos.append({"nombre": nombre, "puntaje": puntaje})
    datos.sort(key=lambda x: x["puntaje"], reverse=True)  # ordena de mayor a menor
    with open(ARCHIVO_LB, "w") as f:
        json.dump(datos, f)

def abrir_leaderboard():
    lb = tk.Toplevel(Inicio)
    lb.title("Leaderboard")
    lb.geometry("600x500")

    tk.Label(lb, text="Mejores Entrenadores", font=("Arial", 24, "bold")).pack(pady=20)

    datos = cargar_leaderboard()
    frame = tk.Frame(lb)
    frame.pack(pady=10)

    # encabezados de la tabla
    tk.Label(frame, text="Posición",   font=("Arial", 14, "bold"), width=10).grid(row=0, column=0, padx=10)
    tk.Label(frame, text="Entrenador", font=("Arial", 14, "bold"), width=20).grid(row=0, column=1, padx=10)
    tk.Label(frame, text="Puntaje",    font=("Arial", 14, "bold"), width=10).grid(row=0, column=2, padx=10)

    if not datos:
        tk.Label(lb, text="No hay puntajes aún", font=("Arial", 14), fg="gray").pack(pady=20)
    else:
        for i, entrada in enumerate(datos):
            color = "gold" if i == 0 else "silver" if i == 1 else "white"
            tk.Label(frame, text=f"#{i+1}",               font=("Arial", 13), bg=color, width=10).grid(row=i+1, column=0, padx=10, pady=5)
            tk.Label(frame, text=entrada["nombre"],        font=("Arial", 13), bg=color, width=20).grid(row=i+1, column=1, padx=10, pady=5)
            tk.Label(frame, text=str(entrada["puntaje"]), font=("Arial", 13), bg=color, width=10).grid(row=i+1, column=2, padx=10, pady=5)

# ============================================
# SISTEMA DE BATALLA
# ============================================

def crear_equipo_rival(mi_coleccion):
    todos = list(POKEMONES_STATS.keys())
    disponibles = [p for p in todos if p not in mi_coleccion]
    tamaño = len(mi_coleccion)

    if len(disponibles) >= tamaño:
        return random.sample(disponibles, tamaño)
    else:
        equipo = disponibles.copy()
        resto = [p for p in todos if p not in equipo]
        equipo += random.sample(resto, tamaño - len(equipo))
        return equipo

def calcular_daño(atacante_stats, defensor_stats):
    daño = max(1, atacante_stats["atk"] - (defensor_stats["def"] // 2))
    return random.randint(int(daño * 0.8), int(daño * 1.2))

def abrir_batalla():
    global puntaje_actual, hp_guardado, coleccion_jugador

    batalla = tk.Toplevel(Inicio)
    batalla.title("Batalla Pokemon!")
    batalla.geometry("1280x720")

    # construir equipo jugador con hp guardado o hp máximo
    equipo_jugador = {}
    for nombre in coleccion_jugador:
        stats = POKEMONES_STATS[nombre]
        equipo_jugador[nombre] = {
            "hp_actual": hp_guardado.get(nombre, stats["hp"]),
            "hp_max":    stats["hp"],
            "atk":       stats["atk"],
            "def":       stats["def"]
        }

    # construir equipo rival
    equipo_rival = {}
    for nombre in crear_equipo_rival(coleccion_jugador):
        stats = POKEMONES_STATS[nombre]
        equipo_rival[nombre] = {
            "hp_actual": stats["hp"],
            "hp_max":    stats["hp"],
            "atk":       stats["atk"],
            "def":       stats["def"]
        }

    pokemones_derrotados_rival = []
    batalla_terminada = [False]

    # ---- INTERFAZ ----
    tk.Label(batalla, text="BATALLA POKEMON!", font=("Arial", 20, "bold"), bg="lightblue").pack(fill="x", pady=10)

    frame_medio = tk.Frame(batalla)
    frame_medio.pack(fill="both", expand=True)

    # panel rival
    frame_rival = tk.Frame(frame_medio, bg="lightyellow")
    frame_rival.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    tk.Label(frame_rival, text="RIVAL", font=("Arial", 16, "bold"), bg="lightyellow").pack()

    # log de batalla
    frame_log = tk.Frame(frame_medio, bg="white")
    frame_log.pack(side="left", fill="both", expand=True, padx=10, pady=10)
    tk.Label(frame_log, text="Log", font=("Arial", 14, "bold")).pack()
    log = tk.Text(frame_log, font=("Arial", 11), state="disabled", wrap="word")
    log.pack(fill="both", expand=True)

    # panel jugador
    frame_jugador = tk.Frame(frame_medio, bg="lightgreen")
    frame_jugador.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    tk.Label(frame_jugador, text="TU EQUIPO", font=("Arial", 16, "bold"), bg="lightgreen").pack()

    label_puntaje = tk.Label(batalla, text=f"Puntaje: {puntaje_actual}", font=("Arial", 14, "bold"))
    label_puntaje.pack()

    botones_jugador = {}

    def agregar_log(msg):
        log.config(state="normal")
        log.insert("end", msg + "\n")
        log.see("end")
        log.config(state="disabled")

    # labels de HP del rival
    labels_rival = {}
    for nombre in equipo_rival:
        f = tk.Frame(frame_rival, bg="lightyellow")
        f.pack(pady=3, fill="x", padx=5)
        tk.Label(f, text=nombre, font=("Arial", 12), bg="lightyellow", width=12, anchor="w").pack(side="left")
        lbl = tk.Label(f, text=f"HP: {equipo_rival[nombre]['hp_actual']}/{equipo_rival[nombre]['hp_max']}", font=("Arial", 11), bg="lightyellow")
        lbl.pack(side="left")
        labels_rival[nombre] = lbl

    def actualizar_ui():
        for nombre, lbl in labels_rival.items():
            hp = max(0, equipo_rival[nombre]["hp_actual"])
            lbl.config(text=f"HP: {hp}/{equipo_rival[nombre]['hp_max']}")
        for nombre, btn in botones_jugador.items():
            hp = max(0, equipo_jugador[nombre]["hp_actual"])
            hp_max = equipo_jugador[nombre]["hp_max"]
            if hp <= 0:
                btn.config(text=f"{nombre}\nHP: 0/{hp_max}", state="disabled", bg="gray")
            else:
                btn.config(text=f"{nombre}\nHP: {hp}/{hp_max}")

    def verificar_fin():
        global puntaje_actual
        vivos_rival   = [n for n in equipo_rival   if equipo_rival[n]["hp_actual"]   > 0]
        vivos_jugador = [n for n in equipo_jugador if equipo_jugador[n]["hp_actual"] > 0]

        if not vivos_rival:
            batalla_terminada[0] = True
            puntaje_actual += 50
            label_puntaje.config(text=f"Puntaje: {puntaje_actual}")
            agregar_log("¡GANASTE! +50 puntos por victoria")

            for n in equipo_jugador:
                hp_guardado[n] = max(0, equipo_jugador[n]["hp_actual"])

            for p in pokemones_derrotados_rival:
                if p not in coleccion_jugador:
                    coleccion_jugador.append(p)

            batalla.after(2000, lambda: [batalla.destroy(), verificar_victoria_juego()])
            return True

        if not vivos_jugador:
            batalla_terminada[0] = True
            agregar_log("Perdiste la batalla...")
            for btn in botones_jugador.values():
                btn.config(state="disabled")
            tk.Button(batalla, text="Volver al menu", font=("Arial", 14),
                      command=batalla.destroy).pack(pady=10)
            return True

        return False

    def turno_rival():
        if batalla_terminada[0]:
            return
        vivos_rival   = [n for n in equipo_rival   if equipo_rival[n]["hp_actual"]   > 0]
        vivos_jugador = [n for n in equipo_jugador if equipo_jugador[n]["hp_actual"] > 0]

        if not vivos_rival or not vivos_jugador:
            verificar_fin()
            return

        atacante = random.choice(vivos_rival)
        objetivo = random.choice(vivos_jugador)
        daño = calcular_daño(equipo_rival[atacante], equipo_jugador[objetivo])
        equipo_jugador[objetivo]["hp_actual"] -= daño
        agregar_log(f"Rival: {atacante} ataca a {objetivo} por {daño} daño!")

        if equipo_jugador[objetivo]["hp_actual"] <= 0:
            agregar_log(f"{objetivo} fue derrotado!")

        actualizar_ui()
        if not verificar_fin():
            agregar_log("--- Tu turno ---")
            for nombre, btn in botones_jugador.items():
                if equipo_jugador[nombre]["hp_actual"] > 0:
                    btn.config(state="normal")

    # ← ATACAR_CON AHORA ESTÁ ADENTRO DE ABRIR_BATALLA (esto era el bug principal)
    def atacar_con(nombre_jugador):
        if batalla_terminada[0]:
            return

        for btn in botones_jugador.values():
            btn.config(state="disabled")

        vivos_rival = [n for n in equipo_rival if equipo_rival[n]["hp_actual"] > 0]

        elegir = tk.Toplevel(batalla)
        elegir.title("Elige objetivo")
        elegir.geometry("300x300")
        tk.Label(elegir, text="¿A quién atacas?", font=("Arial", 14)).pack(pady=10)

        def cancelar():
            # re-habilita los botones si cierra con X
            elegir.destroy()
            for nombre, btn in botones_jugador.items():
                if equipo_jugador[nombre]["hp_actual"] > 0:
                    btn.config(state="normal")

        elegir.protocol("WM_DELETE_WINDOW", cancelar)  # arregla el bug de cerrar con X

        def confirmar(objetivo):
            global puntaje_actual
            elegir.destroy()
            daño = calcular_daño(equipo_jugador[nombre_jugador], equipo_rival[objetivo])
            equipo_rival[objetivo]["hp_actual"] -= daño
            agregar_log(f"Tu {nombre_jugador} ataca a {objetivo} por {daño} daño!")

            if equipo_rival[objetivo]["hp_actual"] <= 0:
                agregar_log(f"{objetivo} fue derrotado!")
                pokemones_derrotados_rival.append(objetivo)
                puntaje_actual += 10
                label_puntaje.config(text=f"Puntaje: {puntaje_actual}")

            actualizar_ui()
            if not verificar_fin():
                agregar_log("--- Turno del rival ---")
                batalla.after(1000, turno_rival)

        for nombre_rival in vivos_rival:
            hp = equipo_rival[nombre_rival]["hp_actual"]
            hp_max = equipo_rival[nombre_rival]["hp_max"]
            tk.Button(elegir, text=f"{nombre_rival}  HP: {hp}/{hp_max}",
                      font=("Arial", 12), width=25,
                      command=lambda obj=nombre_rival: confirmar(obj)).pack(pady=5)

    # crear botones del jugador
    for nombre in equipo_jugador:
        hp = equipo_jugador[nombre]["hp_actual"]
        hp_max = equipo_jugador[nombre]["hp_max"]
        btn = tk.Button(frame_jugador,
                        text=f"{nombre}\nHP: {hp}/{hp_max}",
                        font=("Arial", 12), width=15, height=3,
                        command=lambda n=nombre: atacar_con(n))
        btn.pack(pady=5, padx=5)
        botones_jugador[nombre] = btn
        if hp <= 0:
            btn.config(state="disabled", bg="gray")

    agregar_log("¡La batalla comienza! Es tu turno.")

# ============================================
# VERIFICAR SI EL JUEGO TERMINÓ
# ============================================

def verificar_victoria_juego():
    todos = list(POKEMONES_STATS.keys())
    if all(p in coleccion_jugador for p in todos):
        abrir_pantalla_ganaste()
    else:
        faltantes = [p for p in todos if p not in coleccion_jugador]
        abrir_entre_batallas(faltantes)

def abrir_entre_batallas(faltantes):
    ventana = tk.Toplevel(Inicio)
    ventana.title("Resultado")
    ventana.geometry("600x400")

    tk.Label(ventana, text="¡Batalla ganada!", font=("Arial", 22, "bold"), fg="green").pack(pady=20)
    tk.Label(ventana, text=f"Tu colección: {', '.join(coleccion_jugador)}", font=("Arial", 12), wraplength=500).pack(pady=10)
    tk.Label(ventana, text=f"Te faltan: {', '.join(faltantes)}", font=("Arial", 12), fg="red", wraplength=500).pack(pady=10)
    tk.Label(ventana, text=f"Puntaje actual: {puntaje_actual}", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Button(ventana, text="Siguiente batalla",
              font=("Arial", 16), bg="blue", fg="white",
              command=lambda: [ventana.destroy(), abrir_batalla()]).pack(pady=20)

def abrir_pantalla_ganaste():
    global puntaje_actual

    fin = tk.Toplevel(Inicio)
    fin.title("¡Ganaste!")
    fin.geometry("600x500")

    tk.Label(fin, text="¡ERES EL MEJOR ENTRENADOR!", font=("Arial", 22, "bold"), fg="gold").pack(pady=20)
    tk.Label(fin, text=f"Puntaje final: {puntaje_actual}", font=("Arial", 18)).pack(pady=10)

    nombre_var = tk.StringVar()
    tk.Label(fin, text="Ingresa tu nombre:", font=("Arial", 14)).pack(pady=10)
    tk.Entry(fin, textvariable=nombre_var, font=("Arial", 14)).pack(pady=5)

    def guardar_y_salir():
        nombre = nombre_var.get().strip()
        if not nombre:
            nombre = "Entrenador"

        guardar_puntaje(nombre, puntaje_actual)

        # agrega rivales con puntajes menores al del jugador
        datos_existentes = cargar_leaderboard()
        nombres_ya_guardados = [d["nombre"] for d in datos_existentes]

        for rival in NOMBRES_RIVALES:
            if rival not in nombres_ya_guardados:
                puntaje_rival = random.randint(10, max(10, puntaje_actual - 10))
                guardar_puntaje(rival, puntaje_rival)

        fin.destroy()
        abrir_leaderboard()

    tk.Button(fin, text="Guardar puntaje", font=("Arial", 14), bg="green", fg="white",
              command=guardar_y_salir).pack(pady=20)

# ============================================
# SELECCIÓN DE PERSONAJE Y POKEMONES
# ============================================

personaje_elegido = None
pokemones_elegidos = []

def abrir_seleccion():
    Inicio.withdraw()
    seleccion = tk.Toplevel(Inicio)
    seleccion.title("seleccion")
    seleccion.geometry("1280x720")
    tk.Label(seleccion, text="Bienvenido! escoge tu personaje y tus pokemones", font=("Arial", 20)).pack(pady=20)

    personajes = ["Jeffrey", "Carlos K", "Sean"]

    def elegir_personaje(nombre, botones):
        global personaje_elegido
        personaje_elegido = nombre
        for b in botones:
            b.config(relief="raised", bg="SystemButtonFace")
        botones[personajes.index(nombre)].config(relief="sunken", bg="lightblue")

    frame_personajes = tk.Frame(seleccion)
    frame_personajes.pack(pady=20)

    botones_personaje = []
    for p in personajes:
        b = tk.Button(frame_personajes, text=p, font=("Arial", 16), width=15, height=5)
        b.pack(side="left", padx=20)
        botones_personaje.append(b)

    for b in botones_personaje:
        nombre = b.cget("text")
        b.config(command=lambda n=nombre: elegir_personaje(n, botones_personaje))

    def ir_a_pokemones():
        if not personaje_elegido:
            tk.Label(seleccion, text="¡Elige un personaje primero!", fg="red").pack()
            return
        seleccion.withdraw()
        abrir_pokemones(seleccion)

    tk.Button(seleccion, text="Siguiente →", font=("Arial", 16), command=ir_a_pokemones).pack(pady=30)

def abrir_pokemones(ventana_anterior):
    Poke = tk.Toplevel(Inicio)
    Poke.title("Elige tus Pokémon")
    Poke.geometry("1280x720")

    tk.Label(Poke, text="Elige 3 Pokémon:", font=("Arial", 24)).pack(pady=20)

    pokemones = ["Bulbasaur", "Charmander", "Squirtle", "Pikachu",
                 "Jigglypuff", "Meowth", "Psyduck", "Snorlax", "Eevee", "Gengar"]

    frame_poke = tk.Frame(Poke)
    frame_poke.pack(pady=10)

    label_info = tk.Label(Poke, text="Seleccionados: 0/3", font=("Arial", 14))
    label_info.pack(pady=10)

    botones_poke = []

    def elegir_pokemon(nombre, boton):
        global pokemones_elegidos
        if nombre in pokemones_elegidos:
            pokemones_elegidos.remove(nombre)
            boton.config(bg="SystemButtonFace", relief="raised")
        elif len(pokemones_elegidos) < 3:
            pokemones_elegidos.append(nombre)
            boton.config(bg="lightgreen", relief="sunken")

        for b in botones_poke:
            n = b.cget("text")
            if n not in pokemones_elegidos and len(pokemones_elegidos) >= 3:
                b.config(state="disabled")
            else:
                b.config(state="normal")

        label_info.config(text=f"Seleccionados: {len(pokemones_elegidos)}/3")

    for i, p in enumerate(pokemones):
        b = tk.Button(frame_poke, text=p, font=("Arial", 14), width=12, height=3)
        b.grid(row=i//5, column=i%5, padx=10, pady=10)
        botones_poke.append(b)

    for b in botones_poke:
        nombre = b.cget("text")
        b.config(command=lambda n=nombre, btn=b: elegir_pokemon(n, btn))

    def ir_a_juego():
        if len(pokemones_elegidos) < 3:
            tk.Label(Poke, text="¡Elige 3 Pokémon primero!", fg="red").pack()
            return
        Poke.withdraw()
        abrir_juego()

    tk.Button(Poke, text="¡Comenzar!", font=("Arial", 16), bg="green", fg="white",
              command=ir_a_juego).pack(pady=20)

def abrir_juego():
    global coleccion_jugador
    coleccion_jugador = pokemones_elegidos.copy()
    abrir_batalla()

def abrir_creditos():
    Inicio.withdraw()
    creditos = tk.Toplevel(Inicio)
    creditos.title("Creditos")
    creditos.geometry("1280x720")
    tk.Label(creditos, text="Todo gracias a Luis", font=("Arial", 20)).pack(pady=20)

# ============================================
# MENU PRINCIPAL
# ============================================

fotoinicio = tk.PhotoImage(file="Iniciar.png")
fotocreditos = tk.PhotoImage(file="Creditos.png")

boton = tk.Button(Inicio, image=fotoinicio, command=abrir_seleccion, bg="yellow", fg="red")
boton.pack(pady=10)

boton2 = tk.Button(Inicio, image=fotocreditos, command=abrir_creditos, bg="yellow", fg="red")
boton2.pack(pady=0)

boton_lb = tk.Button(Inicio, text="🏆 Leaderboard", font=("Arial", 14), command=abrir_leaderboard)
boton_lb.pack(pady=10)

Inicio.mainloop()


