import math
from typing import List, Dict, Set
from modelos.grafo import Grafo

class Dijkstra:
    """
    Motor matemático para resolver el Problema del Camino Mínimo.
    Diseñado específicamente para soportar el almacenamiento de múltiples caminos óptimos.
    """
    def __init__(self, grafo: Grafo):
        self.grafo = grafo
        # Tablas de estado del algoritmo
        self.distancias: Dict[int, float] = {}
        
        # IMPORTANTE: A diferencia del Dijkstra básico que guarda un (1) predecesor,
        # aquí usamos una lista de predecesores para cada nodo. Esto permite registrar
        # empates si dos rutas distintas cuestan exactamente lo mismo.
        self.predecesores: Dict[int, List[int]] = {}
        
        self.visitados: Set[int] = set()
        
    def ejecutar(self, id_origen: int):
        """
        Ejecuta el algoritmo desde un vértice origen hacia todos los demás.
        """
        # 1. Inicialización de distancias y predecesores
        for nodo in self.grafo.obtener_todos_los_nodos():
            self.distancias[nodo.id_nodo] = math.inf
            self.predecesores[nodo.id_nodo] = []
            
        # La distancia al propio origen siempre es 0
        self.distancias[id_origen] = 0.0
        self.visitados.clear()
        
        # Nodos que aún no hemos marcado como visitados (definitivos)
        nodos_pendientes = set(self.distancias.keys())
        
        while nodos_pendientes:
            # 2. Selección del vértice con menor distancia temporal
            # Extraemos el nodo no visitado que tenga el menor valor en el diccionario de distancias
            nodo_actual = min(nodos_pendientes, key=lambda n: self.distancias[n])
            
            # Condición de parada temprana: si el nodo más cercano está a distancia infinita,
            # significa que los nodos restantes están completamente desconectados (son inalcanzables).
            if self.distancias[nodo_actual] == math.inf:
                break
                
            # 3. Marcado de vértice visitado
            nodos_pendientes.remove(nodo_actual)
            self.visitados.add(nodo_actual)
            
            # 4. Evaluación de vecinos
            for arista in self.grafo.obtener_sucesores(nodo_actual):
                vecino = arista.destino.id_nodo
                
                if vecino in self.visitados:
                    continue # Ya conocemos su distancia mínima definitiva
                    
                # Distancia calculada si pasamos por el 'nodo_actual'
                nueva_distancia = self.distancias[nodo_actual] + arista.peso
                
                # 5. Actualización de distancias y predecesores (Relajación)
                if nueva_distancia < self.distancias[vecino]:
                    # Encontramos un camino ESTRICTAMENTE mejor. Descartamos los anteriores.
                    self.distancias[vecino] = nueva_distancia
                    self.predecesores[vecino] = [nodo_actual]
                    
                elif nueva_distancia == self.distancias[vecino]:
                    # Encontramos un camino ALTERNATIVO con el mismo costo exacto.
                    # Mantenemos los anteriores y agregamos este nuevo predecesor.
                    self.predecesores[vecino].append(nodo_actual)
                    
    def obtener_caminos_minimos(self, id_destino: int) -> List[List[int]]:
        """
        Reconstruye y devuelve TODOS los caminos mínimos encontrados hacia un destino.
        Utiliza recursividad (backtracking) para explorar todas las ramificaciones.
        """
        # Si el destino es inalcanzable, retornamos lista vacía
        if self.distancias.get(id_destino, math.inf) == math.inf:
            return []
            
        caminos_completos = []
        
        def backtrack(nodo_actual: int, camino_parcial: List[int]):
            # Caso base: Si no hay predecesores, significa que llegamos al origen
            if not self.predecesores[nodo_actual]:
                # El camino se armó de atrás hacia adelante (Destino -> Origen)
                # Lo invertimos antes de guardarlo (Origen -> Destino)
                caminos_completos.append(camino_parcial[::-1])
                return
                
            # Llamada recursiva por cada posible ruta que empató
            for pred in self.predecesores[nodo_actual]:
                camino_parcial.append(pred)      # Avanzamos hacia atrás
                backtrack(pred, camino_parcial)  # Exploramos esa ruta
                camino_parcial.pop()             # Deshacemos para probar otra opción
                
        # Arrancamos la reconstrucción desde el final (destino)
        backtrack(id_destino, [id_destino])
        return caminos_completos

    def ejecutar_paso_a_paso(self, id_origen: int):
        """
        Generador de Python que cede (yield) el control y el estado actual del algoritmo 
        en cada iteración lógica. Esto permite a la UI pintar paso a paso sin bloquearse.
        """
        for nodo in self.grafo.obtener_todos_los_nodos():
            self.distancias[nodo.id_nodo] = math.inf
            self.predecesores[nodo.id_nodo] = []
            
        self.distancias[id_origen] = 0.0
        self.visitados.clear()
        nodos_pendientes = set(self.distancias.keys())
        
        # Emitimos el estado inicial
        yield {"estado": "INICIO", "nodo_actual": id_origen, "visitados": set(self.visitados), "distancias": dict(self.distancias)}
        
        while nodos_pendientes:
            nodo_actual = min(nodos_pendientes, key=lambda n: self.distancias[n])
            
            if self.distancias[nodo_actual] == math.inf:
                break
                
            nodos_pendientes.remove(nodo_actual)
            self.visitados.add(nodo_actual)
            
            # Emitimos cuando un nodo se marca como visitado/definitivo
            yield {"estado": "VISITADO", "nodo_actual": nodo_actual, "visitados": set(self.visitados), "distancias": dict(self.distancias)}
            
            for arista in self.grafo.obtener_sucesores(nodo_actual):
                vecino = arista.destino.id_nodo
                if vecino in self.visitados:
                    continue 
                    
                nueva_distancia = self.distancias[nodo_actual] + arista.peso
                cambio_realizado = False
                
                if nueva_distancia < self.distancias[vecino]:
                    self.distancias[vecino] = nueva_distancia
                    self.predecesores[vecino] = [nodo_actual]
                    cambio_realizado = True
                elif nueva_distancia == self.distancias[vecino]:
                    self.predecesores[vecino].append(nodo_actual)
                    cambio_realizado = True
                    
                # Emitimos la evaluación de aristas
                yield {
                    "estado": "EVALUANDO", 
                    "nodo_actual": nodo_actual, 
                    "vecino": vecino, 
                    "hubo_cambio": cambio_realizado,
                    "visitados": set(self.visitados), 
                    "distancias": dict(self.distancias)
                }
                
        # Emitimos estado final
        yield {"estado": "FIN", "nodo_actual": None, "visitados": set(self.visitados), "distancias": dict(self.distancias)}
