class Nodo:
    """
    Representa un vértice en el grafo.
    """
    def __init__(self, id_nodo: int, etiqueta: str = ""):
        self.id_nodo = id_nodo
        # Si no se provee etiqueta, usamos el ID como texto por defecto
        self.etiqueta = etiqueta if etiqueta else str(id_nodo)
        
    def __hash__(self):
        # Necesario para usar nodos como llaves en diccionarios o conjuntos
        return hash(self.id_nodo)
        
    def __eq__(self, otro):
        # Permite comparar si dos objetos Nodo son lógicamente el mismo
        if isinstance(otro, Nodo):
            return self.id_nodo == otro.id_nodo
        return False
        
    def __str__(self):
        return f"Nodo({self.etiqueta})"
