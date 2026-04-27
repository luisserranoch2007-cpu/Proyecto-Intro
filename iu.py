import tkinter as tk
import game

#Abrir el menu del juego
Inicio = tk.Tk()
Inicio.title("Pokekirk")
Inicio.geometry("1280x720")

personaje_elegido = None
pokemones_elegidos = []

def abrir_seleccion():
    Inicio.withdraw()
    seleccion = tk.Toplevel(Inicio)
    seleccion.title("seleccion")
    seleccion.geometry("1280x720")
    tk.Label(seleccion, text="Bienvenido! escoge tu personaje y tus pokemones", font=("Arial", 20)).pack(pady=20)

    personajes = ["Ash", "Misty", "Brock"]

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
            tk.Label(seleccion, text="¡Elige un personaje primero!", fg="red").pack()  # ← corregido
            return
        seleccion.withdraw()  # ← corregido
        abrir_pokemones(seleccion)  # ← corregido

    tk.Button(seleccion, text="Siguiente →", font=("Arial", 16), command=ir_a_pokemones).pack(pady=30)  # ← corregido


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
            # deseleccionar
            pokemones_elegidos.remove(nombre)
            boton.config(bg="SystemButtonFace", relief="raised")
        elif len(pokemones_elegidos) < 3:
            # seleccionar
            pokemones_elegidos.append(nombre)
            boton.config(bg="lightgreen", relief="sunken")

        # bloquear todos si ya hay 3
        for b in botones_poke:
            n = b.cget("text")
            if n not in pokemones_elegidos and len(pokemones_elegidos) >= 3:
                b.config(state="disabled")
            else:
                b.config(state="normal")

        label_info.config(text=f"Seleccionados: {len(pokemones_elegidos)}/3")

    # Crear botones en grilla de 5x2
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
        print(f"Personaje: {personaje_elegido}")
        print(f"Pokémon: {pokemones_elegidos}")
        Poke.withdraw()
        abrir_juego()  # siguiente ventana

    tk.Button(Poke, text="¡Comenzar!", font=("Arial", 16), bg="green", fg="white",
              command=ir_a_juego).pack(pady=20)


def abrir_juego():
    Juego = tk.Toplevel(Inicio)
    Juego.title("Juego")
    Juego.geometry("1280x720")

    tk.Label(Juego, text=f"Personaje: {personaje_elegido}", font=("Arial", 20)).pack(pady=20)
    tk.Label(Juego, text=f"Pokémon: {', '.join(pokemones_elegidos)}", font=("Arial", 20)).pack(pady=10)
    # aquí continúas el juego

def abrir_creditos():
    Inicio.withdraw()
    creditos = tk.Toplevel(Inicio)
    creditos.title("Creditos")
    creditos.geometry("1280x720")
    tk.Label(creditos, text="Todo garcias a Luis", font=("Arial", 20)).pack(pady=20)

fotoinicio = tk.PhotoImage(file="Iniciar.png")
fotocreditos = tk.PhotoImage(file="Creditos.png")

boton = tk.Button(Inicio, image=fotoinicio, command=abrir_seleccion, bg="yellow", fg="red")
boton.pack(pady=10)

boton2 = tk.Button(Inicio, image=fotocreditos, command=abrir_creditos, bg="yellow", fg="red")
boton2.pack(pady=0)



Inicio.mainloop()

