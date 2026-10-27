# ================================================================
# COMPARATIVO DE ALGORITMOS DE BÚSQUEDA
# BFS, DFS, UCS, GREEDY BEST-FIRST SEARCH y A*
# Interfaz gráfica con Tkinter (Estética Lila y Verde)
# ================================================================
# Objetivo didáctico:
#   Comparar cinco algoritmos sobre el mismo grafo, con el mismo
#   origen y destino, mostrando rutas, costos y nodos expandidos.
# ================================================================

import tkinter as tk
from tkinter import ttk, messagebox
import heapq
from collections import deque
import math


# ------------------------------------------------
# 1. DEFINICIÓN DEL GRAFO (Escenario Casa -> Universidad)
# ------------------------------------------------
GRAFO = {
    "A": {"B": 2, "C": 5},   # Casa conecta con dos avenidas
    "B": {"D": 4, "E": 7},   # Avenida B conecta con dos calles
    "C": {"F": 2, "G": 6},   # Avenida C conecta con otras dos
    "D": {"H": 3},        # Calle D lleva a H
    "E": {"H": 2},        # Calle E lleva a H
    "F": {"I": 3},        # Calle F lleva a I
    "G": {"I": 2},        # Calle G lleva a I
    "H": {"J": 5},        # Calle H lleva a J
    "I": {"J": 2},        # Calle I conecta directo a la universidad
    "J": {}            # Universidad (objetivo)
}

# ------------------------------------------------
# 2. HEURÍSTICA Y POSICIONES
# ------------------------------------------------
HEURISTICA_HASTA_J = {
    "A": 25,
    "B": 20,
    "C": 15,
    "D": 18,
    "E": 30,
    "F": 10,
    "G": 25,
    "H": 40,
    "I": 5,
    "J": 0
}

POSICIONES = {
    "A": (320, 50),
    "B": (200, 130),
    "C": (440, 130),
    "D": (120, 210),
    "E": (250, 210),
    "F": (390, 210),
    "G": (520, 210),
    "H": (180, 290),
    "I": (460, 290),
    "J": (320, 370)
}

# Paleta de colores Lila y Verde
COLOR_NORMAL = "#E8F5E9"
COLOR_INICIO = "#2E7D32"
COLOR_OBJETIVO = "#6A1B9A"
COLOR_EXPANDIDO = "#C8E6C9"
COLOR_RUTA = "#AB47BC"


# ------------------------------------------------
# 3. FUNCIONES AUXILIARES
# ------------------------------------------------
def reconstruir_camino(padres, inicio, objetivo):
    """Reconstruye el camino desde el origen al objetivo."""
    if objetivo != inicio and objetivo not in padres:
        return []

    camino = []
    actual = objetivo

    while actual is not None:
        camino.append(actual)
        if actual == inicio:
            break
        actual = padres.get(actual)

    camino.reverse()
    if not camino or camino[0] != inicio:
        return []

    return camino


def calcular_costo(camino):
    """Suma los pesos de las aristas que componen un camino."""
    if not camino:
        return math.inf

    costo = 0
    for i in range(len(camino) - 1):
        origen = camino[i]
        destino = camino[i + 1]
        costo += GRAFO[origen][destino]

    return costo


def vecinos_ordenados(nodo):
    """Devuelve vecinos en orden alfabético para resultados reproducibles."""
    return sorted(GRAFO[nodo].items())


# ------------------------------------------------
# 4. IMPLEMENTACIÓN DE ALGORITMOS
# ------------------------------------------------
def bfs(inicio, objetivo):
    frontera = deque([inicio])
    descubiertos = {inicio}
    padres = {inicio: None}
    expandidos = []
    registro = []

    while frontera:
        actual = frontera.popleft()
        expandidos.append(actual)
        registro.append(f"BFS: se extrae {actual} de la cola.")

        if actual == objetivo:
            break

        for vecino, peso in vecinos_ordenados(actual):
            if vecino not in descubiertos:
                descubiertos.add(vecino)
                padres[vecino] = actual
                frontera.append(vecino)
                registro.append(f"  Se descubre {vecino} desde {actual} (peso={peso}).")

    camino = reconstruir_camino(padres, inicio, objetivo)
    return crear_resultado("BFS", camino, expandidos, registro)


def dfs(inicio, objetivo):
    pila = [inicio]
    descubiertos = {inicio}
    padres = {inicio: None}
    expandidos = []
    registro = []

    while pila:
        actual = pila.pop()
        expandidos.append(actual)
        registro.append(f"DFS: se extrae {actual} de la pila.")

        if actual == objetivo:
            break

        for vecino, peso in reversed(vecinos_ordenados(actual)):
            if vecino not in descubiertos:
                descubiertos.add(vecino)
                padres[vecino] = actual
                pila.append(vecino)
                registro.append(f"  Se agrega {vecino} a la pila desde {actual} (peso={peso}).")

    camino = reconstruir_camino(padres, inicio, objetivo)
    return crear_resultado("DFS", camino, expandidos, registro)


def ucs(inicio, objetivo):
    frontera = [(0, inicio)]
    mejor_costo = {inicio: 0}
    padres = {inicio: None}
    expandidos = []
    registro = []
    cerrados = set()

    while frontera:
        costo_actual, actual = heapq.heappop(frontera)
        if costo_actual != mejor_costo.get(actual, math.inf) or actual in cerrados:
            continue
        cerrados.add(actual)
        expandidos.append(actual)
        registro.append(f"UCS: se expande {actual} con g(n)={costo_actual}.")

        if actual == objetivo:
            break

        for vecino, peso in vecinos_ordenados(actual):
            nuevo_costo = costo_actual + peso
            if nuevo_costo < mejor_costo.get(vecino, math.inf):
                mejor_costo[vecino] = nuevo_costo
                padres[vecino] = actual
                heapq.heappush(frontera, (nuevo_costo, vecino))
                registro.append(f"  Mejor costo para {vecino}: g(n)={nuevo_costo}.")

    camino = reconstruir_camino(padres, inicio, objetivo)
    return crear_resultado("UCS", camino, expandidos, registro)


def greedy(inicio, objetivo, heuristica):
    frontera = [(heuristica[inicio], inicio)]
    descubiertos = {inicio}
    padres = {inicio: None}
    expandidos = []
    registro = []

    while frontera:
        h_actual, actual = heapq.heappop(frontera)
        expandidos.append(actual)
        registro.append(f"Greedy: se expande {actual} con h(n)={h_actual}.")

        if actual == objetivo:
            break

        for vecino, peso in vecinos_ordenados(actual):
            if vecino not in descubiertos:
                descubiertos.add(vecino)
                padres[vecino] = actual
                heapq.heappush(frontera, (heuristica[vecino], vecino))
                registro.append(f"  Se agrega {vecino}: h(n)={heuristica[vecino]}.")

    camino = reconstruir_camino(padres, inicio, objetivo)
    return crear_resultado("Greedy", camino, expandidos, registro)


def astar(inicio, objetivo, heuristica):
    frontera = [(heuristica[inicio], 0, inicio)]
    mejor_g = {inicio: 0}
    padres = {inicio: None}
    expandidos = []
    registro = []

    while frontera:
        f_actual, g_actual, actual = heapq.heappop(frontera)
        if g_actual != mejor_g.get(actual, math.inf):
            continue
        expandidos.append(actual)
        registro.append(f"A*: se expande {actual}: g(n)={g_actual}, h(n)={heuristica[actual]}, f(n)={f_actual}.")

        if actual == objetivo:
            break

        for vecino, peso in vecinos_ordenados(actual):
            nuevo_g = g_actual + peso
            if nuevo_g < mejor_g.get(vecino, math.inf):
                mejor_g[vecino] = nuevo_g
                padres[vecino] = actual
                nuevo_f = nuevo_g + heuristica[vecino]
                heapq.heappush(frontera, (nuevo_f, nuevo_g, vecino))
                registro.append(f"  Se actualiza {vecino}: g={nuevo_g}, h={heuristica[vecino]}, f={nuevo_f}.")

    camino = reconstruir_camino(padres, inicio, objetivo)
    return crear_resultado("A*", camino, expandidos, registro)


def crear_resultado(nombre, camino, expandidos, registro):
    return {
        "algoritmo": nombre,
        "camino": camino,
        "costo": calcular_costo(camino) if camino else math.inf,
        "pasos": len(camino) - 1 if camino else 0,
        "expandidos": expandidos,
        "cantidad_expandidos": len(expandidos),
        "registro": registro
    }


# ------------------------------------------------
# 5. INTERFAZ GRÁFICA (Ventana Compacta)
# ------------------------------------------------
class LaboratorioBusquedaCompacto:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Laboratorio de Búsqueda IA - Casa a Universidad")
        self.ventana.geometry("950x700")  # Pantalla más pequeña y cómoda
        self.ventana.minsize(800, 650)

        self.inicio = "A"
        self.objetivo = "J"
        self.resultados = {}
        self.modo_seleccion = tk.StringVar(value="Inicio")

        self.construir_interfaz()
        self.dibujar_grafo()
        self.mostrar_instrucciones()

    def construir_interfaz(self):
        encabezado = ttk.Frame(self.ventana, padding=8)
        encabezado.pack(fill="x")

        ttk.Label(
            encabezado,
            text="LABORATORIO DE BÚSQUEDA IA (CASA A UNIVERSIDAD)",
            font=("Arial", 14, "bold"),
            foreground="#2E7D32"
        ).pack(anchor="w")

        ttk.Label(
            encabezado,
            text="Comparación de algoritmos (BFS, DFS, UCS, Greedy, A*) con estimación heurística en minutos."
        ).pack(anchor="w", pady=(2, 0))

        # Controles
        controles = ttk.LabelFrame(self.ventana, text="Configuración de la búsqueda", padding=6)
        controles.pack(fill="x", padx=8, pady=4)

        ttk.Label(controles, text="Origen:").grid(row=0, column=0, padx=4, pady=2, sticky="w")
        self.combo_inicio = ttk.Combobox(controles, values=list(GRAFO.keys()), state="readonly", width=6)
        self.combo_inicio.set(self.inicio)
        self.combo_inicio.grid(row=0, column=1, padx=4, pady=2)
        self.combo_inicio.bind("<<ComboboxSelected>>", self.cambiar_inicio)

        ttk.Label(controles, text="Destino:").grid(row=0, column=2, padx=4, pady=2, sticky="w")
        self.combo_objetivo = ttk.Combobox(controles, values=list(GRAFO.keys()), state="readonly", width=6)
        self.combo_objetivo.set(self.objetivo)
        self.combo_objetivo.grid(row=0, column=3, padx=4, pady=2)
        self.combo_objetivo.bind("<<ComboboxSelected>>", self.cambiar_objetivo)

        ttk.Label(controles, text="Algoritmo:").grid(row=0, column=4, padx=4, pady=2, sticky="w")
        self.combo_algoritmo = ttk.Combobox(
            controles,
            values=["BFS", "DFS", "UCS", "Greedy", "A*"],
            state="readonly",
            width=10
        )
        self.combo_algoritmo.set("A*")
        self.combo_algoritmo.grid(row=0, column=5, padx=4, pady=2)

        ttk.Button(controles, text="Ejecutar", command=self.ejecutar_individual).grid(row=0, column=6, padx=6, pady=2)
        ttk.Button(controles, text="Comparar 5", command=self.comparar_todos).grid(row=0, column=7, padx=6, pady=2)
        ttk.Button(controles, text="Reiniciar", command=self.reiniciar).grid(row=0, column=8, padx=6, pady=2)

        # Leyenda
        leyenda = ttk.Frame(self.ventana, padding=(8, 2))
        leyenda.pack(fill="x")
        ttk.Label(leyenda, text="Leyenda: ").pack(side="left")
        for texto, color, fg_c in [
            ("Inicio", COLOR_INICIO, "white"),
            ("Objetivo", COLOR_OBJETIVO, "white"),
            ("Expandido", COLOR_EXPANDIDO, "black"),
            ("Ruta final", COLOR_RUTA, "white")
        ]:
            tk.Label(leyenda, text=f"  {texto}  ", bg=color, fg=fg_c, relief="groove", padx=3).pack(side="left", padx=3)

        # Área Principal
        principal = ttk.Panedwindow(self.ventana, orient="horizontal")
        principal.pack(fill="both", expand=True, padx=8, pady=4)

        marco_grafo = ttk.LabelFrame(principal, text="Mapa de la Ciudad (Grafo Ponderado)", padding=4)
        principal.add(marco_grafo, weight=3)

        self.canvas = tk.Canvas(marco_grafo, bg="white", width=500, height=400, highlightthickness=1, highlightbackground="#C8E6C9")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Button-1>", self.clic_en_grafo)

        marco_registro = ttk.LabelFrame(principal, text="Registro Explicativo y Bitácora", padding=4)
        principal.add(marco_registro, weight=2)

        self.registro = tk.Text(marco_registro, width=38, height=18, wrap="word", font=("Consolas", 9))
        barra = ttk.Scrollbar(marco_registro, orient="vertical", command=self.registro.yview)
        self.registro.configure(yscrollcommand=barra.set)
        self.registro.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        # Tabla inferior
        marco_tabla = ttk.LabelFrame(self.ventana, text="Métricas de Resultados", padding=4)
        marco_tabla.pack(fill="x", padx=8, pady=(0, 6))

        columnas = ("algoritmo", "ruta", "pasos", "costo", "expandidos")
        self.tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", height=4)
        encabezados = {
            "algoritmo": "Algoritmo",
            "ruta": "Ruta Encontrada",
            "pasos": "Aristas",
            "costo": "Costo Total",
            "expandidos": "Nodos Expandidos"
        }
        anchos = {"algoritmo": 90, "ruta": 320, "pasos": 60, "costo": 80, "expandidos": 110}

        for columna in columnas:
            self.tabla.heading(columna, text=encabezados[columna])
            self.tabla.column(columna, width=anchos[columna], anchor="w" if columna == "ruta" else "center")

        self.tabla.pack(fill="x")

    def dibujar_grafo(self, camino=None, expandidos=None):
        camino = camino or []
        expandidos = expandidos or []
        self.canvas.delete("all")

        for origen, vecinos in GRAFO.items():
            x1, y1 = POSICIONES[origen]
            for destino, peso in vecinos.items():
                x2, y2 = POSICIONES[destino]
                en_ruta = (len(camino) > 1 and any(camino[i] == origen and camino[i + 1] == destino for i in range(len(camino) - 1)))

                color = "#8E24AA" if en_ruta else "#B0BEC5"
                grosor = 4 if en_ruta else 2

                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=grosor, arrow=tk.LAST, arrowshape=(8, 10, 4))

                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                self.canvas.create_rectangle(mx - 10, my - 8, mx + 10, my + 8, fill="white", outline="")
                self.canvas.create_text(mx, my, text=str(peso), fill="#1B5E20", font=("Arial", 8, "bold"))

        for nodo, (x, y) in POSICIONES.items():
            if nodo == self.inicio:
                color, fg_t = COLOR_INICIO, "white"
            elif nodo == self.objetivo:
                color, fg_t = COLOR_OBJETIVO, "white"
            elif nodo in camino:
                color, fg_t = COLOR_RUTA, "white"
            elif nodo in expandidos:
                color, fg_t = COLOR_EXPANDIDO, "black"
            else:
                color, fg_t = COLOR_NORMAL, "black"

            radio = 22
            self.canvas.create_oval(x-radio, y-radio, x+radio, y+radio, fill=color, outline="#2E7D32", width=2)
            self.canvas.create_text(x, y - 5, text=nodo, font=("Arial", 11, "bold"), fill=fg_t)
            self.canvas.create_text(x, y + 9, text=f"h={HEURISTICA_HASTA_J[nodo]}", font=("Arial", 7), fill=fg_t)

    def clic_en_grafo(self, evento):
        x, y = evento.x, evento.y
        for nodo, (nx, ny) in POSICIONES.items():
            if (nx - 25 <= x <= nx + 25 and ny - 25 <= y <= ny + 25):
                if self.modo_seleccion.get() == "Inicio":
                    self.inicio = nodo
                    self.combo_inicio.set(nodo)
                    self.modo_seleccion.set("Objetivo")
                    self.escribir(f"Origen: {nodo}. Selecciona el destino.")
                else:
                    self.objetivo = nodo
                    self.combo_objetivo.set(nodo)
                    self.modo_seleccion.set("Inicio")
                    self.escribir(f"Destino: {nodo}.")
                self.resultados.clear()
                self.actualizar_tabla()
                self.dibujar_grafo()
                break

    def cambiar_inicio(self, _e=None):
        self.inicio = self.combo_inicio.get()
        self.limpiar_resultados()

    def cambiar_objetivo(self, _e=None):
        self.objetivo = self.combo_objetivo.get()
        self.limpiar_resultados()

    def limpiar_resultados(self):
        self.resultados.clear()
        self.actualizar_tabla()
        self.dibujar_grafo()
        self.escribir(f"Ruta configurada de {self.inicio} a {self.objetivo}.")

    def ejecutar_algoritmo(self, nombre):
        if self.inicio == self.objetivo:
            return crear_resultado(nombre, [self.inicio], [self.inicio], ["Origen y destino iguales."])
        
        heuristica_activa = HEURISTICA_HASTA_J if self.objetivo == "J" else {n: 0 for n in GRAFO}
        
        if nombre == "BFS": return bfs(self.inicio, self.objetivo)
        if nombre == "DFS": return dfs(self.inicio, self.objetivo)
        if nombre == "UCS": return ucs(self.inicio, self.objetivo)
        if nombre == "Greedy": return greedy(self.inicio, self.objetivo, heuristica_activa)
        if nombre == "A*": return astar(self.inicio, self.objetivo, heuristica_activa)
        raise ValueError(f"Algoritmo desconocido: {nombre}")

    def ejecutar_individual(self):
        nombre = self.combo_algoritmo.get()
        resultado = self.ejecutar_algoritmo(nombre)
        self.resultados = {nombre: resultado}
        self.actualizar_tabla()
        self.dibujar_grafo(resultado["camino"], resultado["expandidos"])
        self.mostrar_resultado(resultado)

    def comparar_todos(self):
        self.resultados = {}
        for nombre in ["BFS", "DFS", "UCS", "Greedy", "A*"]:
            self.resultados[nombre] = self.ejecutar_algoritmo(nombre)
        self.actualizar_tabla()
        
        resultado_astar = self.resultados["A*"]
        self.dibujar_grafo(resultado_astar["camino"], resultado_astar["expandidos"])

        self.registro.delete("1.0", tk.END)
        self.registro.insert(tk.END, f"COMPARATIVA GENERAL: {self.inicio} -> {self.objetivo}\n" + "="*35 + "\n\n")

        for nombre, resultado in self.resultados.items():
            ruta = " -> ".join(resultado["camino"]) if resultado["camino"] else "Sin ruta"
            costo = str(resultado["costo"]) if math.isfinite(resultado["costo"]) else "N/A"
            self.registro.insert(tk.END, f"[{nombre}]\n  Ruta: {ruta}\n  Costo: {costo}\n  Expandidos: {resultado['cantidad_expandidos']}\n\n")

    def actualizar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        for nombre in ["BFS", "DFS", "UCS", "Greedy", "A*"]:
            if nombre not in self.resultados: continue
            r = self.resultados[nombre]
            ruta = " -> ".join(r["camino"]) if r["camino"] else "Sin ruta"
            costo = f"{r['costo']:.1f}" if math.isfinite(r['costo']) else "—"
            self.tabla.insert("", "end", values=(nombre, ruta, r["pasos"], costo, r["cantidad_expandidos"]))

    def mostrar_resultado(self, r):
        self.registro.delete("1.0", tk.END)
        self.registro.insert(tk.END, f"ALGORITMO: {r['algoritmo']}\nORIGEN: {self.inicio} | DESTINO: {self.objetivo}\n" + "="*35 + "\n\n")
        for linea in r['registro']: self.registro.insert(tk.END, linea + "\n")

    def mostrar_instrucciones(self):
        self.escribir(
            "INFORMACIÓN DEL ESCENARIO:\n"
            "• Queremos ir desde la CASA (A) hasta la UNIVERSIDAD (J).\n"
            "• h = Estimación en minutos de camino.\n"
            "• Selecciona un algoritmo y ejecuta o haz clic en los nodos del mapa.\n"
        )

    def escribir(self, texto):
        self.registro.insert(tk.END, texto + "\n")
        self.registro.see(tk.END)

    def reiniciar(self):
        self.inicio = "A"
        self.objetivo = "J"
        self.combo_inicio.set(self.inicio)
        self.combo_objetivo.set(self.objetivo)
        self.combo_algoritmo.set("A*")
        self.resultados.clear()
        self.actualizar_tabla()
        self.dibujar_grafo()
        self.registro.delete("1.0", tk.END)
        self.mostrar_instrucciones()

if __name__ == "__main__":
    ventana = tk.Tk()
    app = LaboratorioBusquedaCompacto(ventana)
    ventana.mainloop()