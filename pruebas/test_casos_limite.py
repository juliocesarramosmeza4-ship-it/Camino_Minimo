import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modelos.grafo import Grafo
from algoritmos.dijkstra import Dijkstra
from servicios.validador_grafo import ValidadorGrafo

def correr_pruebas():
    print("--- INICIANDO BATERÍA DE PRUEBAS DE CASOS LÍMITE ---")
    
    # 1. Caso: Origen y destino iguales
    g1 = Grafo()
    g1.agregar_nodo(1)
    d1 = Dijkstra(g1)
    d1.ejecutar(1)
    caminos1 = d1.obtener_caminos_minimos(1)
    assert d1.distancias[1] == 0.0, "Error en Caso 1"
    assert caminos1 == [[1]], "Error en caminos Caso 1"
    print("✓ Caso: Origen y destino iguales (Distancia 0) - Superado")
    
    # 2. Caso: Destino inalcanzable (Grafo desconectado)
    g2 = Grafo()
    g2.agregar_nodo(1)
    g2.agregar_nodo(2)
    # No agregamos arista entre 1 y 2
    d2 = Dijkstra(g2)
    d2.ejecutar(1)
    caminos2 = d2.obtener_caminos_minimos(2)
    assert caminos2 == [], "Error en Caso 2"
    assert d2.distancias[2] == float('inf'), "Error distancia Caso 2"
    print("✓ Caso: Destino inalcanzable (Distancia infinita) - Superado")
    
    # 3. Caso: Múltiples caminos mínimos (Empate exacto)
    g3 = Grafo()
    for i in range(1, 5): g3.agregar_nodo(i)
    g3.agregar_arista(1, 2, 5.0) # Ruta A (1->2->4) peso 10
    g3.agregar_arista(2, 4, 5.0)
    g3.agregar_arista(1, 3, 5.0) # Ruta B (1->3->4) peso 10
    g3.agregar_arista(3, 4, 5.0)
    
    d3 = Dijkstra(g3)
    d3.ejecutar(1)
    caminos3 = d3.obtener_caminos_minimos(4)
    assert d3.distancias[4] == 10.0, "Error peso Caso 3"
    assert len(caminos3) == 2, "Dijkstra no está detectando el empate"
    print("✓ Caso: Múltiples caminos mínimos guardados - Superado")
    
    # 4. Caso: Grafo con ciclo introducido manualmente
    g4 = Grafo()
    for i in range(1, 4): g4.agregar_nodo(i)
    g4.agregar_arista(1, 2, 1.0)
    g4.agregar_arista(2, 3, 1.0)
    g4.agregar_arista(3, 1, 1.0) # Ciclo
    hay_ciclo = ValidadorGrafo.tiene_ciclos(g4)
    assert hay_ciclo == True, "El validador no detectó el ciclo"
    print("✓ Caso: Detección estricta de ciclos (Validador DAG) - Superado")
    
    # 5. Caso: Entrada de arista con peso negativo
    g5 = Grafo()
    g5.agregar_nodo(1)
    g5.agregar_nodo(2)
    try:
        g5.agregar_arista(1, 2, -5.0)
        print("✗ Error: El sistema permitió un peso negativo.")
    except ValueError:
        print("✓ Caso: Rechazo automático de pesos negativos - Superado")
        
    print("--- TODAS LAS PRUEBAS PASARON EXITOSAMENTE ---")

if __name__ == "__main__":
    correr_pruebas()
