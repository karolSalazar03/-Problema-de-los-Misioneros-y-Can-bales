
import time
from collections import deque

# 1. FORMULACIÓN DEL PROBLEMA (ESTADOS)
# Estado representado como una tupla: (misioneros_izq, canibales_izq, bote_izq)
ESTADO_INICIAL = (3, 3, 1)
ESTADO_OBJETIVO = (0, 0, 0)

def es_valido(estado):
    """
    Verifica si un estado no rompe las reglas del juego.
    """
    m, c, b = estado
    # Restricción 1: No pueden haber números negativos ni mayores a 3
    if m < 0 or c < 0 or m > 3 or c > 3:
        return False
        
    # Restricción 2: Misioneros en la izquierda no pueden ser superados por caníbales
    if m > 0 and m < c:
        return False
        
    # Restricción 3: Misioneros en la derecha no pueden ser superados por caníbales
    m_der = 3 - m
    c_der = 3 - c
    if m_der > 0 and m_der < c_der:
        return False
        
    return True

def obtener_sucesores(estado):
    """
    Modelo de Transición: Dado un estado, genera los estados hijos válidos.
    """
    sucesores = []
    m, c, b = estado
    # Acciones posibles (misioneros_a_mover, canibales_a_mover)
    acciones = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
    
    for am, ac in acciones:
        if b == 1:
            # Bote en la izquierda, viaja a la derecha (restamos de la izquierda)
            nuevo_estado = (m - am, c - ac, 0)
            movimiento = f"Mover {am}M, {ac}C a la Derecha ->"
        else:
            # Bote en la derecha, viaja a la izquierda (sumamos a la izquierda)
            nuevo_estado = (m + am, c + ac, 1)
            movimiento = f"<- Mover {am}M, {ac}C a la Izquierda"
            
        if es_valido(nuevo_estado):
            sucesores.append((nuevo_estado, movimiento))
            
    return sucesores

# 2. ALGORITMOS DE BÚSQUEDA CIEGA

def busqueda_bfs():
    """Búsqueda en Anchura (Queue / Cola)"""
    inicio_tiempo = time.perf_counter()
    # Frontera almacena: (estado_actual, camino_hasta_aqui)
    frontera = deque([(ESTADO_INICIAL, [])])
    visitados = {ESTADO_INICIAL}
    nodos_expandidos = 0
    
    while frontera:
        estado_actual, camino = frontera.popleft()
        nodos_expandidos += 1
        
        if estado_actual == ESTADO_OBJETIVO:
            tiempo_total = time.perf_counter() - inicio_tiempo
            return camino, nodos_expandidos, tiempo_total
            
        for sucesor, accion in obtener_sucesores(estado_actual):
            if sucesor not in visitados:
                visitados.add(sucesor)
                nuevo_camino = camino + [(estado_actual, accion, sucesor)]
                frontera.append((sucesor, nuevo_camino))
                
    return None, nodos_expandidos, time.perf_counter() - inicio_tiempo

def busqueda_dfs():
    """Búsqueda en Profundidad (Stack / Pila)"""
    inicio_tiempo = time.perf_counter()
    # Pila almacena: (estado_actual, camino_hasta_aqui)
    pila = [(ESTADO_INICIAL, [])]
    visitados = {ESTADO_INICIAL}
    nodos_expandidos = 0
    
    while pila:
        estado_actual, camino = pila.pop()
        nodos_expandidos += 1
        
        if estado_actual == ESTADO_OBJETIVO:
            tiempo_total = time.perf_counter() - inicio_tiempo
            return camino, nodos_expandidos, tiempo_total
            
        for sucesor, accion in obtener_sucesores(estado_actual):
            if sucesor not in visitados:
                visitados.add(sucesor)
                nuevo_camino = camino + [(estado_actual, accion, sucesor)]
                pila.append((sucesor, nuevo_camino))
                
    return None, nodos_expandidos, time.perf_counter() - inicio_tiempo