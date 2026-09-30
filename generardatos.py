import tkinter as tk
from tkinter import messagebox
from faker import Faker
import random
from datetime import datetime, timedelta

# ==========================================
# MONGODB
# ==========================================

from pymongo import MongoClient
from dotenv import load_dotenv
from pathlib import Path
from urllib.parse import quote_plus
import os


# ==========================================
# CONFIGURACIÓN
# ==========================================

fake = Faker("es_MX")


# ==========================================
# CONEXIÓN A MONGODB
# ==========================================

env_path= Path(__file__).resolve().parent.parent / ".env"
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


# ==========================================
# FUNCIONES PARA GENERAR DATOS
# ==========================================

def generar_tk():

    return f"TK-{random.randint(10000, 99999)}"


def generar_numero_cita():

    return random.randint(1000, 9999)


def generar_consultorio():

    return random.randint(1, 20)


def generar_piso():

    return random.randint(1, 5)


def generar_fecha():

    fecha = datetime.now() + timedelta(
        days=random.randint(1, 15)
    )

    return fecha.strftime("%d/%m/%Y")


def generar_hora():

    hora = random.randint(8, 17)

    minutos = random.choice(
        [0, 15, 30, 45]
    )

    return f"{hora:02d}:{minutos:02d}"


# ==========================================
# CRUD - INSERTAR
# ==========================================

def insertar_paciente(datos):

    if coleccion is None:

        messagebox.showerror(
            "MongoDB",
            "No hay conexión con MongoDB."
        )

        return None

    try:

        resultado = coleccion.insert_one(datos)

        messagebox.showinfo(
            "MongoDB",
            "Paciente guardado correctamente."
        )

        return resultado.inserted_id

    except Exception as e:

        messagebox.showerror(
            "MongoDB",
            f"Error al guardar el paciente:\n\n{e}"
        )

        return None


# ==========================================
# CRUD - CONSULTAR
# ==========================================

def buscar_paciente(tk_numero):

    if coleccion is None:

        messagebox.showerror(
            "MongoDB",
            "No hay conexión con MongoDB."
        )

        return None

    try:

        paciente = coleccion.find_one(
            {"tk": tk_numero}
        )

        return paciente

    except Exception as e:

        messagebox.showerror(
            "MongoDB",
            f"Error al consultar:\n\n{e}"
        )

        return None


# ==========================================
# CRUD - ACTUALIZAR
# ==========================================

def actualizar_paciente(
    tk_numero,
    nuevos_datos
):

    if coleccion is None:

        messagebox.showerror(
            "MongoDB",
            "No hay conexión con MongoDB."
        )

        return

    try:

        resultado = coleccion.update_one(

            {"tk": tk_numero},

            {
                "$set": nuevos_datos
            }

        )

        if resultado.matched_count == 0:

            messagebox.showwarning(
                "MongoDB",
                "No se encontró el paciente."
            )

        elif resultado.modified_count == 0:

            messagebox.showinfo(
                "MongoDB",
                "El paciente existe, pero no hubo cambios."
            )

        else:

            messagebox.showinfo(
                "MongoDB",
                "Paciente actualizado correctamente."
            )

    except Exception as e:

        messagebox.showerror(
            "MongoDB",
            f"Error al actualizar:\n\n{e}"
        )


# ==========================================
# CRUD - ELIMINAR
# ==========================================

def eliminar_paciente(tk_numero):

    if coleccion is None:

        messagebox.showerror(
            "MongoDB",
            "No hay conexión con MongoDB."
        )

        return

    try:

        resultado = coleccion.delete_one(
            {"tk": tk_numero}
        )

        if resultado.deleted_count > 0:

            messagebox.showinfo(
                "MongoDB",
                "Paciente eliminado correctamente."
            )

        else:

            messagebox.showwarning(
                "MongoDB",
                "No se encontró el paciente."
            )

    except Exception as e:

        messagebox.showerror(
            "MongoDB",
            f"Error al eliminar:\n\n{e}"
        )


# ==========================================
# DIAGNÓSTICO
# ==========================================

def realizar_diagnostico():

    nombre = entrada_nombre.get().strip()

    if nombre == "":

        messagebox.showwarning(
            "Dato faltante",
            "Por favor, escribe el nombre del paciente."
        )

        return

    try:

        edad = int(
            entrada_edad.get()
        )

        oxigenacion = float(
            entrada_oxigenacion.get()
        )

        frecuencia = int(
            entrada_frecuencia.get()
        )

        peso = float(
            entrada_peso.get()
        )

        talla = float(
            entrada_talla.get()
        )

        presion = entrada_presion.get().strip()

        if edad <= 0:
            raise ValueError

        if oxigenacion <= 0:
            raise ValueError

        if frecuencia <= 0:
            raise ValueError

        if peso <= 0:
            raise ValueError

        if talla <= 0:
            raise ValueError


        # ==========================================
        # CALCULAR IMC
        # ==========================================

        talla_metros = talla / 100

        imc = peso / (
            talla_metros ** 2
        )


        # ==========================================
        # ANALIZAR PRESIÓN
        # ==========================================

        try:

            sistolica, diastolica = presion.split("/")

            sistolica = int(
                sistolica
            )

            diastolica = int(
                diastolica
            )

        except:

            messagebox.showwarning(
                "Presión incorrecta",
                "Escribe la presión en formato 120/80."
            )

            return


        # ==========================================
        # RESULTADOS
        # ==========================================

        resultados = []

        menu_destino = "Cita"


        # ==========================================
        # OXIGENACIÓN
        # ==========================================

        if oxigenacion < 90:

            resultados.append(
                "Oxigenación baja."
            )

            menu_destino = "Urgencias"

        elif oxigenacion < 95:

            resultados.append(
                "Oxigenación ligeramente baja. "
                "Se recomienda valoración médica."
            )

        else:

            resultados.append(
                "Oxigenación dentro del rango esperado."
            )


        # ==========================================
        # FRECUENCIA CARDIACA
        # ==========================================

        if frecuencia < 60:

            resultados.append(
                "Frecuencia cardiaca baja."
            )

            if menu_destino != "Urgencias":

                menu_destino = "Cita"

        elif frecuencia > 100:

            resultados.append(
                "Frecuencia cardiaca elevada."
            )

            if frecuencia > 120:

                menu_destino = "Urgencias"

        else:

            resultados.append(
                "Frecuencia cardiaca dentro del rango esperado."
            )


        # ==========================================
        # PRESIÓN ARTERIAL
        # ==========================================

        if sistolica >= 180 or diastolica >= 120:

            resultados.append(
                "Presión arterial muy elevada."
            )

            menu_destino = "Urgencias"

        elif sistolica >= 140 or diastolica >= 90:

            resultados.append(
                "Presión arterial elevada."
            )

            if menu_destino != "Urgencias":

                menu_destino = "Cita"

        else:

            resultados.append(
                "Presión arterial dentro del rango esperado."
            )


        # ==========================================
        # IMC
        # ==========================================

        resultados.append(
            f"IMC calculado: {imc:.2f}"
        )

        if imc >= 30:

            resultados.append(
                "Resultado orientativo: posible obesidad."
            )

            if menu_destino != "Urgencias":

                menu_destino = "Cita"

        elif imc >= 25:

            resultados.append(
                "Resultado orientativo: sobrepeso."
            )

            if menu_destino != "Urgencias":

                menu_destino = "Cita"

        else:

            resultados.append(
                "IMC dentro del rango considerado normal."
            )


        # ==========================================
        # GENERAR CITA / TK
        # ==========================================

        tk_numero = generar_tk()

        numero_cita = generar_numero_cita()

        consultorio = generar_consultorio()

        piso = generar_piso()

        fecha = generar_fecha()

        hora = generar_hora()


        # ==========================================
        # DATOS PARA MONGODB
        # ==========================================

        datos_paciente = {

            "nombre": nombre,

            "edad": edad,

            "oxigenacion": oxigenacion,

            "frecuencia_cardiaca": frecuencia,

            "presion_arterial": presion,

            "peso": peso,

            "talla": talla,

            "imc": round(imc, 2),

            "destino": menu_destino,

            "tk": tk_numero,

            "numero_cita": numero_cita,

            "consultorio": consultorio,

            "piso": piso,

            "fecha": fecha,

            "hora": hora,

            "resultados": resultados,

            "fecha_registro": datetime.now()

        }


        # ==========================================
        # INSERTAR EN MONGODB
        # ==========================================

        insertar_paciente(
            datos_paciente
        )


        # ==========================================
        # MOSTRAR INFORMACIÓN
        # ==========================================

        texto = f"""

ASISTENTE HOSPITALARIO


Paciente: {nombre}

Edad: {edad} años


----------------------------------------
SIGNOS Y MEDIDAS
----------------------------------------


Oxigenación: {oxigenacion} %

Frecuencia cardiaca: {frecuencia} lpm

Presión arterial: {presion}

Peso: {peso} kg

Talla: {talla} cm

IMC: {imc:.2f}


----------------------------------------
RESULTADO
----------------------------------------

"""

        for resultado in resultados:

            texto += resultado + "\n"


        texto += f"""

----------------------------------------
DESTINO RECOMENDADO
----------------------------------------

{menu_destino}


----------------------------------------
DATOS DE LA CITA
----------------------------------------


TK: {tk_numero}

Número de cita: {numero_cita}

Consultorio: {consultorio}

Piso: {piso}

Fecha: {fecha}

Hora: {hora}

"""


        if menu_destino == "Urgencias":

            texto += """

El resultado requiere atención prioritaria.

Dirígete al área de URGENCIAS.

Si se trata de una emergencia real,
solicita atención médica inmediata.

"""

        elif menu_destino == "Cita":

            texto += """

Se recomienda acudir a la CITA
generada para valoración profesional.

"""


        resultado_texto.config(
            state="normal"
        )

        resultado_texto.delete(
            "1.0",
            tk.END
        )

        resultado_texto.insert(
            tk.END,
            texto
        )

        resultado_texto.config(
            state="disabled"
        )


        # ==========================================
        # GUARDAR DATOS PARA LOS BOTONES
        # ==========================================

        datos_cita["tk"] = tk_numero

        datos_cita["numero"] = numero_cita

        datos_cita["consultorio"] = consultorio

        datos_cita["piso"] = piso

        datos_cita["fecha"] = fecha

        datos_cita["hora"] = hora

        datos_cita["destino"] = menu_destino


    except ValueError:

        messagebox.showerror(
            "Error",
            "Verifica que todos los datos numéricos sean correctos."
        )


# ==========================================
# CONSULTAR PACIENTE
# ==========================================

def consultar_paciente():

    ventana = tk.Toplevel(root)

    ventana.title(
        "Consultar paciente"
    )

    ventana.geometry(
        "500x450"
    )

    ventana.resizable(
        False,
        False
    )

    ventana.configure(
        bg="#EAF4FF"
    )


    tk.Label(
        ventana,
        text="CONSULTAR PACIENTE",
        font=("Arial", 20, "bold"),
        bg="#EAF4FF",
        fg="#123A5B"
    ).pack(pady=20)


    tk.Label(
        ventana,
        text="Ingresa el TK del paciente:",
        font=("Arial", 12),
        bg="#EAF4FF",
        fg="#234D69"
    ).pack(pady=5)


    entrada_tk = tk.Entry(
        ventana,
        width=30,
        font=("Arial", 11)
    )

    entrada_tk.pack(
        pady=10
    )


    resultado = tk.Text(
        ventana,
        width=55,
        height=14,
        font=("Consolas", 9)
    )

    resultado.pack(
        pady=10
    )


    def buscar():

        tk_numero = entrada_tk.get().strip()

        if tk_numero == "":

            messagebox.showwarning(
                "Dato faltante",
                "Ingresa un TK."
            )

            return


        paciente = buscar_paciente(
            tk_numero
        )


        if paciente:

            paciente.pop(
                "_id",
                None
            )

            resultado.delete(
                "1.0",
                tk.END
            )

            for clave, valor in paciente.items():

                resultado.insert(
                    tk.END,
                    f"{clave}: {valor}\n"
                )


    tk.Button(
        ventana,
        text="Buscar",
        command=buscar,
        width=20,
        bg="#00A6A6",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        bd=0
    ).pack(pady=10)


# ==========================================
# ACTUALIZAR PACIENTE
# ==========================================

def actualizar_desde_ventana():

    ventana = tk.Toplevel(root)

    ventana.title(
        "Actualizar paciente"
    )

    ventana.geometry(
        "500x450"
    )

    ventana.resizable(
        False,
        False
    )

    ventana.configure(
        bg="#EAF4FF"
    )


    tk.Label(
        ventana,
        text="ACTUALIZAR PACIENTE",
        font=("Arial", 20, "bold"),
        bg="#EAF4FF",
        fg="#123A5B"
    ).pack(pady=20)


    tk.Label(
        ventana,
        text="TK del paciente:",
        bg="#EAF4FF",
        fg="#234D69"
    ).pack()


    entrada_tk = tk.Entry(
        ventana,
        width=30
    )

    entrada_tk.pack(
        pady=8
    )


    tk.Label(
        ventana,
        text="Nuevo nombre:",
        bg="#EAF4FF",
        fg="#234D69"
    ).pack()


    entrada_nombre = tk.Entry(
        ventana,
        width=30
    )

    entrada_nombre.pack(
        pady=8
    )


    tk.Label(
        ventana,
        text="Nueva edad:",
        bg="#EAF4FF",
        fg="#234D69"
    ).pack()


    entrada_edad = tk.Entry(
        ventana,
        width=30
    )

    entrada_edad.pack(
        pady=8
    )


    tk.Label(
        ventana,
        text="Nuevo peso:",
        bg="#EAF4FF",
        fg="#234D69"
    ).pack()


    entrada_peso = tk.Entry(
        ventana,
        width=30
    )

    entrada_peso.pack(
        pady=8
    )


    def actualizar():

        tk_numero = entrada_tk.get().strip()

        nombre = entrada_nombre.get().strip()


        if tk_numero == "":

            messagebox.showwarning(
                "Dato faltante",
                "Ingresa el TK."
            )

            return


        try:

            edad = int(
                entrada_edad.get()
            )

            peso = float(
                entrada_peso.get()
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Edad y peso deben ser números."
            )

            return


        nuevos_datos = {

            "nombre": nombre,

            "edad": edad,

            "peso": peso

        }


        actualizar_paciente(
            tk_numero,
            nuevos_datos
        )


    tk.Button(
        ventana,
        text="Actualizar",
        command=actualizar,
        width=20,
        bg="#3A86FF",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        bd=0
    ).pack(pady=20)


# ==========================================
# ELIMINAR PACIENTE
# ==========================================

def eliminar_desde_ventana():

    ventana = tk.Toplevel(root)

    ventana.title(
        "Eliminar paciente"
    )

    ventana.geometry(
        "400x250"
    )

    ventana.resizable(
        False,
        False
    )

    ventana.configure(
        bg="#EAF4FF"
    )


    tk.Label(
        ventana,
        text="ELIMINAR PACIENTE",
        font=("Arial", 20, "bold"),
        bg="#EAF4FF",
        fg="#123A5B"
    ).pack(pady=20)


    tk.Label(
        ventana,
        text="Ingresa el TK:",
        font=("Arial", 12),
        bg="#EAF4FF",
        fg="#234D69"
    ).pack()


    entrada_tk = tk.Entry(
        ventana,
        width=30
    )

    entrada_tk.pack(
        pady=10
    )


    def eliminar():

        tk_numero = entrada_tk.get().strip()


        if tk_numero == "":

            messagebox.showwarning(
                "Dato faltante",
                "Ingresa el TK."
            )

            return


        confirmar = messagebox.askyesno(
            "Confirmar",
            "¿Seguro que deseas eliminar este paciente?"
        )


        if confirmar:

            eliminar_paciente(
                tk_numero
            )

            ventana.destroy()


    tk.Button(
        ventana,
        text="Eliminar",
        command=eliminar,
        width=20,
        bg="#E63946",
        fg="white",
        font=("Arial", 11, "bold"),
        relief="flat",
        bd=0
    ).pack(pady=20)


# ==========================================
# URGENCIAS
# ==========================================

def abrir_urgencias():

    ventana = tk.Toplevel(root)

    ventana.title(
        "Urgencias"
    )

    ventana.geometry(
        "500x400"
    )

    ventana.resizable(
        False,
        False
    )

    ventana.configure(
        bg="#EAF4FF"
    )


    tk.Label(
        ventana,
        text="URGENCIAS",
        font=("Arial", 22, "bold"),
        bg="#EAF4FF",
        fg="#123A5B"
    ).pack(pady=20)


    tk.Label(
        ventana,
        text="Selecciona el motivo de atención:",
        font=("Arial", 12),
        bg="#EAF4FF",
        fg="#234D69"
    ).pack(pady=10)


    motivos = [

        "Dificultad para respirar",

        "Dolor intenso",

        "Presión arterial muy elevada",

        "Frecuencia cardiaca alterada",

        "Otro"

    ]


    motivo = tk.StringVar()

    motivo.set(
        motivos[0]
    )


    menu = tk.OptionMenu(
        ventana,
        motivo,
        *motivos
    )


    menu.config(
        width=35,
        font=("Arial", 11),
        bg="#FFFFFF",
        fg="#123A5B",
        highlightbackground="#D5E8FF",
        activebackground="#D5E8FF"
    )

    menu.pack(
        pady=10
    )


    def confirmar():

        messagebox.showinfo(
            "Urgencias",
            f"Motivo seleccionado:\n\n"
            f"{motivo.get()}\n\n"
            f"El paciente debe ser valorado por "
            f"personal médico."
        )


    tk.Button(
        ventana,
        text="Solicitar atención",
        command=confirmar,
        font=("Arial", 12, "bold"),
        width=25,
        bg="#1F6FEB",
        fg="white",
        activebackground="#184FA5",
        activeforeground="white",
        relief="flat",
        bd=0
    ).pack(
        pady=25
    )


    tk.Button(
        ventana,
        text="Cerrar",
        command=ventana.destroy,
        width=15,
        bg="#E63946",
        fg="white",
        activebackground="#C62F3C",
        activeforeground="white",
        relief="flat",
        bd=0
    ).pack()


# ==========================================
# CITA
# ==========================================

def abrir_cita():

    ventana = tk.Toplevel(root)

    ventana.title(
        "Cita médica"
    )

    ventana.geometry(
        "500x500"
    )

    ventana.resizable(
        False,
        False
    )

    ventana.configure(
        bg="#EAF4FF"
    )


    tk.Label(
        ventana,
        text="CITA MÉDICA",
        font=("Arial", 22, "bold"),
        bg="#EAF4FF",
        fg="#123A5B"
    ).pack(
        pady=20
    )


    if "numero" in datos_cita:

        informacion = f"""

TK: {datos_cita['tk']}


Número de cita:
{datos_cita['numero']}


Consultorio:
{datos_cita['consultorio']}


Piso:
{datos_cita['piso']}


Fecha:
{datos_cita['fecha']}


Hora:
{datos_cita['hora']}

"""


        tk.Label(
            ventana,
            text=informacion,
            font=("Arial", 13),
            justify="left",
            bg="#EAF4FF",
            fg="#123A5B"
        ).pack(
            pady=10
        )


    else:

        tk.Label(
            ventana,
            text="Primero realiza el diagnóstico\ndel paciente.",
            font=("Arial", 13),
            bg="#EAF4FF",
            fg="#234D69"
        ).pack(
            pady=30
        )


    tk.Button(
        ventana,
        text="Cerrar",
        command=ventana.destroy,
        width=15,
        bg="#E63946",
        fg="white",
        activebackground="#C62F3C",
        activeforeground="white",
        relief="flat",
        bd=0
    ).pack(
        pady=20
    )


# ==========================================
# FARMACIA
# ==========================================

def abrir_farmacia():

    ventana = tk.Toplevel(root)

    ventana.title(
        "Farmacia"
    )

    ventana.geometry(
        "500x400"
    )

    ventana.resizable(
        False,
        False
    )

    ventana.configure(
        bg="#EAF4FF"
    )


    tk.Label(
        ventana,
        text="FARMACIA",
        font=("Arial", 22, "bold"),
        bg="#EAF4FF",
        fg="#123A5B"
    ).pack(
        pady=20
    )


    tk.Label(
        ventana,
        text="Selecciona una opción:",
        font=("Arial", 12),
        bg="#EAF4FF",
        fg="#234D69"
    ).pack(
        pady=10
    )


    opciones = [

        "Consultar medicamento",

        "Consultar disponibilidad",

        "Información general"

    ]


    opcion = tk.StringVar()

    opcion.set(
        opciones[0]
    )


    menu = tk.OptionMenu(
        ventana,
        opcion,
        *opciones
    )


    menu.config(
        width=30,
        font=("Arial", 11),
        bg="#FFFFFF",
        fg="#123A5B",
        highlightbackground="#D5E8FF",
        activebackground="#D5E8FF"
    )

    menu.pack(
        pady=15
    )


    def consultar():

        messagebox.showinfo(
            "Farmacia",
            f"Opción seleccionada:\n\n"
            f"{opcion.get()}\n\n"
            f"Consulta con el personal de farmacia."
        )


    tk.Button(
        ventana,
        text="Continuar",
        command=consultar,
        font=("Arial", 12, "bold"),
        width=20,
        bg="#5A67D8",
        fg="white",
        activebackground="#454FB5",
        activeforeground="white",
        relief="flat",
        bd=0
    ).pack(
        pady=20
    )


    tk.Button(
        ventana,
        text="Cerrar",
        command=ventana.destroy,
        width=15,
        bg="#E63946",
        fg="white",
        activebackground="#C62F3C",
        activeforeground="white",
        relief="flat",
        bd=0
    ).pack()


# ==========================================
# RAYOS X
# ==========================================

def abrir_rayos_x():

    ventana = tk.Toplevel(root)

    ventana.title(
        "Rayos X"
    )

    ventana.geometry(
        "500x400"
    )

    ventana.resizable(
        False,
        False
    )

    ventana.configure(
        bg="#EAF4FF"
    )


    tk.Label(
        ventana,
        text="RAYOS X",
        font=("Arial", 22, "bold"),
        bg="#EAF4FF",
        fg="#123A5B"
    ).pack(
        pady=20
    )


    tk.Label(
        ventana,
        text="Área de estudios de Rayos X",
        font=("Arial", 13),
        bg="#EAF4FF",
        fg="#234D69"
    ).pack(
        pady=20
    )


    tk.Label(
        ventana,
        text="Para realizar este estudio,\n"
             "se requiere indicación médica.",
        font=("Arial", 12),
        justify="center",
        bg="#EAF4FF",
        fg="#234D69"
    ).pack(
        pady=10
    )


    tk.Button(
        ventana,
        text="Solicitar información",
        command=lambda: messagebox.showinfo(
            "Rayos X",
            "Consulta con el personal médico "
            "para determinar si este estudio es necesario."
        ),
        width=25,
        bg="#00A6A6",
        fg="white",
        activebackground="#008C8C",
        activeforeground="white",
        relief="flat",
        bd=0
    ).pack(
        pady=20
    )


# ==========================================
# TOMOGRAFÍA
# ==========================================

def abrir_tomografia():

    ventana = tk.Toplevel(root)

    ventana.title(
        "Tomografía"
    )

    ventana.geometry(
        "500x400"
    )

    ventana.resizable(
        False,
        False
    )

    ventana.configure(
        bg="#EAF4FF"
    )


    tk.Label(
        ventana,
        text="TOMOGRAFÍA",
        font=("Arial", 22, "bold"),
        bg="#EAF4FF",
        fg="#123A5B"
    ).pack(
        pady=20
    )


    tk.Label(
        ventana,
        text="Área de Tomografía",
        font=("Arial", 13),
        bg="#EAF4FF",
        fg="#234D69"
    ).pack(
        pady=20
    )


    tk.Label(
        ventana,
        text="La tomografía debe realizarse "
             "con indicación médica.",
        font=("Arial", 12),
        justify="center",
        bg="#EAF4FF",
        fg="#234D69"
    ).pack(
        pady=10
    )


    tk.Button(
        ventana,
        text="Solicitar información",
        command=lambda: messagebox.showinfo(
            "Tomografía",
            "Consulta con el personal médico "
            "si este estudio es necesario."
        ),
        width=25,
        bg="#3A86FF",
        fg="white",
        activebackground="#2E6DCC",
        activeforeground="white",
        relief="flat",
        bd=0
    ).pack(
        pady=20
    )


# ==========================================
# ESTUDIOS
# ==========================================

def abrir_estudios():

    ventana = tk.Toplevel(root)

    ventana.title(
        "Estudios"
    )

    ventana.geometry(
        "500x450"
    )

    ventana.resizable(
        False,
        False
    )

    ventana.configure(
        bg="#EAF4FF"
    )


    tk.Label(
        ventana,
        text="ESTUDIOS",
        font=("Arial", 22, "bold"),
        bg="#EAF4FF",
        fg="#123A5B"
    ).pack(
        pady=20
    )


    tk.Label(
        ventana,
        text="Selecciona el estudio:",
        font=("Arial", 13),
        bg="#EAF4FF",
        fg="#234D69"
    ).pack(
        pady=15
    )


    tk.Button(
        ventana,
        text="Rayos X",
        command=abrir_rayos_x,
        width=25,
        height=2,
        font=("Arial", 12),
        bg="#00A6A6",
        fg="white",
        activebackground="#008C8C",
        activeforeground="white",
        relief="flat",
        bd=0
    ).pack(
        pady=10
    )


    tk.Button(
        ventana,
        text="Tomografía",
        command=abrir_tomografia,
        width=25,
        height=2,
        font=("Arial", 12),
        bg="#3A86FF",
        fg="white",
        activebackground="#2E6DCC",
        activeforeground="white",
        relief="flat",
        bd=0
    ).pack(
        pady=10
    )


    tk.Button(
        ventana,
        text="Cerrar",
        command=ventana.destroy,
        width=15,
        bg="#E63946",
        fg="white",
        activebackground="#C62F3C",
        activeforeground="white",
        relief="flat",
        bd=0
    ).pack(
        pady=20
    )


# ==========================================
# NUEVO PACIENTE
# ==========================================

def limpiar():

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


    resultado_texto.config(
        state="normal"
    )

    resultado_texto.delete(
        "1.0",
        tk.END
    )

    resultado_texto.config(
        state="disabled"
    )


    datos_cita.clear()


# ==========================================
# VENTANA PRINCIPAL
# ==========================================

root = tk.Tk()

root.title(
    "Asistente Hospitalario IA"
)

root.geometry(
    "950x850"
)

root.resizable(
    False,
    False
)

root.configure(
    bg="#EAF4FF"
)


# Diccionario para almacenar la cita

datos_cita = {}


# ==========================================
# TÍTULO
# ==========================================

titulo = tk.Label(
    root,
    text="ASISTENTE HOSPITALARIO",
    font=("Arial", 26, "bold"),
    bg="#EAF4FF",
    fg="#123A5B"
)

titulo.pack(
    pady=15
)


subtitulo = tk.Label(
    root,
    text="Sistema de orientación y gestión hospitalaria",
    font=("Arial", 12),
    bg="#EAF4FF",
    fg="#234D69"
)

subtitulo.pack(
    pady=5
)


# ==========================================
# CONTENEDOR PRINCIPAL
# ==========================================

frame_principal = tk.Frame(
    root
)

frame_principal.pack(
    pady=15
)


# ==========================================
# DATOS DEL PACIENTE
# ==========================================

frame_datos = tk.LabelFrame(
    frame_principal,
    text="Datos del paciente",
    font=("Arial", 13, "bold"),
    padx=20,
    pady=15
)

frame_datos.grid(
    row=0,
    column=0,
    padx=15,
    sticky="n"
)


# ==========================================
# NOMBRE
# ==========================================

tk.Label(
    frame_datos,
    text="Nombre:"
).grid(
    row=0,
    column=0,
    sticky="w",
    pady=8
)


entrada_nombre = tk.Entry(
    frame_datos,
    width=30
)

entrada_nombre.grid(
    row=0,
    column=1,
    pady=8
)


# ==========================================
# EDAD
# ==========================================

tk.Label(
    frame_datos,
    text="Edad:"
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=8
)


entrada_edad = tk.Entry(
    frame_datos,
    width=30
)

entrada_edad.grid(
    row=1,
    column=1,
    pady=8
)


# ==========================================
# OXIGENACIÓN
# ==========================================

tk.Label(
    frame_datos,
    text="Oxigenación (%):"
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=8
)


entrada_oxigenacion = tk.Entry(
    frame_datos,
    width=30
)

entrada_oxigenacion.grid(
    row=2,
    column=1,
    pady=8
)


# ==========================================
# FRECUENCIA CARDIACA
# ==========================================

tk.Label(
    frame_datos,
    text="Frecuencia cardiaca:"
).grid(
    row=3,
    column=0,
    sticky="w",
    pady=8
)


entrada_frecuencia = tk.Entry(
    frame_datos,
    width=30
)

entrada_frecuencia.grid(
    row=3,
    column=1,
    pady=8
)


# ==========================================
# PRESIÓN
# ==========================================

tk.Label(
    frame_datos,
    text="Presión arterial:"
).grid(
    row=4,
    column=0,
    sticky="w",
    pady=8
)


entrada_presion = tk.Entry(
    frame_datos,
    width=30
)

entrada_presion.insert(
    0,
    "120/80"
)

entrada_presion.grid(
    row=4,
    column=1,
    pady=8
)


# ==========================================
# PESO
# ==========================================

tk.Label(
    frame_datos,
    text="Peso (kg):"
).grid(
    row=5,
    column=0,
    sticky="w",
    pady=8
)


entrada_peso = tk.Entry(
    frame_datos,
    width=30
)

entrada_peso.grid(
    row=5,
    column=1,
    pady=8
)


# ==========================================
# TALLA
# ==========================================

tk.Label(
    frame_datos,
    text="Talla (cm):"
).grid(
    row=6,
    column=0,
    sticky="w",
    pady=8
)


entrada_talla = tk.Entry(
    frame_datos,
    width=30
)

entrada_talla.grid(
    row=6,
    column=1,
    pady=8
)


# ==========================================
# BOTONES
# ==========================================

frame_botones = tk.Frame(
    frame_principal
)

frame_botones.grid(
    row=0,
    column=1,
    padx=15,
    sticky="n"
)


# ==========================================
# DIAGNÓSTICO
# ==========================================

tk.Button(
    frame_botones,
    text="Realizar diagnóstico",
    command=realizar_diagnostico,
    width=25,
    height=2,
    font=("Arial", 11, "bold"),
    bg="#1F6FEB",
    fg="white",
    activebackground="#184FA5",
    activeforeground="white",
    relief="flat",
    bd=0
).pack(
    pady=8
)


# ==========================================
# URGENCIAS
# ==========================================

tk.Button(
    frame_botones,
    text="Urgencias",
    command=abrir_urgencias,
    width=25,
    height=2,
    bg="#2B7A78",
    fg="white",
    activebackground="#215D5A",
    activeforeground="white",
    relief="flat",
    bd=0
).pack(
    pady=8
)


# ==========================================
# CITA
# ==========================================

tk.Button(
    frame_botones,
    text="Cita",
    command=abrir_cita,
    width=25,
    height=2,
    bg="#3A86FF",
    fg="white",
    activebackground="#2E6DCC",
    activeforeground="white",
    relief="flat",
    bd=0
).pack(
    pady=8
)


# ==========================================
# FARMACIA
# ==========================================

tk.Button(
    frame_botones,
    text="Farmacia",
    command=abrir_farmacia,
    width=25,
    height=2,
    bg="#5A67D8",
    fg="white",
    activebackground="#454FB5",
    activeforeground="white",
    relief="flat",
    bd=0
).pack(
    pady=8
)


# ==========================================
# ESTUDIOS
# ==========================================

tk.Button(
    frame_botones,
    text="Estudios",
    command=abrir_estudios,
    width=25,
    height=2,
    bg="#00A6A6",
    fg="white",
    activebackground="#008C8C",
    activeforeground="white",
    relief="flat",
    bd=0
).pack(
    pady=8
)


# ==========================================
# NUEVO PACIENTE
# ==========================================

tk.Button(
    frame_botones,
    text="Nuevo paciente",
    command=limpiar,
    width=25,
    height=2,
    bg="#7C4DFF",
    fg="white",
    activebackground="#5E3CCB",
    activeforeground="white",
    relief="flat",
    bd=0
).pack(
    pady=8
)


# ==========================================
# CRUD - CONSULTAR
# ==========================================

tk.Button(
    frame_botones,
    text="Consultar paciente",
    command=consultar_paciente,
    width=25,
    height=2,
    bg="#00A6A6",
    fg="white",
    relief="flat",
    bd=0
).pack(
    pady=8
)


# ==========================================
# CRUD - ACTUALIZAR
# ==========================================

tk.Button(
    frame_botones,
    text="Actualizar paciente",
    command=actualizar_desde_ventana,
    width=25,
    height=2,
    bg="#3A86FF",
    fg="white",
    relief="flat",
    bd=0
).pack(
    pady=8
)


# ==========================================
# CRUD - ELIMINAR
# ==========================================

tk.Button(
    frame_botones,
    text="Eliminar paciente",
    command=eliminar_desde_ventana,
    width=25,
    height=2,
    bg="#E63946",
    fg="white",
    relief="flat",
    bd=0
).pack(
    pady=8
)


# ==========================================
# SALIR
# ==========================================

tk.Button(
    frame_botones,
    text="Salir",
    command=root.destroy,
    width=25,
    height=2,
    bg="#E63946",
    fg="white",
    activebackground="#C62F3C",
    activeforeground="white",
    relief="flat",
    bd=0
).pack(
    pady=8
)


# ==========================================
# RESULTADOS
# ==========================================

frame_resultado = tk.LabelFrame(
    root,
    text="Resultado del asistente",
    font=("Arial", 13, "bold"),
    padx=10,
    pady=10
)

frame_resultado.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)


resultado_texto = tk.Text(
    frame_resultado,
    height=12,
    width=100,
    font=("Consolas", 10),
    wrap="word"
)

resultado_texto.pack(
    fill="both",
    expand=True
)


resultado_texto.config(
    state="disabled"
)


# ==========================================
# PIE DE PÁGINA
# ==========================================

tk.Label(
    root,
    text="Sistema académico de simulación hospitalaria",
    font=("Arial", 9)
).pack(
    pady=5
)


# ==========================================
# INICIAR PROGRAMA
# ==========================================

root.mainloop()
