from typing import List, Dict
from modelos.nodo import Nodo
from modelos.arista import Arista

class Grafo:
    """
    Representa el grafo principal utilizando listas de adyacencia.
    Estructura dirigida, ponderada y preparada para verificar si es acíclica.
    """
    def __init__(self):
        # Diccionario para almacenar los nodos: { id_nodo : objeto Nodo }
        self.nodos: Dict[int, Nodo] = {}
        
        # Lista de adyacencia: { id_nodo : [lista de objetos Arista salientes] }
        # Esto es clave para grafos dirigidos (las aristas apuntan en un solo sentido)
        self.adyacencia: Dict[int, List[Arista]] = {}
        
    def agregar_nodo(self, id_nodo: int, etiqueta: str = "") -> Nodo:
        """Agrega un nodo al grafo si no existe previamente."""
        if id_nodo not in self.nodos:
            nuevo_nodo = Nodo(id_nodo, etiqueta)
            self.nodos[id_nodo] = nuevo_nodo
            self.adyacencia[id_nodo] = []
        return self.nodos[id_nodo]
        
    def agregar_arista(self, id_origen: int, id_destino: int, peso: float):
        """Agrega una arista dirigida entre dos nodos existentes."""
        if id_origen not in self.nodos or id_destino not in self.nodos:
            raise ValueError("Ambos nodos deben existir antes de crear una arista.")
            
        origen = self.nodos[id_origen]
        destino = self.nodos[id_destino]
        
        nueva_arista = Arista(origen, destino, peso)
        # Solo lo agregamos a la lista de adyacencia del origen (grafo dirigido)
        self.adyacencia[id_origen].append(nueva_arista)
        
    def obtener_sucesores(self, id_nodo: int) -> List[Arista]:
        """Retorna todas las aristas que salen de un nodo específico."""
        return self.adyacencia.get(id_nodo, [])
        
    def cantidad_nodos(self) -> int:
        return len(self.nodos)
        
    def obtener_todos_los_nodos(self) -> List[Nodo]:
        return list(self.nodos.values())
        
    def reiniciar_grafo(self):
        """Limpia todo el estado del grafo."""
        self.nodos.clear()
        self.adyacencia.clear()
