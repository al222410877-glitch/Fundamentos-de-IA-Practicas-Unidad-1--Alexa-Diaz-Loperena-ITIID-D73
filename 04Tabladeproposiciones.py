import tkinter as tk
from tkinter import messagebox


def generar_tabla():
    try:
        num_proposiciones = int(entrada.get())
    except ValueError:
        messagebox.showwarning("Entrada inválida", "Escribe un número entero válido.")
        return

    if num_proposiciones <= 0:
        messagebox.showwarning("Entrada inválida", "Debe ser un número mayor que 0.")
        return

    valores = [True, False]
    proposiciones = [chr(80 + i) for i in range(num_proposiciones)]

    def tabla(posicion, resultado, filas):
        if posicion == num_proposiciones:
            and_resultado = all(resultado)
            or_resultado = any(resultado)
            not_resultado = not resultado[0]

            filas.append(
                "\t".join(map(str, resultado))
                + f"\t{and_resultado}\t{or_resultado}\t{not_resultado}"
            )
            return

        for valor in valores:
            tabla(posicion + 1, resultado + [valor], filas)

    filas = []
    tabla(0, [], filas)

    salida.configure(state="normal")
    salida.delete("1.0", tk.END)

    encabezado = "\t".join(proposiciones) + "\tAND\tOR\tNOT"
    salida.insert(tk.END, encabezado + "\n")
    salida.insert(tk.END, "-" * len(encabezado) + "\n")

    for fila in filas:
        salida.insert(tk.END, fila + "\n")

    salida.configure(state="disabled")


root = tk.Tk()
root.title("Tabla de verdad")
root.geometry("760x500")
root.configure(bg="#eaf4ff")

frame = tk.Frame(root, bg="#eaf4ff", padx=20, pady=20)
frame.pack(fill="both", expand=True)

lbl_titulo = tk.Label(
    frame,
    text="TABLA DE VERDAD",
    font=("Arial", 20, "bold"),
    bg="#eaf4ff",
    fg="#143d5b"
)
lbl_titulo.pack(pady=(0, 15))

entrada_frame = tk.Frame(frame, bg="#eaf4ff")
entrada_frame.pack(fill="x", pady=(0, 10))

lbl = tk.Label(
    entrada_frame,
    text="Número de proposiciones:",
    font=("Arial", 11, "bold"),
    bg="#eaf4ff",
    fg="#1d3557"
)
lbl.pack(side="left", padx=(0, 10))

entrada = tk.Entry(
    entrada_frame,
    width=10,
    font=("Arial", 11),
    bg="#ffffff",
    fg="#0b132b",
    bd=2,
    relief="solid"
)
entrada.pack(side="left")
entrada.insert(0, "2")

boton = tk.Button(
    frame,
    text="Generar tabla",
    command=generar_tabla,
    width=18,
    height=2,
    bg="#1f6feb",
    fg="white",
    font=("Arial", 11, "bold"),
    activebackground="#184fa5",
    activeforeground="white",
    relief="flat",
    bd=0
)
boton.pack(pady=(5, 15))

salida = tk.Text(
    frame,
    width=90,
    height=18,
    wrap="none",
    bg="#f8fbff",
    fg="#102a43",
    font=("Consolas", 10),
    relief="solid",
    bd=1
)
salida.pack(fill="both", expand=True)
salida.configure(state="disabled")

root.mainloop()