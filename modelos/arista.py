from modelos.nodo import Nodo

class Arista:
    """
    Representa una conexión dirigida con un peso entre dos nodos.
    """
    def __init__(self, origen: Nodo, destino: Nodo, peso: float):
        # El algoritmo de Dijkstra puro no soporta ciclos de peso negativo,
        # y usualmente no se usa con pesos negativos. Lo validamos de entrada.
        if peso < 0:
            raise ValueError("El algoritmo de Dijkstra no admite pesos negativos.")
            
        self.origen = origen
        self.destino = destino
        self.peso = peso
        
    def __str__(self):
        return f"{self.origen.etiqueta} --({self.peso})--> {self.destino.etiqueta}"
