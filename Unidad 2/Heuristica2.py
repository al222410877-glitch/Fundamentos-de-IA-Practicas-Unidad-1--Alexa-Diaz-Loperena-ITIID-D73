# ============================================================
# BÚSQUEDA CON HEAPQ Y COSTOS ACUMULADOS (A -> J) EN TERMINAL
# ============================================================

import heapq

# Estructura del árbol con los costos de transición hacia cada hijo
# Formato: "NodoPadre": [("NodoHijo", costo_arista), ...]
acciones_con_costos = {
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

# Valores de los nodos provistos
valores_nodos = {
    "A": 0, "B": 2, "C": 5, "D": 4, "E": 1, 
    "F": 2, "G": 8, "H": 3, "I": 2, "J": 3
}

def busqueda_heapq_costos(inicio, objetivo):
    inicio_mayus = inicio.upper()
    objetivo_mayus = objetivo.upper()
    
    # El heap almacena tuplas: (costo_acumulado, nodo_actual, camino)
    # heapq ordena automáticamente basándose en el primer elemento (el costo acumulado menor)
    costo_inicial = 0
    heap = [(costo_inicial, inicio_mayus, [inicio_mayus])]
    
    # Diccionario para almacenar el menor costo conocido para llegar a cada nodo
    costos_visitados = {inicio_mayus: 0}

    print(f"=== INICIANDO BÚSQUEDA CON HEAPQ (De '{inicio_mayus}' a '{objetivo_mayus}') ===\n")

    while heap:
        # Extraer el elemento con el menor costo acumulado
        costo_actual, actual, camino = heapq.heappop(heap)

        print(f"Explorando nodo: '{actual}' | Costo acumulado g(n) = {costo_actual} | Camino: {' → '.join(camino)}")

        if actual == objetivo_mayus:
            print(f"\n" + "=" * 50)
            print(f"★ RUTA ÓPTIMA ENCONTRADA (HEAPQ): {' → '.join(camino)}")
            print(f"★ Costo acumulado total mínimo: {costo_actual}")
            print("=" * 50)
            return camino

        # Evaluar vecinos y sus costos de arista
        hijos = acciones_con_costos.get(actual, [])
        if hijos:
            print(f"  -> Hijos disponibles:")
            for hijo, costo_arista in hijos:
                # Sumar el costo acumulado actual más el costo de la arista hacia el hijo
                nuevo_costo = costo_actual + costo_arista
                
                # Si el nodo no ha sido visitado o encontramos un camino con menor costo
                if hijo not in costos_visitados or nuevo_costo < costos_visitados[hijo]:
                    costos_visitados[hijo] = nuevo_costo
                    nuevo_camino = camino + [hijo]
                    heapq.heappush(heap, (nuevo_costo, hijo, nuevo_camino))
                    print(f"     * Añadiendo '{hijo}' (Costo arista: {costo_arista}) -> Costo acumulado total: {nuevo_costo}")

        print("-" * 50)

    print("\nNo se encontró una ruta disponible hacia el objetivo.")
    return None

if __name__ == "__main__":
    busqueda_heapq_costos("A", "J")