import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
import os
from urllib.parse import quote_plus
from datetime import datetime


# =========================================================
# CONEXIÓN A MONGODB
# =========================================================

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

user = os.getenv("MONGO_USER")
password = quote_plus(os.getenv("MONGO_PASSWORD"))
cluster = os.getenv("MONGO_CLUSTER")
database = os.getenv("MONGO_DB")
collection_name = os.getenv("MONGO_COLLECTION")


if not all([user, password, cluster, database, collection_name]):
    raise ValueError("Faltan variables en el archivo .env")


mongo_uri = f"mongodb+srv://{user}:{password}@{cluster}"

client = MongoClient(mongo_uri)

db = client[database]

coleccion = db[collection_name]


# =========================================================
# VARIABLES
# =========================================================

paciente_actual = None


# =========================================================
# CREAR PACIENTE
# =========================================================

def crear_paciente():

    nombre = entrada_nombre.get().strip()
    edad = entrada_edad.get().strip()
    oxigenacion = entrada_oxigenacion.get().strip()
    frecuencia = entrada_frecuencia.get().strip()
    presion = entrada_presion.get().strip()
    peso = entrada_peso.get().strip()
    talla = entrada_talla.get().strip()
    tk = entrada_tk.get().strip()

    if not nombre or not edad or not oxigenacion or not frecuencia \
            or not presion or not peso or not talla or not tk:

        messagebox.showwarning(
            "Datos incompletos",
            "Completa todos los datos del paciente."
        )

        return

    try:

        edad = int(edad)
        oxigenacion = float(oxigenacion)
        frecuencia = int(frecuencia)
        peso = float(peso)
        talla = float(talla)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Edad, oxigenación, frecuencia, peso y talla deben ser números."
        )

        return

    # Comprobar si ya existe el TK

    paciente_existente = coleccion.find_one(
        {"tk": tk}
    )

    if paciente_existente:

        messagebox.showwarning(
            "Paciente existente",
            "Ya existe un paciente con ese TK."
        )

        return

    # Calcular IMC

    talla_metros = talla / 100

    imc = peso / (talla_metros ** 2)

    # Crear documento

    paciente = {

        "tk": tk,

        "nombre": nombre,

        "edad": edad,

        "oxigenacion": oxigenacion,

        "frecuencia_cardiaca": frecuencia,

        "presion_arterial": presion,

        "peso": peso,

        "talla": talla,

        "imc": round(imc, 2),

        "fecha_registro": datetime.now()

    }

    # INSERTAR

    resultado = coleccion.insert_one(
        paciente
    )

    messagebox.showinfo(
        "Crear",
        "Paciente registrado correctamente.\n\n"
        f"ID de MongoDB:\n{resultado.inserted_id}"
    )

    limpiar_campos()


# =========================================================
# LEER PACIENTE
# =========================================================

def leer_paciente():

    tk_buscar = entrada_tk.get().strip()

    if not tk_buscar:

        messagebox.showwarning(
            "Dato faltante",
            "Escribe el TK del paciente."
        )

        return

    # BUSCAR

    paciente = coleccion.find_one(
        {"tk": tk_buscar}
    )

    if paciente is None:

        messagebox.showwarning(
            "No encontrado",
            "No se encontró ningún paciente con ese TK."
        )

        return

    # Mostrar datos

    entrada_nombre.delete(0, tk.END)
    entrada_nombre.insert(
        0,
        paciente.get("nombre", "")
    )

    entrada_edad.delete(0, tk.END)
    entrada_edad.insert(
        0,
        paciente.get("edad", "")
    )

    entrada_oxigenacion.delete(0, tk.END)
    entrada_oxigenacion.insert(
        0,
        paciente.get("oxigenacion", "")
    )

    entrada_frecuencia.delete(0, tk.END)
    entrada_frecuencia.insert(
        0,
        paciente.get("frecuencia_cardiaca", "")
    )

    entrada_presion.delete(0, tk.END)
    entrada_presion.insert(
        0,
        paciente.get("presion_arterial", "")
    )

    entrada_peso.delete(0, tk.END)
    entrada_peso.insert(
        0,
        paciente.get("peso", "")
    )

    entrada_talla.delete(0, tk.END)
    entrada_talla.insert(
        0,
        paciente.get("talla", "")
    )

    messagebox.showinfo(
        "Leer",
        "Paciente encontrado correctamente."
    )


# =========================================================
# ACTUALIZAR PACIENTE
# =========================================================

def actualizar_paciente():

    tk_buscar = entrada_tk.get().strip()

    if not tk_buscar:

        messagebox.showwarning(
            "Dato faltante",
            "Escribe el TK del paciente."
        )

        return

    paciente = coleccion.find_one(
        {"tk": tk_buscar}
    )

    if paciente is None:

        messagebox.showwarning(
            "No encontrado",
            "No existe un paciente con ese TK."
        )

        return

    nombre = entrada_nombre.get().strip()
    edad = entrada_edad.get().strip()
    oxigenacion = entrada_oxigenacion.get().strip()
    frecuencia = entrada_frecuencia.get().strip()
    presion = entrada_presion.get().strip()
    peso = entrada_peso.get().strip()
    talla = entrada_talla.get().strip()

    try:

        edad = int(edad)
        oxigenacion = float(oxigenacion)
        frecuencia = int(frecuencia)
        peso = float(peso)
        talla = float(talla)

    except ValueError:

        messagebox.showerror(
            "Error",
            "Verifica los datos numéricos."
        )

        return

    # Calcular nuevamente IMC

    talla_metros = talla / 100

    imc = peso / (talla_metros ** 2)

    nuevos_datos = {

        "nombre": nombre,

        "edad": edad,

        "oxigenacion": oxigenacion,

        "frecuencia_cardiaca": frecuencia,

        "presion_arterial": presion,

        "peso": peso,

        "talla": talla,

        "imc": round(imc, 2),

        "fecha_actualizacion": datetime.now()

    }

    # ACTUALIZAR

    resultado = coleccion.update_one(

        {"tk": tk_buscar},

        {
            "$set": nuevos_datos
        }

    )

    if resultado.modified_count > 0:

        messagebox.showinfo(
            "Actualizar",
            "Paciente actualizado correctamente."
        )

    else:

        messagebox.showinfo(
            "Actualizar",
            "El paciente existe, pero no hubo cambios."
        )


# =========================================================
# ELIMINAR PACIENTE
# =========================================================

def eliminar_paciente():

    tk_buscar = entrada_tk.get().strip()

    if not tk_buscar:

        messagebox.showwarning(
            "Dato faltante",
            "Escribe el TK del paciente."
        )

        return

    paciente = coleccion.find_one(
        {"tk": tk_buscar}
    )

    if paciente is None:

        messagebox.showwarning(
            "No encontrado",
            "No existe un paciente con ese TK."
        )

        return

    confirmar = messagebox.askyesno(
        "Eliminar paciente",
        "¿Estás seguro de eliminar este paciente?"
    )

    if not confirmar:

        return

    # ELIMINAR

    resultado = coleccion.delete_one(
        {"tk": tk_buscar}
    )

    if resultado.deleted_count > 0:

        messagebox.showinfo(
            "Eliminar",
            "Paciente eliminado correctamente."
        )

        limpiar_campos()

    else:

        messagebox.showerror(
            "Error",
            "No fue posible eliminar el paciente."
        )


# =========================================================
# MOSTRAR TODOS LOS PACIENTES
# =========================================================

def mostrar_pacientes():

    ventana = tk.Toplevel(root)

    ventana.title(
        "Pacientes registrados"
    )

    ventana.geometry(
        "850x500"
    )

    texto = tk.Text(
        ventana,
        width=100,
        height=25
    )

    texto.pack(
        padx=10,
        pady=10
    )

    pacientes = coleccion.find()

    encontrados = 0

    for paciente in pacientes:

        encontrados += 1

        texto.insert(
            tk.END,
            "========================================\n"
        )

        texto.insert(
            tk.END,
            f"TK: {paciente.get('tk', '')}\n"
        )

        texto.insert(
            tk.END,
            f"Nombre: {paciente.get('nombre', '')}\n"
        )

        texto.insert(
            tk.END,
            f"Edad: {paciente.get('edad', '')}\n"
        )

        texto.insert(
            tk.END,
            f"Oxigenación: {paciente.get('oxigenacion', '')}\n"
        )

        texto.insert(
            tk.END,
            f"Frecuencia cardiaca: "
            f"{paciente.get('frecuencia_cardiaca', '')}\n"
        )

        texto.insert(
            tk.END,
            f"Presión arterial: "
            f"{paciente.get('presion_arterial', '')}\n"
        )

        texto.insert(
            tk.END,
            f"Peso: {paciente.get('peso', '')}\n"
        )

        texto.insert(
            tk.END,
            f"Talla: {paciente.get('talla', '')}\n"
        )

        texto.insert(
            tk.END,
            f"IMC: {paciente.get('imc', '')}\n"
        )

        texto.insert(
            tk.END,
            "\n"
        )

    if encontrados == 0:

        texto.insert(
            tk.END,
            "No existen pacientes registrados."
        )


# =========================================================
# LIMPIAR CAMPOS
# =========================================================

def limpiar_campos():

    entrada_tk.delete(
        0,
        tk.END
    )

    entrada_nombre.delete(
        0,
        tk.END
    )

    entrada_edad.delete(
        0,
        tk.END
    )

    entrada_oxigenacion.delete(
        0,
        tk.END
    )

    entrada_frecuencia.delete(
        0,
        tk.END
    )

    entrada_presion.delete(
        0,
        tk.END
    )

    entrada_peso.delete(
        0,
        tk.END
    )

    entrada_talla.delete(
        0,
        tk.END
    )


# =========================================================
# INTERFAZ
# =========================================================

root = tk.Tk()

root.title(
    "Sistema Hospitalario - CRUD MongoDB"
)

root.geometry(
    "850x700"
)

root.configure(
    bg="#EAF4FF"
)


# =========================================================
# TÍTULO
# =========================================================

tk.Label(
    root,
    text="SISTEMA HOSPITALARIO",
    font=("Arial", 24, "bold"),
    bg="#EAF4FF",
    fg="#123A5B"
).pack(
    pady=20
)


tk.Label(
    root,
    text="CRUD de pacientes con MongoDB",
    font=("Arial", 13),
    bg="#EAF4FF",
    fg="#234D69"
).pack(
    pady=5
)


# =========================================================
# FORMULARIO
# =========================================================

frame = tk.Frame(
    root,
    bg="#EAF4FF"
)

frame.pack(
    pady=15
)


# TK

tk.Label(
    frame,
    text="TK del paciente:",
    bg="#EAF4FF"
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=10,
    pady=7
)

entrada_tk = tk.Entry(
    frame,
    width=35
)

entrada_tk.grid(
    row=0,
    column=1,
    pady=7
)


# Nombre

tk.Label(
    frame,
    text="Nombre:",
    bg="#EAF4FF"
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=10,
    pady=7
)

entrada_nombre = tk.Entry(
    frame,
    width=35
)

entrada_nombre.grid(
    row=1,
    column=1,
    pady=7
)


# Edad

tk.Label(
    frame,
    text="Edad:",
    bg="#EAF4FF"
).grid(
    row=2,
    column=0,
    sticky="w",
    padx=10,
    pady=7
)

entrada_edad = tk.Entry(
    frame,
    width=35
)

entrada_edad.grid(
    row=2,
    column=1,
    pady=7
)


# Oxigenación

tk.Label(
    frame,
    text="Oxigenación:",
    bg="#EAF4FF"
).grid(
    row=3,
    column=0,
    sticky="w",
    padx=10,
    pady=7
)

entrada_oxigenacion = tk.Entry(
    frame,
    width=35
)

entrada_oxigenacion.grid(
    row=3,
    column=1,
    pady=7
)


# Frecuencia

tk.Label(
    frame,
    text="Frecuencia cardiaca:",
    bg="#EAF4FF"
).grid(
    row=4,
    column=0,
    sticky="w",
    padx=10,
    pady=7
)

entrada_frecuencia = tk.Entry(
    frame,
    width=35
)

entrada_frecuencia.grid(
    row=4,
    column=1,
    pady=7
)


# Presión

tk.Label(
    frame,
    text="Presión arterial:",
    bg="#EAF4FF"
).grid(
    row=5,
    column=0,
    sticky="w",
    padx=10,
    pady=7
)

entrada_presion = tk.Entry(
    frame,
    width=35
)

entrada_presion.grid(
    row=5,
    column=1,
    pady=7


)


# Peso

tk.Label(
    frame,
    text="Peso (kg):",
    bg="#EAF4FF"
).grid(
    row=6,
    column=0,
    sticky="w",
    padx=10,
    pady=7
)

entrada_peso = tk.Entry(
    frame,
    width=35
)

entrada_peso.grid(
    row=6,
    column=1,
    pady=7
)


# Talla

tk.Label(
    frame,
    text="Talla (cm):",
    bg="#EAF4FF"
).grid(
    row=7,
    column=0,
    sticky="w",
    padx=10,
    pady=7
)

entrada_talla = tk.Entry(
    frame,
    width=35
)

entrada_talla.grid(
    row=7,
    column=1,
    pady=7
)


# =========================================================
# BOTONES CRUD
# =========================================================

frame_botones = tk.Frame(
    root,
    bg="#EAF4FF"
)

frame_botones.pack(
    pady=15
)


# CREAR

tk.Button(
    frame_botones,
    text="CREAR PACIENTE",
    command=crear_paciente,
    width=22,
    height=2,
    bg="#2E7D32",
    fg="white",
    relief="flat"
).grid(
    row=0,
    column=0,
    padx=5
)


# LEER

tk.Button(
    frame_botones,
    text="LEER PACIENTE",
    command=leer_paciente,
    width=22,
    height=2,
    bg="#1976D2",
    fg="white",
    relief="flat"
).grid(
    row=0,
    column=1,
    padx=5
)


# ACTUALIZAR

tk.Button(
    frame_botones,
    text="ACTUALIZAR PACIENTE",
    command=actualizar_paciente,
    width=22,
    height=2,
    bg="#F57C00",
    fg="white",
    relief="flat"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=10
)


# ELIMINAR

tk.Button(
    frame_botones,
    text="ELIMINAR PACIENTE",
    command=eliminar_paciente,
    width=22,
    height=2,
    bg="#C62828",
    fg="white",
    relief="flat"
).grid(
    row=1,
    column=1,
    padx=5,
    pady=10
)


# MOSTRAR TODOS

tk.Button(
    root,
    text="MOSTRAR TODOS LOS PACIENTES",
    command=mostrar_pacientes,
    width=30,
    height=2,
    bg="#5E35B1",
    fg="white",
    relief="flat"
).pack(
    pady=10
)


# LIMPIAR

tk.Button(
    root,
    text="LIMPIAR",
    command=limpiar_campos,
    width=20,
    height=2,
    bg="#607D8B",
    fg="white",
    relief="flat"
).pack(
    pady=5
)


# SALIR

tk.Button(
    root,
    text="SALIR",
    command=root.destroy,
    width=20,
    height=2,
    bg="#424242",
    fg="white",
    relief="flat"
).pack(
    pady=10
)


# =========================================================
# EJECUTAR
# =========================================================

root.mainloop()