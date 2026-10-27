import tkinter as tk
from tkinter import ttk
import time

# ============================================================
# PROBLEMA DE BÚSQUEDA
# ============================================================

estados = ["A", "B", "C", "D", "E", "F"]

acciones = {
    "A": ["D", "B"],
    "B": ["C", "A"],
    "C": ["F", "B"],
    "D": ["E", "A"],
    "E": ["F", "D"],
    "F": ["E", "C"]
}

posiciones_grafo = {
    "A": (60, 50),   "B": (180, 50),  "C": (300, 50),
    "D": (60, 140),  "E": (180, 140), "F": (300, 140)
}

# ============================================================
# ESTILOS Y COLORES (Lila y Rosa)
# ============================================================

C_FONDO = "#F8F0F6"        # Fondo lila/rosa claro
C_TARJETA = "#FFFFFF"      # Blanco para contenedores
C_LILA_NODO = "#E5D0F5"    # Color base del cuadrado
C_LILA_TEXTO = "#4A2E56"   # Texto oscuro
C_ROSA_EXPLORA = "#FFB3D9" # Cuadrado en exploración
C_ROSA_RUTA = "#D84382"    # Borde y línea de la ruta final

# ============================================================
# DIBUJO DEL GRAFO Y DEL ÁRBOL
# ============================================================

def dibujar_grafo(nodo_actual=None, ruta_final=None):
    canvas_grafo.delete("all")
    
    # Conexiones del grafo
    dibujadas = set()
    for origen, vecinos in acciones.items():
        x1, y1 = posiciones_grafo[origen]
        for destino in vecinos:
            par = tuple(sorted([origen, destino]))
            if par not in dibujadas:
                x2, y2 = posiciones_grafo[destino]
                color = "#D8C5E2"
                ancho = 2
                
                if ruta_final:
                    for i in range(len(ruta_final) - 1):
                        if (ruta_final[i] == origen and ruta_final[i+1] == destino) or \
                           (ruta_final[i] == destino and ruta_final[i+1] == origen):
                            color = C_ROSA_RUTA
                            ancho = 4
                            
                canvas_grafo.create_line(x1, y1, x2, y2, fill=color, width=ancho)
                dibujadas.add(par)

    # Nodos del grafo
    tam = 18
    for nodo, (x, y) in posiciones_grafo.items():
        color_fill = C_LILA_NODO
        color_borde = C_LILA_TEXTO
        
        if nodo == nodo_actual or (ruta_final and nodo in ruta_final):
            color_fill = C_ROSA_EXPLORA
            color_borde = C_ROSA_RUTA

        canvas_grafo.create_rectangle(x - tam, y - tam, x + tam, y + tam, fill=color_fill, outline=color_borde, width=2)
        canvas_grafo.create_text(x, y, text=nodo, font=("Segoe UI", 10, "bold"), fill=C_LILA_TEXTO)

def calcular_posiciones_arbol(arbol_nodos):
    if not arbol_nodos:
        return {}
    
    niveles = {}
    for id_nodo, datos in arbol_nodos.items():
        niv = datos["nivel"]
        niveles.setdefault(niv, []).append(id_nodo)
        
    pos = {}
    ancho_canvas = 360
    alto_nivel = 45
    
    for niv, lista_ids in niveles.items():
        n = len(lista_ids)
        y = 30 + niv * alto_nivel
        for i, id_nodo in enumerate(lista_ids):
            x = (ancho_canvas / (n + 1)) * (i + 1)
            pos[id_nodo] = (x, y)
            
    return pos

def dibujar_arbol(arbol_nodos, nodo_actual_id=None, ruta_final_ids=None):
    canvas_arbol.delete("all")
    if not arbol_nodos:
        return

    pos = calcular_posiciones_arbol(arbol_nodos)

    # Líneas entre padre e hijo
    for id_nodo, datos in arbol_nodos.items():
        padre_id = datos["padre"]
        if padre_id and padre_id in pos and id_nodo in pos:
            x1, y1 = pos[padre_id]
            x2, y2 = pos[id_nodo]
            color = "#D8C5E2"
            ancho = 2
            
            if ruta_final_ids and id_nodo in ruta_final_ids and padre_id in ruta_final_ids:
                color = C_ROSA_RUTA
                ancho = 3
                
            canvas_arbol.create_line(x1, y1, x2, y2, fill=color, width=ancho)

    # Nodos del árbol
    tam = 14
    for id_nodo, datos in arbol_nodos.items():
        if id_nodo not in pos:
            continue
        x, y = pos[id_nodo]
        nombre_estado = datos["estado"]
        
        color_fill = C_LILA_NODO
        color_borde = C_LILA_TEXTO
        
        if id_nodo == nodo_actual_id or (ruta_final_ids and id_nodo in ruta_final_ids):
            color_fill = C_ROSA_EXPLORA
            color_borde = C_ROSA_RUTA

        canvas_arbol.create_rectangle(x - tam, y - tam, x + tam, y + tam, fill=color_fill, outline=color_borde, width=2)
        canvas_arbol.create_text(x, y, text=nombre_estado, font=("Segoe UI", 9, "bold"), fill=C_LILA_TEXTO)

# ============================================================
# ALGORITMO BFS CON HISTORIAL DE PASOS
# ============================================================

def agregar_paso_historial(paso, estado, detalle):
    tabla_historial.insert("", tk.END, values=(f"Paso {paso}", estado, detalle))
    # Autoscroll al último elemento agregado
    items = tabla_historial.get_children()
    if items:
        tabla_historial.see(items[-1])

def busqueda_anchura_gui(inicio, objetivo):
    arbol = {
        1: {"estado": inicio, "padre": None, "nivel": 0}
    }
    
    cola = [[1]]
    visitados = set()
    contador_ids = 1
    num_paso = 1

    agregar_paso_historial(0, inicio, "Estado inicial configurado")

    while cola:
        camino_ids = cola.pop(0)
        nodo_id = camino_ids[-1]
        estado_actual = arbol[nodo_id]["estado"]

        if estado_actual in visitados:
            continue

        visitados.add(estado_actual)

        # Registro en la bitácora derecha y en el cuadro de texto
        agregar_paso_historial(num_paso, estado_actual, "Explorando nodo")
        txt_resumen.insert(tk.END, f"• Paso {num_paso}: Explorando '{estado_actual}'\n")
        txt_resumen.see(tk.END)
        num_paso += 1
        
        # Animación visual
        dibujar_grafo(nodo_actual=estado_actual)
        dibujar_arbol(arbol, nodo_actual_id=nodo_id)
        ventana.update()
        time.sleep(0.4)

        if estado_actual == objetivo:
            agregar_paso_historial("¡ÉXITO!", estado_actual, "Objetivo alcanzado")
            return camino_ids, arbol

        # Generar hijos
        nivel_actual = arbol[nodo_id]["nivel"]
        for vecino in acciones[estado_actual]:
            if vecino not in visitados:
                contador_ids += 1
                arbol[contador_ids] = {
                    "estado": vecino,
                    "padre": nodo_id,
                    "nivel": nivel_actual + 1
                }
                cola.append(camino_ids + [contador_ids])

    return None, arbol

def ejecutar():
    inicio = combo_inicio.get()
    objetivo = combo_objetivo.get()

    # Limpieza de vistas
    txt_resumen.delete("1.0", tk.END)
    for row in tabla_historial.get_children():
        tabla_historial.delete(row)

    if inicio == objetivo:
        txt_resumen.insert(tk.END, "⚠️ El estado inicial y el objetivo son iguales.\n")
        return

    btn_iniciar.config(state="disabled")
    
    camino_ids, arbol = busqueda_anchura_gui(inicio, objetivo)

    if camino_ids:
        ruta_estados = [arbol[i]["estado"] for i in camino_ids]
        txt_resumen.insert(tk.END, "\n✨ ¡Objetivo Encontrado!\n")
        txt_resumen.insert(tk.END, f"Ruta: {' ➔ '.join(ruta_estados)}\n")
        txt_resumen.insert(tk.END, f"Total de movimientos: {len(ruta_estados) - 1}\n")
        
        dibujar_grafo(ruta_final=ruta_estados)
        dibujar_arbol(arbol, ruta_final_ids=camino_ids)
    else:
        txt_resumen.insert(tk.END, "\n❌ No se encontró una ruta hacia el objetivo.\n")
        
    btn_iniciar.config(state="normal")

# ============================================================
# INTERFAZ GRÁFICA (LAYOUT DE DOS COLUMNAS)
# ============================================================

ventana = tk.Tk()
ventana.title("Búsqueda BFS - Visualizador Interactivo")
ventana.geometry("780x500")
ventana.configure(bg=C_FONDO)
ventana.resizable(False, False)

# Configurar estilos de TTK para la tabla e interfaz
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", 
                background="#FFFFFF",
                fieldbackground="#FFFFFF",
                foreground=C_LILA_TEXTO,
                rowheight=24,
                font=("Segoe UI", 9))
style.configure("Treeview.Heading", 
                background=C_LILA_NODO, 
                foreground=C_LILA_TEXTO, 
                font=("Segoe UI", 9, "bold"))
style.map("Treeview", background=[("selected", C_ROSA_EXPLORA)])

# Título Principal
lbl_titulo = tk.Label(ventana, text="Algoritmo de Búsqueda en Anchura (BFS)", font=("Segoe UI", 13, "bold"), bg=C_FONDO, fg=C_LILA_TEXTO)
lbl_titulo.pack(pady=(10, 5))

# Contenedor Principal (Dos Columnas)
frame_principal = tk.Frame(ventana, bg=C_FONDO)
frame_principal.pack(fill="both", expand=True, padx=12, pady=5)

# ------------------------------------------------------------
# COLUMNA IZQUIERDA: Grafo y Árbol
# ------------------------------------------------------------
col_izquierda = tk.Frame(frame_principal, bg=C_FONDO)
col_izquierda.grid(row=0, column=0, padx=(0, 10), sticky="nsew")

lbl_grafo = tk.Label(col_izquierda, text="Mapa de Estados (Grafo):", font=("Segoe UI", 9, "bold"), bg=C_FONDO, fg=C_LILA_TEXTO)
lbl_grafo.pack(anchor="w", pady=(0, 2))

canvas_grafo = tk.Canvas(col_izquierda, width=360, height=180, bg=C_TARJETA, highlightthickness=1, highlightbackground=C_LILA_NODO)
canvas_grafo.pack(pady=(0, 8))

lbl_arbol = tk.Label(col_izquierda, text="Estructura del Árbol de Búsqueda:", font=("Segoe UI", 9, "bold"), bg=C_FONDO, fg=C_LILA_TEXTO)
lbl_arbol.pack(anchor="w", pady=(0, 2))

canvas_arbol = tk.Canvas(col_izquierda, width=360, height=180, bg=C_TARJETA, highlightthickness=1, highlightbackground=C_LILA_NODO)
canvas_arbol.pack()

# ------------------------------------------------------------
# COLUMNA DERECHA: Controles e Historial de Pasos
# ------------------------------------------------------------
col_derecha = tk.Frame(frame_principal, bg=C_FONDO)
col_derecha.grid(row=0, column=1, sticky="nsew")

# Panel de Selección (Controles)
frame_controles = tk.LabelFrame(col_derecha, text=" Configuración ", font=("Segoe UI", 9, "bold"), bg=C_FONDO, fg=C_LILA_TEXTO, bd=1, relief="solid")
frame_controles.pack(fill="x", pady=(0, 8), ipady=4)

lbl_inicio = tk.Label(frame_controles, text="Inicio:", font=("Segoe UI", 9, "bold"), bg=C_FONDO, fg=C_LILA_TEXTO)
lbl_inicio.grid(row=0, column=0, padx=(10, 4), pady=4)

combo_inicio = ttk.Combobox(frame_controles, values=estados, width=4, state="readonly")
combo_inicio.set("A")
combo_inicio.grid(row=0, column=1, padx=(0, 12), pady=4)

lbl_objetivo = tk.Label(frame_controles, text="Objetivo:", font=("Segoe UI", 9, "bold"), bg=C_FONDO, fg=C_LILA_TEXTO)
lbl_objetivo.grid(row=0, column=2, padx=(0, 4), pady=4)

combo_objetivo = ttk.Combobox(frame_controles, values=estados, width=4, state="readonly")
combo_objetivo.set("F")
combo_objetivo.grid(row=0, column=3, padx=(0, 12), pady=4)

btn_iniciar = tk.Button(
    frame_controles, text="Iniciar Recorrido", command=ejecutar,
    font=("Segoe UI", 9, "bold"), bg=C_ROSA_EXPLORA, fg=C_LILA_TEXTO,
    activebackground=C_LILA_NODO, bd=0, padx=10, pady=3, cursor="hand2"
)
btn_iniciar.grid(row=0, column=4, padx=(0, 10), pady=4)

# Tabla de Historial / Bitácora de Pasos
lbl_historial = tk.Label(col_derecha, text="Historial / Bitácora de Pasos:", font=("Segoe UI", 9, "bold"), bg=C_FONDO, fg=C_LILA_TEXTO)
lbl_historial.pack(anchor="w", pady=(0, 2))

frame_tabla = tk.Frame(col_derecha, bg=C_TARJETA, bd=1, relief="solid")
frame_tabla.pack(fill="x", pady=(0, 8))

tabla_historial = ttk.Treeview(
    frame_tabla, 
    columns=("Paso", "Estado", "Detalle"), 
    show="headings", 
    height=8
)

tabla_historial.heading("Paso", text="Paso")
tabla_historial.heading("Estado", text="Nodo")
tabla_historial.heading("Detalle", text="Acción / Estado")

tabla_historial.column("Paso", width=70, anchor="center")
tabla_historial.column("Estado", width=60, anchor="center")
tabla_historial.column("Detalle", width=210, anchor="w")

scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla_historial.yview)
tabla_historial.configure(yscrollcommand=scrollbar_tabla.set)

tabla_historial.pack(side="left", fill="both", expand=True)
scrollbar_tabla.pack(side="right", fill="y")

# Cuadro de Resumen Final
txt_resumen = tk.Text(col_derecha, width=44, height=5, font=("Consolas", 8), bg=C_TARJETA, fg=C_LILA_TEXTO, bd=1, relief="solid")
txt_resumen.pack(fill="x")

# Inicialización
dibujar_grafo()

ventana.mainloop()