# ============================================================
# BÚSQUEDA VISUAL E INTERACTIVA (Colores vivos y nodo E integrado)
# ============================================================

import tkinter as tk
from tkinter import messagebox, scrolledtext
import time

# Grafo ajustado para que el nodo E sí sea alcanzado y participe en las rutas
acciones = {
    "A": ["B", "D"],
    "B": ["C", "E"],
    "C": ["D", "F"],
    "D": ["A", "E", "F"],
    "E": ["B", "D", "F"],
    "F": ["C", "E"]
}

estado_inicial = "A"
estado_objetivo = "F"

# Coordenadas reubicadas para incluir bien al nodo E en el mapa visual
coordenadas_nodos = {
    "A": (80, 140),
    "B": (200, 60),
    "C": (320, 60),
    "D": (200, 220),
    "E": (320, 220),
    "F": (440, 140)
}

def buscar_todas_las_rutas(actual, objetivo, camino_actual, orden_exploracion, todas_las_rutas, limite, pasos_simples):
    pasos_simples.append(f"• Pasando por '{actual}' (Ruta: {' → '.join(camino_actual)})")

    if actual not in orden_exploracion:
        orden_exploracion.append(actual)

    if len(camino_actual) > limite:
        pasos_simples.append(f"  (Límite alcanzado, regresamos).")
        return

    if actual == objetivo:
        todas_las_rutas.append(list(camino_actual))
        pasos_simples.append(f"  ★ ¡Meta alcanzada! Ruta: {' → '.join(camino_actual)}")
        return

    for vecino in acciones.get(actual, []):
        if vecino not in camino_actual:
            camino_actual.append(vecino)
            buscar_todas_las_rutas(vecino, objetivo, camino_actual, orden_exploracion, todas_las_rutas, limite, pasos_simples)
            camino_actual.pop()
        else:
            pasos_simples.append(f"  (Evitamos ciclo en '{vecino}').")

def dibujar_grafo(nodo_activo=None, ruta_estatica=None):
    canvas.delete("all")
    
    # 1. Dibujar líneas del grafo
    for nodo, vecinos in acciones.items():
        x1, y1 = coordenadas_nodos[nodo]
        for vecino in vecinos:
            if vecino in coordenadas_nodos:
                x2, y2 = coordenadas_nodos[vecino]
                
                es_parte_ruta = False
                if ruta_estatica and len(ruta_estatica) > 1:
                    for i in range(len(ruta_estatica) - 1):
                        if (ruta_estatica[i] == nodo and ruta_estatica[i+1] == vecino) or \
                           (ruta_estatica[i] == vecino and ruta_estatica[i+1] == nodo):
                            es_parte_ruta = True
                            break
                
                color_linea = "#FF69B4" if es_parte_ruta else "#BDC3C7"  # Rosa más fuerte para la ruta
                grosor = 4 if es_parte_ruta else 2
                canvas.create_line(x1, y1, x2, y2, fill=color_linea, width=grosor)

    # 2. Dibujar nodos con colores más vivos
    for nodo, (x, y) in coordenadas_nodos.items():
        if nodo == estado_inicial:
            color_relleno = "#2ECC71"  # Verde más vivo
        elif nodo == estado_objetivo:
            color_relleno = "#FF69B4"  # Rosa fuerte
        else:
            color_relleno = "#9B59B6"  # Lila más intenso
            
        outline_color = "#E74C3C" if nodo == nodo_activo else "#2C3E50"
        grosor_borde = 4 if nodo == nodo_activo else 2
            
        radio = 24
        canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill=color_relleno, outline=outline_color, width=grosor_borde)
        canvas.create_text(x, y, text=nodo, font=("Arial", 13, "bold"), fill="#FFFFFF")

def ejecutar_busqueda():
    try:
        limite = int(entry_limite.get())
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido para el límite.")
        return

    orden_exploracion = []
    todas_las_rutas = []
    pasos_simples = []
    camino_inicial = [estado_inicial]

    buscar_todas_las_rutas(
        estado_inicial, 
        estado_objetivo, 
        camino_inicial, 
        orden_exploracion, 
        todas_las_rutas, 
        limite,
        pasos_simples
    )

    # Mostrar explicación muy directa y corta
    txt_resultados.config(state=tk.NORMAL)
    txt_resultados.delete("1.0", tk.END)
    
    txt_resultados.insert(tk.END, "=== RESUMEN DE BÚSQUEDA ===\n\n")
    for paso in pasos_simples:
        txt_resultados.insert(tk.END, paso + "\n")
        
    txt_resultados.insert(tk.END, "\n" + "─"*35 + "\n")
    txt_resultados.insert(tk.END, f"Rutas totales encontradas: {len(todas_las_rutas)}\n")
    for i, ruta in enumerate(todas_las_rutas, 1):
        txt_resultados.insert(tk.END, f"Ruta {i}: {' → '.join(ruta)}\n")
    txt_resultados.config(state=tk.DISABLED)

    # Animación y marcado de la última ruta final
    if todas_las_rutas:
        ruta_animar = todas_las_rutas[0]
        for nodo_actual in ruta_animar:
            dibujar_grafo(nodo_activo=nodo_actual)
            root.update()
            time.sleep(0.35)
        
        ultima_ruta = todas_las_rutas[-1]
        dibujar_grafo(nodo_activo=None, ruta_estatica=ultima_ruta)

# ============================================================
# CONFIGURACIÓN DE LA VENTANA (DOS COLUMNAS)
# ============================================================

root = tk.Tk()
root.title("Búsqueda de Rutas - Interfaz Interactiva")
root.geometry("880x540")
root.config(bg="#F9F6F0")

COLOR_LILA_VIVO = "#9B59B6"
COLOR_VERDE_VIVO = "#2ECC71"
COLOR_TEXTO = "#2C3E50"

# Título superior
lbl_titulo = tk.Label(
    root, 
    text="Explorador de Rutas y Control de Ciclos", 
    font=("Arial", 16, "bold"), 
    bg="#F9F6F0", 
    fg=COLOR_TEXTO
)
lbl_titulo.pack(pady=10)

# Controles superiores
frame_controles = tk.Frame(root, bg="#F9F6F0")
frame_controles.pack(pady=5)

tk.Label(frame_controles, text="Límite de Profundidad:", font=("Arial", 11, "bold"), bg="#F9F6F0", fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5)
entry_limite = tk.Entry(frame_controles, font=("Arial", 11), width=5, justify="center")
entry_limite.insert(0, "5")
entry_limite.pack(side=tk.LEFT, padx=5)

btn_ejecutar = tk.Button(
    frame_controles, 
    text="Iniciar Búsqueda", 
    command=ejecutar_busqueda, 
    font=("Arial", 11, "bold"), 
    bg=COLOR_LILA_VIVO, 
    fg="#FFFFFF",
    padx=12, 
    pady=4
)
btn_ejecutar.pack(side=tk.LEFT, padx=15)

# Marco principal en DOS COLUMNAS
frame_principal = tk.Frame(root, bg="#F9F6F0")
frame_principal.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)

# Columna Izquierda: Texto resumido
frame_izq = tk.Frame(frame_principal, bg="#F9F6F0")
frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

txt_resultados = scrolledtext.ScrolledText(
    frame_izq, 
    width=46, 
    height=16, 
    font=("Consolas", 9), 
    bg="#FFF0F5", 
    fg="#2C3E50",
    state=tk.DISABLED
)
txt_resultados.pack(fill=tk.BOTH, expand=True)

# Columna Derecha: Lienzo del grafo
frame_der = tk.Frame(frame_principal, bg="#F9F6F0")
frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

canvas = tk.Canvas(frame_der, width=440, height=300, bg="#FFFFFF", highlightthickness=2, highlightbackground="#BDC3C7")
canvas.pack(fill=tk.BOTH, expand=True)

# Pie de página
lbl_footer = tk.Label(
    root, 
    text="Sistema Inteligente de Búsqueda | UTVT", 
    font=("Arial", 9, "bold"), 
    bg=COLOR_VERDE_VIVO, 
    fg="#FFFFFF",
    pady=6
)
lbl_footer.pack(fill=tk.X, side=tk.BOTTOM)

# Dibujar grafo inicial al abrir
dibujar_grafo()

root.mainloop()