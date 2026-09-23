import tkinter as tk
from tkinter import ttk


def calcular_resultado(asistencia, promedio, proyecto, autorizacion, lista_oficial):
    P = asistencia >= 80
    Q = promedio >= 7
    R = proyecto == "si"
    S = autorizacion == "si"
    T = lista_oficial == "si"
    negacion_P = not P
    conjuncion = P and Q
    disyuncion = Q or S
    condicional = (not P) or Q
    bicondicional = P == Q
    expresion = (P and Q and T) or S

    return {
        "P": P,
        "Q": Q,
        "R": R,
        "S": S,
        "T": T,
        "negacion_P": negacion_P,
        "conjuncion": conjuncion,
        "disyuncion": disyuncion,
        "condicional": condicional,
        "bicondicional": bicondicional,
        "expresion": expresion,
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
    autorizacion = combo_autorizacion.get().lower()
    lista_oficial = combo_lista.get().lower()

    datos = calcular_resultado(asistencia, promedio, proyecto, autorizacion, lista_oficial)

    salida = ""
    salida += "=" * 60 + "\n"
    salida += "        SISTEMA DE AUTORIZACIÓN PARA EXAMEN FINAL\n"
    salida += "=" * 60 + "\n\n"
    salida += f"P - Asistencia suficiente: {datos['P']}\n"
    salida += f"Q - Promedio aprobatorio: {datos['Q']}\n"
    salida += f"R - Proyecto entregado: {datos['R']}\n"
    salida += f"S - Autorización especial: {datos['S']}\n"
    salida += f"T - Aparece en la lista oficial: {datos['T']}\n\n"
    salida += f"¬P = {datos['negacion_P']}\n"
    salida += f"P ∧ Q = {datos['conjuncion']}\n"
    salida += f"Q ∨ S = {datos['disyuncion']}\n"
    salida += f"P → Q = {datos['condicional']}\n"
    salida += f"P ↔ Q = {datos['bicondicional']}\n"
    salida += f"(P ∧ Q ∧ T) ∨ S = {datos['expresion']}\n\n"
    salida += "=" * 60 + "\n"
    if datos['expresion']:
        salida += "El alumno PUEDE presentar el examen.\n"
    else:
        salida += "El alumno NO puede presentar el examen.\n"
    salida += "=" * 60 + "\n"

    texto_resultado.delete("1.0", tk.END)
    texto_resultado.insert(tk.END, salida)


root = tk.Tk()
root.title("Sistema de autorización")
root.geometry("860x680")
root.configure(bg="#edf6ff")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#edf6ff", foreground="#103a5a", font=("Arial", 10, "bold"))
style.configure("TEntry", fieldbackground="#ffffff", foreground="#103a5a")
style.configure("TCombobox", fieldbackground="#ffffff", foreground="#103a5a")
style.configure("TButton", background="#2d7ff9", foreground="white", font=("Arial", 10, "bold"), padding=(10, 8))
style.map("TButton", background=[("active", "#1b5fc4")], foreground=[("active", "white")])

frame = tk.Frame(root, bg="#edf6ff", padx=22, pady=20)
frame.pack(fill="both", expand=True)

header = tk.Label(
    frame,
    text="SISTEMA DE AUTORIZACIÓN PARA EXAMEN FINAL",
    font=("Arial", 22, "bold"),
    bg="#edf6ff",
    fg="#103a5a",
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

lbl_autorizacion = ttk.Label(panel, text="¿Tiene autorización especial?")
lbl_autorizacion.grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
combo_autorizacion = ttk.Combobox(panel, values=["si", "no"], state="readonly", width=22)
combo_autorizacion.set("no")
combo_autorizacion.grid(row=3, column=1, sticky="w", pady=8)

lbl_lista = ttk.Label(panel, text="¿Aparece en la lista oficial?")
lbl_lista.grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
combo_lista = ttk.Combobox(panel, values=["si", "no"], state="readonly", width=22)
combo_lista.set("si")
combo_lista.grid(row=4, column=1, sticky="w", pady=8)

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
    height=20,
    width=92,
    bg="#f6fbff",
    fg="#103a5a",
    font=("Consolas", 10),
    wrap="word",
    relief="solid",
    bd=1,
)
texto_resultado.pack(fill="both", expand=True)

texto_resultado.insert(tk.END, "Ingresa los datos y presiona Evaluar.\n")

root.mainloop()