from modelos.grafo import Grafo

class ValidadorGrafo:
    """
    Servicio encargado de aplicar algoritmos matemáticos para comprobar
    la integridad y restricciones del grafo.
    """
    
    @staticmethod
    def tiene_ciclos(grafo: Grafo) -> bool:
        """
        Utiliza Búsqueda en Profundidad (DFS - Depth First Search) para detectar 
        si existen ciclos en el grafo dirigido.
        
        Retorna:
            True si hay al menos un ciclo (inválido para el proyecto).
            False si es un Grafo Dirigido Acíclico (DAG) (válido).
        """
        # Conjunto de nodos que ya procesamos completamente
        visitados = set()
        # Conjunto de nodos en el camino o rama actual que estamos explorando
        apilados = set() 
        
        def dfs(id_nodo: int) -> bool:
            visitados.add(id_nodo)
            apilados.add(id_nodo)
            
            # Revisar todos los hijos (aristas salientes) de este nodo
            for arista in grafo.obtener_sucesores(id_nodo):
                id_vecino = arista.destino.id_nodo
                
                # Si el vecino no ha sido visitado, exploramos esa rama
                if id_vecino not in visitados:
                    if dfs(id_vecino):
                        return True
                # Si el vecino ya está en nuestra rama actual de exploración, 
                # significa que hemos regresado sobre nuestros pasos -> ¡Hay un ciclo!
                elif id_vecino in apilados:
                    return True
                    
            # Ya no estamos explorando este nodo, lo quitamos del camino actual
            apilados.remove(id_nodo)
            return False

        # Es posible que el grafo no esté completamente conectado (islas aisladas).
        # Por eso debemos intentar lanzar el DFS desde todos los nodos posibles
        # que no hayan sido visitados aún.
        for nodo in grafo.obtener_todos_los_nodos():
            if nodo.id_nodo not in visitados:
                if dfs(nodo.id_nodo):
                    return True
                    
        return False
