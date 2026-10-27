# ============================================================
# BÚSQUEDA HEURÍSTICA CON SUMA TOTAL DE COSTOS (A -> J)
# ============================================================

# Estructura del árbol basado en tu imagen
acciones = {
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

# Valores de la heurística proporcionados para cada nodo: h(n)
heuristicas = {
    "A": 7,
    "B": 6,
    "C": 4,
    "D": 7,
    "E": 5,
    "F": 3,
    "G": 6,
    "H": 8,
    "I": 1,
    "J": 0
}

def busqueda_con_costos_totales(inicio, objetivo):
    # Suma de todas las letras del árbol
    suma_todas_heuristicas = sum(heuristicas.values())
    print(f"=== SUMA TOTAL DE LAS HEURÍSTICAS DE TODO EL ÁRBOL ===")
    print(f"Valores: {heuristicas}")
    print(f"Suma total de h(n) de todas las letras = {suma_todas_heuristicas}\n")
    print("=" * 55 + "\n")

    g_inicial = 0
    h_inicial = heuristicas.get(inicio, 0)
    f_inicial = g_inicial + h_inicial

    frontera = [(f_inicial, g_inicial, inicio, [inicio])]
    visitados = set()

    print(f"=== INICIANDO BÚSQUEDA (De '{inicio}' a '{objetivo}') ===\n")

    while frontera:
        frontera.sort(key=lambda x: (x[0], x[1]))
        f_actual, g_actual, actual, camino = frontera.pop(0)
        h_actual = heuristicas.get(actual, 0)

        print(f"Nodo actual: '{actual}'")
        print(f"  -> Costo recorrido g(n) = {g_actual} pasos")
        print(f"  -> Costo estimado h(n) = {h_actual}")
        print(f"  -> Costo total f(n) = g(n) + h(n) = {f_actual}")
        print(f"  -> Camino: {' → '.join(camino)}")

        if actual == objetivo:
            # Calcular la suma de h(n) de los nodos que forman parte de la ruta óptima
            suma_ruta = sum(heuristicas[nodo] for nodo in camino)
            print(f"\n★ ¡Meta alcanzada! Ruta óptima: {' → '.join(camino)}")
            print(f"Costo total de pasos (g): {g_actual}")
            print(f"Suma de las heurísticas h(n) en la ruta óptima: {suma_ruta}")
            return camino

        visitados.add(actual)

        vecinos = acciones.get(actual, [])
        if vecinos:
            print(f"  -> Hijos evaluados:")
            for vecino in vecinos:
                if vecino not in visitados:
                    g_vecino = g_actual + 1
                    h_vecino = heuristicas.get(vecino, 0)
                    f_vecino = g_vecino + h_vecino
                    
                    nuevo_camino = camino + [vecino]
                    frontera.append((f_vecino, g_vecino, vecino, nuevo_camino))
                    print(f"     * '{vecino}' -> g({g_vecino}) + h({h_vecino}) = f({f_vecino})")

        print("-" * 50)

    print("\nNo se encontró una ruta disponible hacia el objetivo.")
    return None

if __name__ == "__main__":
    busqueda_con_costos_totales("A", "J")