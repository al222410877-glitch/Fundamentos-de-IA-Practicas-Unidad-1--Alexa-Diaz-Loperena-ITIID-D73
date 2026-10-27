# ============================================================
# COMPARACIÓN COMPLETA DE GRAFOS: HEURÍSTICA VS COSTO (A -> J)
# ============================================================

import tkinter as tk
from tkinter import scrolledtext
import heapq

# --- DATOS DEL SCRIPT 1 (HEURÍSTICA) ---
acciones_h = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": ["H"],
    "E": [],
    "F": ["I"],
    "G": [],
    "H": [],
    "I": ["J"],
    "J": []
}

heuristicas = {
    "A": 7, "B": 6, "C": 4, "D": 7, "E": 5, 
    "F": 3, "G": 6, "H": 8, "I": 1, "J": 0
}

# --- DATOS DEL SCRIPT 2 (COSTOS POR ARISTA) ---
acciones_c = {
    "A": [("B", 2), ("C", 5)],
    "B": [("D", 4), ("E", 1)],
    "C": [("F", 2), ("G", 8)],
    "D": [("H", 3)],
    "E": [("I", 2)],
    "F": [("J", 3)],
    "G": [],
    "H": [],
    "I": [],
    "J": []
}

coordenadas_nodos = {
    "A": (130, 25),
    "B": (80, 75),
    "C": (180, 75),
    "D": (50, 125),
    "E": (110, 125),
    "F": (150, 125),
    "G": (210, 125),
    "H": (30, 175),
    "I": (110, 175),
    "J": (150, 225)
}

def ejecutar_heuristica(inicio, objetivo):
    pasos = []
    suma_total_h = sum(heuristicas.values())
    pasos.append(f"Suma total de h(n) del árbol: {suma_total_h}")
    
    g_inicial = 0
    h_inicial = heuristicas.get(inicio, 0)
    f_inicial = g_inicial + h_inicial

    frontera = [(f_inicial, g_inicial, inicio, [inicio])]
    visitados = set()

    while frontera:
        frontera.sort(key=lambda x: (x[0], x[1]))
        f_actual, g_actual, actual, camino = frontera.pop(0)
        h_actual = heuristicas.get(actual, 0)
        pasos.append(f"Nodo '{actual}' | g={g_actual}, h={h_actual}, f={f_actual}")

        if actual == objetivo:
            suma_ruta = sum(heuristicas[n] for n in camino)
            pasos.append(f"★ Ruta: {' → '.join(camino)} | Suma h(n) ruta: {suma_ruta}")
            return camino, pasos

        visitados.add(actual)
        for vecino in acciones_h.get(actual, []):
            if vecino not in visitados:
                g_vecino = g_actual + 1
                h_vecino = heuristicas.get(vecino, 0)
                f_vecino = g_vecino + h_vecino
                frontera.append((f_vecino, g_vecino, vecino, camino + [vecino]))
    return None, pasos

def ejecutar_costos(inicio, objetivo):
    pasos = []
    heap = [(0, inicio, [inicio])]
    costos_visitados = {inicio: 0}

    while heap:
        costo_actual, actual, camino = heapq.heappop(heap)
        pasos.append(f"Nodo '{actual}' | Costo acumulado g={costo_actual}")

        if actual == objetivo:
            pasos.append(f"★ Ruta: {' → '.join(camino)} | Costo total: {costo_actual}")
            return camino, pasos

        for hijo, costo_arista in acciones_c.get(actual, []):
            nuevo_costo = costo_actual + costo_arista
            if hijo not in costos_visitados or nuevo_costo < costos_visitados[hijo]:
                costos_visitados[hijo] = nuevo_costo
                heapq.heappush(heap, (nuevo_costo, hijo, camino + [hijo]))
    return None, pasos

def dibujar_grafo(canvas_obj, es_costos, ruta_activa):
    canvas_obj.delete("all")
    
    # Seleccionar estructura de conexiones
    conexiones = acciones_c if es_costos else {k: [(v, 1) for v in vs] for k, vs in acciones_h.items()}

    for nodo, hijos in conexiones.items():
        x1, y1 = coordenadas_nodos[nodo]
        for hijo, val in hijos:
            if hijo in coordenadas_nodos:
                x2, y2 = coordenadas_nodos[hijo]
                
                es_parte = False
                if ruta_activa and len(ruta_activa) > 1:
                    for i in range(len(ruta_activa) - 1):
                        if ruta_activa[i] == nodo and ruta_activa[i+1] == hijo:
                            es_parte = True
                            break
                
                color_linea = "#FF1493" if es_parte else "#E0E0E0"
                grosor = 4 if es_parte else 2
                canvas_obj.create_line(x1, y1, x2, y2, fill=color_linea, width=grosor)
                
                if es_costos:
                    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                    canvas_obj.create_text(mx, my, text=str(val), font=("Arial", 7, "bold"), fill="#DAA520")

    for nodo, (x, y) in coordenadas_nodos.items():
        if nodo == "A":
            color_relleno = "#FFD700"  # Amarillo
        elif nodo == "J":
            color_relleno = "#FF69B4"  # Rosa
        else:
            color_relleno = "#FFFACD"  # Amarillo claro
            
        radio = 15
        canvas_obj.create_oval(x - radio, y - radio, x + radio, y + radio, fill=color_relleno, outline="#FF1493", width=2)
        
        texto_inferior = f"h={heuristicas[nodo]}" if not es_costos else nodo
        canvas_obj.create_text(x, y-2, text=nodo if not es_costos else nodo, font=("Arial", 9, "bold"), fill="#333333")
        if not es_costos:
            canvas_obj.create_text(x, y+9, text=f"h={heuristicas[nodo]}", font=("Arial", 6), fill="#B8860B")

def comparar_todo():
    ruta_h, pasos_h = ejecutar_heuristica("A", "J")
    ruta_c, pasos_c = ejecutar_costos("A", "J")
    
    txt_resultados.config(state=tk.NORMAL)
    txt_resultados.delete("1.0", tk.END)
    
    txt_resultados.insert(tk.END, "=== 1. MÉTODO HEURÍSTICO (Script 1) ===\n")
    txt_resultados.insert(tk.END, "\n".join(pasos_h) + "\n\n")
    txt_resultados.insert(tk.END, "----------------------------------------\n")
    txt_resultados.insert(tk.END, "=== 2. MÉTODO COSTO ACUMULADO (Script 2) ===\n")
    txt_resultados.insert(tk.END, "\n".join(pasos_c) + "\n")
    
    txt_resultados.config(state=tk.DISABLED)
    
    dibujar_grafo(canvas_h, False, ruta_h)
    dibujar_grafo(canvas_c, True, ruta_c)

# ============================================================
# CONFIGURACIÓN DE LA INTERFAZ (Rosa y Amarillo)
# ============================================================

root = tk.Tk()
root.title("Comparativa de Grafos - Heurística vs Costo")
root.geometry("1020x620")
root.config(bg="#FFF8DC")

COLOR_ROSA = "#FF69B4"
COLOR_AMARILLO_VIVO = "#FFD700"

lbl_titulo = tk.Label(
    root, 
    text="Comparación Gráfica: Heurística[cite: 3] vs Costos Acumulados[cite: 4]", 
    font=("Arial", 14, "bold"), 
    bg="#FFF8DC", 
    fg="#4A4A4A"
)
lbl_titulo.pack(pady=8)

btn_ejecutar = tk.Button(
    root, 
    text="Ejecutar Comparación de Grafos", 
    command=comparar_todo, 
    font=("Arial", 11, "bold"), 
    bg=COLOR_ROSA, 
    fg="#FFFFFF",
    padx=15, 
    pady=4
)
btn_ejecutar.pack(pady=5)

frame_principal = tk.Frame(root, bg="#FFF8DC")
frame_principal.pack(pady=5, padx=10, fill=tk.BOTH, expand=True)

# Izquierda: Texto detallado
frame_izq = tk.Frame(frame_principal, bg="#FFF8DC")
frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

txt_resultados = scrolledtext.ScrolledText(
    frame_izq, 
    width=45, 
    height=20, 
    font=("Consolas", 8), 
    bg="#FFFFE0", 
    fg="#333333",
    state=tk.DISABLED
)
txt_resultados.pack(fill=tk.BOTH, expand=True)

# Derecha: Dos Grafos Lado a Lado
frame_der = tk.Frame(frame_principal, bg="#FFF8DC")
frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)

# Grafo 1: Heurística
frame_g1 = tk.LabelFrame(frame_der, text="Grafo 1: Heurística (f = g + h)", font=("Arial", 9, "bold"), bg="#FFF8DC", fg=COLOR_ROSA)
frame_g1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
canvas_h = tk.Canvas(frame_g1, width=230, height=270, bg="#FFFFFF", highlightthickness=1, highlightbackground=COLOR_AMARILLO_VIVO)
canvas_h.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

# Grafo 2: Costos
frame_g2 = tk.LabelFrame(frame_der, text="Grafo 2: Costo Acumulado (heapq)", font=("Arial", 9, "bold"), bg="#FFF8DC", fg="#D4AC0D")
frame_g2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
canvas_c = tk.Canvas(frame_g2, width=230, height=270, bg="#FFFFFF", highlightthickness=1, highlightbackground=COLOR_AMARILLO_VIVO)
canvas_c.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

lbl_footer = tk.Label(
    root, 
    text="Sistema Inteligente de Búsqueda | Interfaz Rosa y Amarillo", 
    font=("Arial", 9, "bold"), 
    bg=COLOR_AMARILLO_VIVO, 
    fg="#333333",
    pady=5
)
lbl_footer.pack(fill=tk.X, side=tk.BOTTOM)

# Dibujar esquema inicial
dibujar_grafo(canvas_h, False, None)
dibujar_grafo(canvas_c, True, None)

root.mainloop()