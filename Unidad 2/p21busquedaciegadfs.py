# ============================================================
# BÚSQUEDA CIEGA DFS (Profundidad) - Interfaz Gráfica Interactiva
# Cumplimiento estricto de rúbrica: Exploración, Ciclos, Rutas y Límite
# ============================================================

import tkinter as tk
from tkinter import messagebox, scrolledtext
import time

# Grafo con ciclos para demostrar el control de bucles
acciones_dfs = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B", "E"],
    "E": ["B", "D", "F"],
    "F": ["C", "E"]
}

estado_inicial = "A"
estado_objetivo = "F"

# Coordenadas visuales para el grafo DFS
coordenadas_nodos = {
    "A": (80, 140),
    "B": (200, 60),
    "C": (200, 220),
    "D": (320, 60),
    "E": (320, 220),
    "F": (440, 140)
}

def dfs_todas_las_rutas(actual, objetivo, camino_actual, visitados_globales, orden_exploracion, todas_las_rutas, limite, pasos_simples):
    pasos_simples.append(f"• Explorando nodo: {actual} (Ruta actual: {' → '.join(camino_actual)})")

    # Registrar en el orden general de exploración (Nodos explorados)
    if actual not in orden_exploracion:
        orden_exploracion.append(actual)

    # 2.4 Control de límite de profundidad
    if len(camino_actual) > limite:
        pasos_simples.append(f"  (Límite de profundidad {limite} alcanzado. Retrocediendo...).")
        return

    # 2.3 Si llegamos al objetivo, guardamos la ruta
    if actual == objetivo:
        todas_las_rutas.append(list(camino_actual))
        pasos_simples.append(f"  ★ ¡Meta encontrada! Ruta válida: {' → '.join(camino_actual)}")
        return

    # 2.2 Control de ciclos usando la estructura visitados / control de ruta
    for vecino in acciones_dfs.get(actual, []):
        if vecino not in camino_actual:  # Evita ciclos en la rama actual
            camino_actual.append(vecino)
            visitados_globales.add(vecino)
            
            dfs_todas_las_rutas(vecino, objetivo, camino_actual, visitados_globales, orden_exploracion, todas_las_rutas, limite, pasos_simples)
            
            camino_actual.pop()  # Backtracking
        else:
            pasos_simples.append(f"  [Ciclo evitado] El nodo '{vecino}' ya fue visitado en este camino.")

def dibujar_grafo(nodo_activo=None, ruta_estatica=None):
    canvas.delete("all")
    
    # 1. Dibujar líneas del grafo
    for nodo, vecinos in acciones_dfs.items():
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
                
                color_linea = "#FF69B4" if es_parte_ruta else "#BDC3C7"
                grosor = 4 if es_parte_ruta else 2
                canvas.create_line(x1, y1, x2, y2, fill=color_linea, width=grosor)

    # 2. Dibujar nodos con colores vivos
    for nodo, (x, y) in coordenadas_nodos.items():
        if nodo == estado_inicial:
            color_relleno = "#2ECC71"  # Verde vivo
        elif nodo == estado_objetivo:
            color_relleno = "#FF69B4"  # Rosa fuerte
        else:
            color_relleno = "#9B59B6"  # Lila intenso
            
        outline_color = "#E74C3C" if nodo == nodo_activo else "#2C3E50"
        grosor_borde = 4 if nodo == nodo_activo else 2
            
        radio = 24
        canvas.create_oval(x - radio, y - radio, x + radio, y + radio, fill=color_relleno, outline=outline_color, width=grosor_borde)
        canvas.create_text(x, y, text=nodo, font=("Arial", 13, "bold"), fill="#FFFFFF")

def ejecutar_busqueda_dfs():
    try:
        limite = int(entry_limite.get())
    except ValueError:
        messagebox.showerror("Error", "Ingresa un número válido para el límite.")
        return

    orden_exploracion = []
    todas_las_rutas = []
    visitados_globales = set()
    pasos_simples = []
    camino_inicial = [estado_inicial]
    visitados_globales.add(estado_inicial)

    dfs_todas_las_rutas(
        estado_inicial, 
        estado_objetivo, 
        camino_inicial, 
        visitados_globales,
        orden_exploracion, 
        todas_las_rutas, 
        limite,
        pasos_simples
    )

    # Mostrar resultados claros diferenciando nodos explorados y rutas encontradas
    txt_resultados.config(state=tk.NORMAL)
    txt_resultados.delete("1.0", tk.END)
    
    txt_resultados.insert(tk.END, "=== REPORTE DE BÚSQUEDA DFS ===\n\n")
    txt_resultados.insert(tk.END, f"• Orden de Exploración (Nodos revisados):\n  {' → '.join(orden_exploracion)}\n\n")
    txt_resultados.insert(tk.END, f"• Control de Ciclos: Activo (Uso de set() y validación)\n\n")
    txt_resultados.insert(tk.END, f"• Rutas Encontradas ({len(todas_las_rutas)} en total):\n")
    
    if todas_las_rutas:
        for i, ruta in enumerate(todas_las_rutas, 1):
            txt_resultados.insert(tk.END, f"  Ruta {i}: {' → '.join(ruta)}\n")
    else:
        txt_resultados.insert(tk.END, "  No hay rutas dentro de este límite.\n")
        
    txt_resultados.insert(tk.END, "\n" + "─"*38 + "\nDETALLE PASO A PASO:\n\n")
    for paso in pasos_simples:
        txt_resultados.insert(tk.END, paso + "\n")
        
    txt_resultados.config(state=tk.DISABLED)

    # Animación y marcado final de la última ruta
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
root.title("Búsqueda Ciega DFS - Interfaz Interactiva")
root.geometry("900x560")
root.config(bg="#F9F6F0")

COLOR_LILA_VIVO = "#9B59B6"
COLOR_VERDE_VIVO = "#2ECC71"
COLOR_TEXTO = "#2C3E50"

# Título superior
lbl_titulo = tk.Label(
    root, 
    text="Búsqueda en Profundidad (DFS) - Control de Ciclos y Rutas", 
    font=("Arial", 15, "bold"), 
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
    text="Iniciar Búsqueda DFS", 
    command=ejecutar_busqueda_dfs, 
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

# Columna Izquierda: Texto resumido con orden de exploración y rutas
frame_izq = tk.Frame(frame_principal, bg="#F9F6F0")
frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

txt_resultados = scrolledtext.ScrolledText(
    frame_izq, 
    width=48, 
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

canvas = tk.Canvas(frame_der, width=450, height=310, bg="#FFFFFF", highlightthickness=2, highlightbackground="#BDC3C7")
canvas.pack(fill=tk.BOTH, expand=True)

# Pie de página
lbl_footer = tk.Label(
    root, 
    text="Búsqueda Ciega DFS | UTVT", 
    font=("Arial", 9, "bold"), 
    bg=COLOR_VERDE_VIVO, 
    fg="#FFFFFF",
    pady=6
)
lbl_footer.pack(fill=tk.X, side=tk.BOTTOM)

# Dibujar grafo inicial al abrir
dibujar_grafo()

root.mainloop()