import tkinter as tk #se importa la lista de tkinter para tener una interfaz grafica sore la cual trabajar
import game #importacion de otro archivo el cual contiene lo respectivo al combate

#Abrir el menu del juego
Inicio = tk.Tk()
Inicio.title("Pokekirk") #pone el nombre a la ventana
Inicio.geometry("1280x720") #da el tamaño de la ventana

personaje_elegido = None
pokemones_elegidos = [] #se crea una lista vacía para poder elegir el personaje

def abrir_seleccion(): #se abre una funcion que reciba la accioon de abrir un boton el cuál abra otra ventana, cierre la anterior, y esa nueva ventana va a abrir una lista de seleccion de personajes 
    Inicio.withdraw()
    seleccion = tk.Toplevel(Inicio)
    seleccion.title("seleccion") #nombre de la ventana
    seleccion.geometry("1280x720") #tamaño de la ventana
    tk.Label(seleccion, text="Bienvenido! escoge tu personaje y tus pokemones", font=("Arial", 20)).pack(pady=20) #muestra una etiqueta que se encarga de mostrar un texto el cual sea encargado de motivar al jugador de elegir su personaje

    personajes = ["Jeffrey", "Carlos K", "Sean"] #se hace una lista que indique cuales son los nombres de los personajes

    def elegir_personaje(nombre, botones): #hace una funcion que recibe el nombre y el boton que presionó el usuario, lo guarda
        global personaje_elegido #esto va a indicar que la variable global (una variable que es facil de modificar) sea modificada
        personaje_elegido = nombre 
        for b in botones: #al elegir el personaje se hace un bucle el cual recorre la lista
            b.config(relief="raised", bg="SystemButtonFace") #esto hace que resetea los botones al color normal
        botones[personajes.index(nombre)].config(relief="sunken", bg="lightblue") #el boton que elegimos del personaje crea la ilusion de que se hunde y lo pone de color azul claro

    frame_personajes = tk.Frame(seleccion) #crea una especie de contenedor que almacena el personaje que se eligió
    frame_personajes.pack(pady=20) #muestra el personaje que se eligió con espacio arriba y abajo

    botones_personaje = [] #aca se va a guardar la eleccion de personajes
    for p in personajes: #recorre cada boton ya creado
        b = tk.Button(frame_personajes, text=p, font=("Arial", 16), width=15, height=5) #
        b.pack(side="left", padx=20) #coloca el boton a la izquierda del anterior con espacio
        botones_personaje.append(b) #agrega lo elegido a la lista de botones

    for b in botones_personaje: #se usa otro for para recorrer los botones ya hechos
        nombre = b.cget("text") #obtiene el nombre del personaje
        b.config(command=lambda n=nombre: elegir_personaje(n, botones_personaje)) #cuando se hace clic se le asigna la funcion para elegir el personaje y el lambda para darle ese nombre como parametro para usarse

    def ir_a_pokemones():
        if not personaje_elegido:
            tk.Label(seleccion, text="¡Elige un personaje primero!", fg="red").pack() #si no se elige un personaje manda error en rojo
            return
        seleccion.withdraw()  
        abrir_pokemones(seleccion)  #se abre de nuevo la ventana para volver a elegir los pokemones

    tk.Button(seleccion, text="Siguiente →", font=("Arial", 16), command=ir_a_pokemones).pack(pady=30)  #hace el boton de ir a siguiente y se abre otra ventana para ir a pokemones


def abrir_pokemones(ventana_anterior): #crea la ventana de la seleccion de pokemones
    Poke = tk.Toplevel(Inicio)
    Poke.title("Elige tus Pokémon") #titulo de la ventanilla
    Poke.geometry("1280x720") #tamaño de la ventana

    tk.Label(Poke, text="Elige 3 Pokémon:", font=("Arial", 24)).pack(pady=20) #crea una etiqueta la cual dice q elija a los pokemones

    pokemones = ["Bulbasaur", "Charmander", "Squirtle", "Pikachu",
                 "Jigglypuff", "Meowth", "Psyduck", "Snorlax", "Eevee", "Gengar"] #se crea una lista para poner los nombres de todos los pokemones

    frame_poke = tk.Frame(Poke) #se almacena la informacion escogida por el usuario
    frame_poke.pack(pady=10) #se muestra lo escogido

    label_info = tk.Label(Poke, text="Seleccionados: 0/3", font=("Arial", 14)) #hace una etiqueta que muestre cuantos pokemones llevo hasta el momento
    label_info.pack(pady=10) #muestra la etiqueta actualizada

    botones_poke = [] #crea una lista vacia para guardar la eleccion de pokemones

    def elegir_pokemon(nombre, boton): #se crea una funcion que reciba el pokemon elegido y el boton apretado
        global pokemones_elegidos #se usa la variable global para poder modificarla a gusto
        if nombre in pokemones_elegidos:
            pokemones_elegidos.remove(nombre)
            boton.config(bg="SystemButtonFace", relief="raised") #si el pokemon ya esta elegido lo quita de la lista y se procede a regresarlo a su color normal
        elif len(pokemones_elegidos) < 3:
            pokemones_elegidos.append(nombre)
            boton.config(bg="lightgreen", relief="sunken") #si hay menos de 3 pokemones elegidos cada vez q agregas uno hunde el boton y lo pone de color verde

        for b in botones_poke: #recorre la lista de los pokemones
            n = b.cget("text") #esto lo que hace es que obtiene el nombre del pokemon del boton escogido
            if n not in pokemones_elegidos and len(pokemones_elegidos) >= 3: 
                b.config(state="disabled") #esto lo que va a hacer es que si ya hay 3 botones elegidos bloquea el resto dejandolos totalmente inutiles
            else:
                b.config(state="normal") #sino, se desbloquea el boton y podes seguir eligiendo

        label_info.config(text=f"Seleccionados: {len(pokemones_elegidos)}/3") #esto va a actualizar el texto del contador con la cantidad actual elegida de pokemones, ejemplo, si solo se escogio uno va a mostrar un "1" en la pantalla y asi sucesivamente

    for i, p in enumerate(pokemones): #recorre la lista de los pokemones en su respectivo orden
        b = tk.Button(frame_poke, text=p, font=("Arial", 14), width=12, height=3) #crea un boton por cada pokemon
        b.grid(row=i//5, column=i%5, padx=10, pady=10)
        botones_poke.append(b) #va agregando a la lista de botones el pokemon previamente elegido

    for b in botones_poke: #recorre cada boton de pokemon 
        nombre = b.cget("text") #se obtiene el nombre del pokemon
        b.config(command=lambda n=nombre, btn=b: elegir_pokemon(n, btn)) #asigna al boton la funcion de elegir el pokemon, guardarlo para sucesivamente usarlo

    def ir_a_juego():
        if len(pokemones_elegidos) < 3:
            tk.Label(Poke, text="¡Elige 3 Pokémon primero!", fg="red").pack() #si no se eligen 3 pokemones manda error en rojo
            return #y aca se edtiene todo porque hay un error
        print(f"Personaje: {personaje_elegido}")
        print(f"Pokémon: {pokemones_elegidos}")
        Poke.withdraw() #cierra la ventana de pokemones
        abrir_juego()   #llama a la funcion para que abra la ventana en donde los bichos van a pelear

    tk.Button(Poke, text="¡Comenzar!", font=("Arial", 16), bg="green", fg="white",
              command=ir_a_juego).pack(pady=20) #crea el boton de comenzar de color verde y se le asigna la funcion de ir a la ventana ya del juego en si


def abrir_juego():
    Juego = tk.Toplevel(Inicio) #crea la ventana principal del juego
    Juego.title("Juego") #titulo de la ventana
    Juego.geometry("1280x720") #tamaño de la ventana

    tk.Label(Juego, text=f"Personaje: {personaje_elegido}", font=("Arial", 20)).pack(pady=20) #crea una etiqueta que muestre los personajes elegidos
    tk.Label(Juego, text=f"Pokémon: {', '.join(pokemones_elegidos)}", font=("Arial", 20)).pack(pady=10) #muestra abajo los pokemones previamente seleccionados

def abrir_creditos():
    Inicio.withdraw()
    creditos = tk.Toplevel(Inicio)
    creditos.title("Creditos")
    creditos.geometry("1280x720")
    tk.Label(creditos, text="Todo gracias a Luis", font=("Arial", 20)).pack(pady=20)

fotoinicio = tk.PhotoImage(file="Iniciar.png")
fotocreditos = tk.PhotoImage(file="Creditos.png")

boton = tk.Button(Inicio, image=fotoinicio, command=abrir_seleccion, bg="yellow", fg="red")
boton.pack(pady=10)

boton2 = tk.Button(Inicio, image=fotocreditos, command=abrir_creditos, bg="yellow", fg="red")
boton2.pack(pady=0)



Inicio.mainloop()

