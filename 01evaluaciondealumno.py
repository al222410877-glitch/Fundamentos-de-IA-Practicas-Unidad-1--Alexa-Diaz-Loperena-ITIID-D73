import tkinter as tk
from tkinter import ttk


def evaluar_alumno(asistencia, promedio, proyecto):
    P = asistencia >= 80
    Q = promedio >= 8
    R = proyecto == "si"
    resultado = P and Q and R
    return P, Q, R, resultado


def procesar():
    try:
        asistencia = float(entry_asistencia.get())
        promedio = float(entry_promedio.get())
    except ValueError:
        texto_resultado.delete("1.0", tk.END)
        texto_resultado.insert(tk.END, "Ingresa valores numéricos válidos.")
        return

    proyecto = combo_proyecto.get().lower()
    P, Q, R, resultado = evaluar_alumno(asistencia, promedio, proyecto)

    salida = ""
    salida += "=" * 55 + "\n"
    salida += "      SISTEMA DE EVALUACIÓN DEL ALUMNO\n"
    salida += "=" * 55 + "\n\n"
    salida += f"P - Asistencia suficiente: {P}\n"
    salida += f"Q - Promedio aprobatorio: {Q}\n"
    salida += f"R - Proyecto entregado: {R}\n\n"
    salida += "=" * 55 + "\n"
    if resultado:
        salida += "El alumno PUEDE presentar el examen final.\n"
    else:
        salida += "El alumno NO puede presentar el examen final.\n"
    salida += "=" * 55 + "\n"

    texto_resultado.delete("1.0", tk.END)
    texto_resultado.insert(tk.END, salida)


root = tk.Tk()
root.title("Evaluación de alumno")
root.geometry("780x520")
root.configure(bg="#edf6ff")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#edf6ff", foreground="#143d5b", font=("Arial", 10, "bold"))
style.configure("TEntry", fieldbackground="#ffffff", foreground="#143d5b")
style.configure("TCombobox", fieldbackground="#ffffff", foreground="#143d5b")
style.configure("TButton", background="#2f7df6", foreground="white", font=("Arial", 10, "bold"), padding=(10, 8))
style.map("TButton", background=[("active", "#1d63c8")], foreground=[("active", "white")])

frame = tk.Frame(root, bg="#edf6ff", padx=20, pady=20)
frame.pack(fill="both", expand=True)

header = tk.Label(
    frame,
    text="SISTEMA DE EVALUACIÓN DEL ALUMNO",
    font=("Arial", 22, "bold"),
    bg="#edf6ff",
    fg="#143d5b",
    pady=8,
)
header.pack(fill="x", pady=(0, 18))

panel = tk.LabelFrame(
    frame,
    text="Datos",
    padx=15,
    pady=15,
    bg="#ffffff",
    fg="#1b4d72",
    font=("Arial", 10, "bold"),
    highlightbackground="#bfe0ff",
    highlightthickness=2,
)
panel.pack(fill="x", pady=(0, 12))

lbl_asistencia = ttk.Label(panel, text="Porcentaje de asistencia:")
lbl_asistencia.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=8)
entry_asistencia = ttk.Entry(panel, width=24)
entry_asistencia.grid(row=0, column=1, sticky="w", pady=8)

lbl_promedio = ttk.Label(panel, text="Promedio del alumno:")
lbl_promedio.grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
entry_promedio = ttk.Entry(panel, width=24)
entry_promedio.grid(row=1, column=1, sticky="w", pady=8)

lbl_proyecto = ttk.Label(panel, text="¿Entregó el proyecto?")
lbl_proyecto.grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
combo_proyecto = ttk.Combobox(panel, values=["si", "no"], state="readonly", width=22)
combo_proyecto.set("si")
combo_proyecto.grid(row=2, column=1, sticky="w", pady=8)

btn = ttk.Button(frame, text="Evaluar", command=procesar)
btn.pack(pady=(0, 12))

resultado_frame = tk.LabelFrame(
    frame,
    text="Resultado",
    padx=12,
    pady=12,
    bg="#ffffff",
    fg="#1b4d72",
    font=("Arial", 10, "bold"),
    highlightbackground="#bfe0ff",
    highlightthickness=2,
)
resultado_frame.pack(fill="both", expand=True)

texto_resultado = tk.Text(
    resultado_frame,
    height=14,
    width=88,
    bg="#f7fbff",
    fg="#143d5b",
    font=("Consolas", 10),
    wrap="word",
    relief="solid",
    bd=1,
)
texto_resultado.pack(fill="both", expand=True)

texto_resultado.insert(tk.END, "Ingresa los datos y presiona Evaluar.\n")

root.mainloop()