import random
from modelos.grafo import Grafo
from servicios.validador_grafo import ValidadorGrafo

class GeneradorAleatorio:
    """
    Clase utilitaria para generar Grafos Dirigidos Acíclicos (DAG) aleatorios,
    cumpliendo con las restricciones del proyecto.
    """
    
    @staticmethod
    def generar_dag(num_nodos: int, min_peso: int = 1, max_peso: int = 20) -> Grafo:
        """
        Genera un grafo aleatorio asegurando que sea dirigido, conexo hacia adelante
        y sin ciclos (DAG).
        
        Args:
            num_nodos: Cantidad de vértices (entre 7 y 16 según enunciado).
            min_peso: Peso mínimo de la arista.
            max_peso: Peso máximo de la arista.
            
        Retorna:
            Instancia de Grafo validada.
        """
        if num_nodos < 7 or num_nodos > 16:
            raise ValueError("La cantidad de nodos debe estar entre 7 y 16, según los requisitos oficiales.")
            
        grafo = Grafo()
        
        # 1. Crear los nodos (1 hasta num_nodos)
        for i in range(1, num_nodos + 1):
            grafo.agregar_nodo(i, f"N{i}")
            
        # 2. Conectividad base (Árbol de expansión dirigido hacia adelante)
        # Para evitar que existan nodos aislados, cada nodo (desde el 2 en adelante)
        # recibirá al menos una arista proveniente de un nodo menor a él.
        # Esto matemáticamente nos asegura que NO hay ciclos (porque origen < destino siempre).
        for i in range(2, num_nodos + 1):
            origen = random.randint(1, i - 1)
            peso = random.randint(min_peso, max_peso)
            grafo.agregar_arista(origen, i, float(peso))
            
        # 3. Añadir aristas cruzadas adicionales para darle complejidad al grafo
        # Recorremos todas las parejas (u, v) donde u < v
        probabilidad_conexion = 0.3 # 30% de probabilidad de crear una arista extra
        
        for u in range(1, num_nodos):
            for v in range(u + 1, num_nodos + 1):
                # Verificamos si la arista ya fue creada en el paso 2
                ya_existe = any(arista.destino.id_nodo == v for arista in grafo.obtener_sucesores(u))
                
                if not ya_existe and random.random() < probabilidad_conexion:
                    peso = random.randint(min_peso, max_peso)
                    grafo.agregar_arista(u, v, float(peso))
                    
        # 4. Control de calidad usando el validador del Bloque 4
        # Aunque por construcción matemática (u < v) es imposible que haya ciclos,
        # utilizamos el ValidadorGrafo para demostrar la integración de los módulos
        # y blindar el sistema contra errores lógicos futuros.
        if ValidadorGrafo.tiene_ciclos(grafo):
            raise RuntimeError("Error crítico: El generador produjo un grafo con ciclos.")
            
        return grafo
