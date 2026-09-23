import tkinter as tk
from tkinter import ttk


def calcular_resultado(asistencia, promedio, proyecto, adeudos, autorizacion, lista_oficial):
    P = asistencia >= 80
    Q = promedio >= 8
    R = proyecto == "si"
    S = adeudos == "no"
    T = autorizacion == "si"
    U = lista_oficial == "si"

    no_P = not P
    conjuncion = P and Q
    disyuncion = Q or T
    condicional = (not P) or Q
    bicondicional = P == Q
    resultado = ((P and Q and R and S) or T) and U
    autorizacion_correcta = T == U

    return {
        "P": P,
        "Q": Q,
        "R": R,
        "S": S,
        "T": T,
        "U": U,
        "no_P": no_P,
        "conjuncion": conjuncion,
        "disyuncion": disyuncion,
        "condicional": condicional,
        "bicondicional": bicondicional,
        "resultado": resultado,
        "autorizacion_correcta": autorizacion_correcta,
    }


def evaluar():
    try:
        asistencia = float(entry_asistencia.get())
        promedio = float(entry_promedio.get())
    except ValueError:
        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, "Ingresa valores numéricos válidos.")
        return

    proyecto = combo_proyecto.get().lower()
    adeudos = combo_adeudos.get().lower()
    autorizacion = combo_autorizacion.get().lower()
    lista_oficial = combo_lista.get().lower()

    datos = calcular_resultado(asistencia, promedio, proyecto, adeudos, autorizacion, lista_oficial)

    salida = ""
    salida += "=" * 60 + "\n"
    salida += "          SISTEMA DE AUTORIZACIÓN PARA EXAMEN\n"
    salida += "=" * 60 + "\n\n"
    salida += f"P - Asistencia suficiente: {datos['P']}\n"
    salida += f"Q - Promedio aprobatorio: {datos['Q']}\n"
    salida += f"R - Proyecto entregado: {datos['R']}\n"
    salida += f"S - Sin adeudos: {datos['S']}\n"
    salida += f"T - Autorización especial: {datos['T']}\n"
    salida += f"U - Aparece en lista: {datos['U']}\n\n"
    salida += f"¬P = {datos['no_P']}\n"
    salida += f"P ∧ Q = {datos['conjuncion']}\n"
    salida += f"Q ∨ T = {datos['disyuncion']}\n"
    salida += f"P → Q = {datos['condicional']}\n"
    salida += f"P ↔ Q = {datos['bicondicional']}\n"
    salida += f"((P ∧ Q ∧ R ∧ S) ∨ T) ∧ U = {datos['resultado']}\n"
    salida += f"T ↔ U = {datos['autorizacion_correcta']}\n\n"
    salida += "=" * 60 + "\n"
    if datos['resultado']:
        salida += "El alumno PUEDE presentar el examen.\n"
    else:
        salida += "El alumno NO puede presentar el examen.\n"

    if datos['autorizacion_correcta']:
        salida += "La autorización COINCIDE con la lista oficial.\n"
    else:
        salida += "ADVERTENCIA: La autorización NO coincide con la lista oficial.\n"
    salida += "=" * 60 + "\n"

    texto_resultado.delete("1.0", tk.END)
    texto_resultado.insert(tk.END, salida)


root = tk.Tk()
root.title("Sistema de autorización")
root.geometry("850x680")
root.configure(bg="#eaf4ff")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#eaf4ff", foreground="#123b5c", font=("Arial", 10, "bold"))
style.configure("TEntry", fieldbackground="#ffffff", foreground="#123b5c")
style.configure("TCombobox", fieldbackground="#ffffff", foreground="#123b5c")
style.configure("TButton", background="#2a7de1", foreground="white", font=("Arial", 10, "bold"), padding=(10, 8))
style.map("TButton", background=[("active", "#1e5fb7")], foreground=[("active", "white")])

frame = tk.Frame(root, bg="#eaf4ff", padx=22, pady=20)
frame.pack(fill="both", expand=True)

header = tk.Label(
    frame,
    text="SISTEMA DE AUTORIZACIÓN PARA EXAMEN",
    font=("Arial", 22, "bold"),
    bg="#eaf4ff",
    fg="#123b5c",
    pady=10,
)
header.pack(fill="x", pady=(0, 18))

panel = tk.LabelFrame(
    frame,
    text="Datos del alumno",
    padx=15,
    pady=15,
    bg="#ffffff",
    fg="#1b4d72",
    font=("Arial", 10, "bold"),
    highlightbackground="#b9d8ff",
    highlightthickness=2,
)
panel.pack(fill="x", pady=(0, 12))

lbl_asistencia = ttk.Label(panel, text="Porcentaje de asistencia:")
lbl_asistencia.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=8)
entry_asistencia = ttk.Entry(panel, width=24)
entry_asistencia.grid(row=0, column=1, sticky="w", pady=8)

lbl_promedio = ttk.Label(panel, text="Promedio:")
lbl_promedio.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
entry_promedio = ttk.Entry(panel, width=24)
entry_promedio.grid(row=1, column=1, sticky="w", pady=8)

lbl_proyecto = ttk.Label(panel, text="¿Entregó el proyecto?")
lbl_proyecto.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
combo_proyecto = ttk.Combobox(panel, values=["si", "no"], state="readonly", width=22)
combo_proyecto.set("si")
combo_proyecto.grid(row=2, column=1, sticky="w", pady=8)

lbl_adeudos = ttk.Label(panel, text="¿Tiene adeudos?")
lbl_adeudos.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
combo_adeudos = ttk.Combobox(panel, values=["si", "no"], state="readonly", width=22)
combo_adeudos.set("no")
combo_adeudos.grid(row=3, column=1, sticky="w", pady=8)

lbl_autorizacion = ttk.Label(panel, text="¿Tiene autorización especial?")
lbl_autorizacion.grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
combo_autorizacion = ttk.Combobox(panel, values=["si", "no"], state="readonly", width=22)
combo_autorizacion.set("no")
combo_autorizacion.grid(row=4, column=1, sticky="w", pady=8)

lbl_lista = ttk.Label(panel, text="¿Aparece en la lista oficial?")
lbl_lista.grid(row=5, column=0, sticky="w", padx=(0, 10), pady=8)
combo_lista = ttk.Combobox(panel, values=["si", "no"], state="readonly", width=22)
combo_lista.set("si")
combo_lista.grid(row=5, column=1, sticky="w", pady=8)

btn = ttk.Button(frame, text="Evaluar", command=evaluar)
btn.pack(pady=(0, 12))

resultado = tk.LabelFrame(
    frame,
    text="Resultado",
    padx=12,
    pady=12,
    bg="#ffffff",
    fg="#1b4d72",
    font=("Arial", 10, "bold"),
    highlightbackground="#b9d8ff",
    highlightthickness=2,
)
resultado.pack(fill="both", expand=True)

texto_resultado = tk.Text(
    resultado,
    height=22,
    width=95,
    bg="#f7fbff",
    fg="#123b5c",
    font=("Consolas", 10),
    wrap="word",
    relief="solid",
    bd=1,
)
texto_resultado.pack(fill="both", expand=True)

texto_resultado.insert(tk.END, "Ingresa los datos y presiona Evaluar.\n")

root.mainloop()