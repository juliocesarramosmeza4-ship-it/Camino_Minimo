import customtkinter as ctk
import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con PyInstaller (_MEIPASS) y desarrollo local"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

from ui.panel_configuracion import PanelConfiguracion
from ui.panel_grafo import PanelGrafo
from generadores.grafo_aleatorio import GeneradorAleatorio
from modelos.grafo import Grafo
from servicios.validador_grafo import ValidadorGrafo
from algoritmos.dijkstra import Dijkstra

from ui.ventana_inicio import VentanaInicio

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Dijkstra Visualizer Pro")
        
        # Intentar cargar el ícono si existe
        try:
            self.iconbitmap(resource_path("icono.ico"))
        except Exception:
            pass
            
        # Pantalla completa por defecto (Maximizado en Windows)
        self.after(0, lambda: self.state('zoomed'))
        self.minsize(800, 500)
        self.configure(fg_color="#F0F2F5")
        
        # Mostrar pantalla de inicio
        self.pantalla_inicio = VentanaInicio(self, self._iniciar_app_principal)
        self.pantalla_inicio.pack(fill="both", expand=True)
        
    def _iniciar_app_principal(self, nodos_iniciales):
        
        # Dividir la ventana en un layout de grilla (1 fila, 2 columnas)
        # La columna 1 (derecha) será expandible
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # --- Panel Izquierdo: Configuración ---
        self.panel_config = PanelConfiguracion(self, self.manejador_generar_aleatorio, self.manejador_cambiar_tema, fg_color="white", corner_radius=15)
        self.panel_config.grid(row=0, column=0, sticky="nswe", padx=15, pady=15)
        
        # Vincular callbacks de modo manual y algoritmo
        self.panel_config.on_iniciar_manual = self.manejador_iniciar_manual
        self.panel_config.on_agregar_arista = self.manejador_agregar_arista
        self.panel_config.on_ejecutar_dijkstra = self.manejador_ejecutar_dijkstra
        self.panel_config.on_iniciar_pasos = self.manejador_iniciar_pasos
        self.panel_config.on_siguiente_paso = self.manejador_siguiente_paso
        
        # --- Panel Derecho: Área de Dibujo ---
        self.panel_grafo = PanelGrafo(self, fg_color="#1E1E24", corner_radius=15)
        self.panel_grafo.grid(row=0, column=1, sticky="nswe", padx=(0, 15), pady=15)
        
        # Conectar callback de clic en grafo
        self.panel_grafo.on_nodo_click = self.manejador_nodo_click
        
        # Estado de la aplicación
        self.grafo_actual = None
        self.generador_pasos = None
        self.destino_actual = None
        
        # Switch de tema global (esquina superior derecha)
        self.switch_tema = ctk.CTkSwitch(self, text="Modo Oscuro", command=self._toggle_tema_app, font=("Inter", 12), text_color="white")
        self.switch_tema.select()
        self.switch_tema.place(relx=0.98, rely=0.02, anchor="ne")
        
        # Forzar el tema oscuro inicial en todos los componentes
        self.manejador_cambiar_tema(True)
        
        # Generar grafo inicial con el valor de la pantalla de bienvenida
        self.manejador_generar_aleatorio(nodos_iniciales)
        
    def manejador_cambiar_tema(self, modo_oscuro):
        if modo_oscuro:
            self.configure(fg_color="#111827") # Fondo ventana más oscuro
            self.panel_config.configure(fg_color="#1F2937")
            # Cambiar frames internos
            for frame in [self.panel_config.frame_init, self.panel_config.frame_manual, self.panel_config.frame_dijkstra, self.panel_config.frame_tabla]:
                frame.configure(fg_color="#374151", border_color="#4B5563")
                
            self.panel_config.lbl_titulo.configure(text_color="white")
            self.panel_config.lbl_nodos.configure(text_color="#E5E7EB")
            self.panel_config.lbl_manual.configure(text_color="white")
            self.panel_config.lbl_origen.configure(text_color="#E5E7EB")
            self.panel_config.lbl_destino.configure(text_color="#E5E7EB")
            self.panel_config.lbl_peso.configure(text_color="#E5E7EB")
            self.panel_config.lbl_dijkstra.configure(text_color="white")
            self.panel_config.lbl_origen_d.configure(text_color="#E5E7EB")
            self.panel_config.lbl_destino_d.configure(text_color="#E5E7EB")
            self.panel_config.lbl_tabla_titulo.configure(text_color="white")
            self.panel_config.lbl_col_origen.configure(text_color="#E5E7EB")
            self.panel_config.lbl_col_destino.configure(text_color="#E5E7EB")
            self.panel_config.lbl_col_peso.configure(text_color="#E5E7EB")
            self.panel_config.btn_manual.configure(text_color="white", hover_color="#4B5563", border_color="#6B7280")
            
            for lbl in self.panel_config.filas_tabla:
                lbl.configure(text_color="#E5E7EB")
            
            self.panel_grafo.configure(fg_color="#1E1E24")
            self.panel_grafo.set_modo_oscuro(True)
            self.switch_tema.configure(text_color="white")
        else:
            self.configure(fg_color="#F0F2F5") # Fondo ventana claro
            self.panel_config.configure(fg_color="white")
            # Cambiar frames internos
            for frame in [self.panel_config.frame_init, self.panel_config.frame_manual, self.panel_config.frame_dijkstra, self.panel_config.frame_tabla]:
                frame.configure(fg_color="#F9FAFB", border_color="#E5E7EB")
                
            self.panel_config.lbl_titulo.configure(text_color="#1F2937")
            self.panel_config.lbl_nodos.configure(text_color="#374151")
            self.panel_config.lbl_manual.configure(text_color="#1F2937")
            self.panel_config.lbl_origen.configure(text_color="black")
            self.panel_config.lbl_destino.configure(text_color="black")
            self.panel_config.lbl_peso.configure(text_color="black")
            self.panel_config.lbl_dijkstra.configure(text_color="#1F2937")
            self.panel_config.lbl_origen_d.configure(text_color="black")
            self.panel_config.lbl_destino_d.configure(text_color="black")
            self.panel_config.lbl_tabla_titulo.configure(text_color="#4B5563")
            self.panel_config.lbl_col_origen.configure(text_color="#1F2937")
            self.panel_config.lbl_col_destino.configure(text_color="#1F2937")
            self.panel_config.lbl_col_peso.configure(text_color="#1F2937")
            self.panel_config.btn_manual.configure(text_color="#374151", hover_color="#F3F4F6", border_color="#D1D5DB")
            
            for lbl in self.panel_config.filas_tabla:
                lbl.configure(text_color="#1F2937")
            
            self.panel_grafo.configure(fg_color="#FFFFFF")
            self.panel_grafo.set_modo_oscuro(False)
            self.switch_tema.configure(text_color="black")
            
        if self.grafo_actual is not None:
            self.panel_grafo.dibujar_grafo(self.grafo_actual)

    def _toggle_tema_app(self):
        modo_oscuro = self.switch_tema.get() == 1
        self.manejador_cambiar_tema(modo_oscuro)

    def manejador_generar_aleatorio(self, num_nodos):
        """Callback que se ejecuta cuando el panel de configuración pide un grafo."""
        self.grafo_actual = GeneradorAleatorio.generar_dag(num_nodos)
        self.panel_config.actualizar_tabla_aristas(self.grafo_actual)
        modo_oscuro = self.switch_tema.get() == 1
        self.manejador_cambiar_tema(modo_oscuro)
        self.panel_grafo.dibujar_grafo(self.grafo_actual)
        
    def manejador_iniciar_manual(self, num_nodos):
        """Prepara un grafo vacío con N nodos para edición manual."""
        self.grafo_actual = Grafo()
        for i in range(1, num_nodos + 1):
            self.grafo_actual.agregar_nodo(i, f"N{i}")
        # Redibujar grafo y tabla
        self.panel_config.actualizar_tabla_aristas(self.grafo_actual)
        modo_oscuro = self.switch_tema.get() == 1
        self.manejador_cambiar_tema(modo_oscuro)
        self.panel_grafo.dibujar_grafo(self.grafo_actual)
        
    def manejador_agregar_arista(self, origen, destino, peso):
        """Intenta agregar una arista. Lanza ValueError si hay ciclo o nodos inválidos."""
        if self.grafo_actual is None:
            raise ValueError("Primero inicie un grafo.")
            
        # 1. Validar que los nodos existan
        if origen not in self.grafo_actual.nodos or destino not in self.grafo_actual.nodos:
            raise ValueError(f"Ambos nodos deben estar entre 1 y {self.grafo_actual.cantidad_nodos()}")
            
        # 2. Agregar la arista temporalmente
        self.grafo_actual.agregar_arista(origen, destino, peso)
        
        # 3. Validar si esto creó un ciclo
        if ValidadorGrafo.tiene_ciclos(self.grafo_actual):
            # Rollback: Quitar la arista que acabamos de meter
            self.grafo_actual.adyacencia[origen].pop()
            raise ValueError("¡Operación denegada! Se detectó un ciclo.")
            
        # Si todo va bien, redibujamos
        self.panel_config.actualizar_tabla_aristas(self.grafo_actual)
        modo_oscuro = self.switch_tema.get() == 1
        self.manejador_cambiar_tema(modo_oscuro)
        self.panel_grafo.dibujar_grafo(self.grafo_actual)
        
    def manejador_ejecutar_dijkstra(self, origen, destino):
        """Ejecuta el algoritmo y actualiza la vista con los resultados."""
        if self.grafo_actual is None or self.grafo_actual.cantidad_nodos() == 0:
            raise ValueError("No hay grafo generado.")
            
        if origen not in self.grafo_actual.nodos or destino not in self.grafo_actual.nodos:
            raise ValueError("Vértice origen o destino no existen en el grafo.")
            
        motor_dijkstra = Dijkstra(self.grafo_actual)
        motor_dijkstra.ejecutar(origen)
        caminos = motor_dijkstra.obtener_caminos_minimos(destino)
        
        if not caminos:
            self.panel_grafo.dibujar_grafo(self.grafo_actual) # Redibujar limpio
            self.panel_grafo.mostrar_mensaje(f"El nodo {chr(64+destino)} es INALCANZABLE desde {chr(64+origen)}.", color="red")
            return f"Error: No hay conexión."
            
        # Distancia mínima oficial
        dist = motor_dijkstra.distancias[destino]
        
        # Redibujar pasando las rutas óptimas para que se resalten en rojo
        self.panel_grafo.dibujar_grafo(self.grafo_actual, caminos_minimos=caminos)
        
        # Formatear el resultado en texto para devolverlo a la UI
        letra_origen = chr(64 + origen)
        letra_destino = chr(64 + destino)
        texto = f"Camino mínimo calculado de {letra_origen} a {letra_destino}.\n"
        texto += f"Distancia Total: {dist} | Rutas óptimas: {len(caminos)}\n"
        for i, c in enumerate(caminos):
            ruta_letras = ' ➔ '.join([chr(64 + nodo) for nodo in c])
            texto += f"Ruta {i+1}: {ruta_letras}\n"
            
        self.panel_grafo.mostrar_mensaje(texto, color="#006600")
        return ""

    def manejador_iniciar_pasos(self, origen, destino):
        if self.grafo_actual is None or self.grafo_actual.cantidad_nodos() == 0:
            raise ValueError("No hay grafo generado.")
        if origen not in self.grafo_actual.nodos or destino not in self.grafo_actual.nodos:
            raise ValueError("Vértice origen o destino no existen.")
            
        self.destino_actual = destino
        self.motor_paso_a_paso = Dijkstra(self.grafo_actual)
        self.generador_pasos = self.motor_paso_a_paso.ejecutar_paso_a_paso(origen)
        self.panel_grafo.dibujar_grafo(self.grafo_actual) # Dibujar limpio antes de empezar
        self.panel_grafo.mostrar_mensaje(f"Iniciando algoritmo de Dijkstra desde el nodo {chr(64 + origen)}.", color="#0055AA")
        
    def manejador_siguiente_paso(self) -> tuple:
        """Avanza el generador un paso. Retorna (terminado, mensaje)."""
        if not self.generador_pasos: return True, ""
        
        try:
            estado = next(self.generador_pasos)
            
            nodo_act = estado["nodo_actual"]
            visitados = estado["visitados"]
            arista_eval = None
            
            letra_act = chr(64 + nodo_act) if nodo_act is not None else ""
            
            if estado["estado"] == "EVALUANDO":
                arista_eval = (nodo_act, estado["vecino"])
                letra_vec = chr(64 + estado["vecino"])
                mensaje = f"Evaluando arista: {letra_act} -> {letra_vec}."
                color_msj = "#D96600"
            elif estado["estado"] == "VISITADO":
                mensaje = f"Marcando nodo {letra_act} como visitado (distancia mínima definitiva)."
                color_msj = "#006600"
            elif estado["estado"] == "INICIO":
                mensaje = f"Iniciando en origen {letra_act}. Distancia = 0."
                color_msj = "#0055AA"
            elif estado["estado"] == "FIN":
                mensaje = f"Algoritmo finalizado. Construyendo caminos mínimos hacia el destino."
                color_msj = "#0055AA"
            else:
                mensaje = f"Seleccionando nodo no visitado con menor distancia temporal: {letra_act}."
                color_msj = "#0055AA"
                
            self.panel_grafo.mostrar_mensaje(mensaje, color=color_msj)
                
            self.panel_grafo.dibujar_grafo(
                self.grafo_actual, 
                nodo_actual=nodo_act, 
                nodos_visitados=visitados,
                arista_evaluada=arista_eval
            )
            
            if estado["estado"] == "FIN":
                # Dibujar ruta final si hay
                caminos = self.motor_paso_a_paso.obtener_caminos_minimos(self.destino_actual)
                if caminos:
                    self.panel_grafo.dibujar_grafo(self.grafo_actual, caminos_minimos=caminos)
                    self.panel_grafo.mostrar_mensaje("Ejecución completa. Camino mínimo resaltado en rojo.", color="#006600")
                else:
                    self.panel_grafo.mostrar_mensaje("Ejecución completa. Destino inalcanzable.", color="#CC0000")
                return True, ""
                
            return False, "" # Todavía quedan pasos
        except StopIteration:
            return True, ""

    def manejador_nodo_click(self, nodo_id):
        """Callback que se ejecuta al hacer clic derecho en un nodo del grafo."""
        letra = chr(64 + int(nodo_id))
        
        origen_actual = self.panel_config.ent_origen_d.get()
        destino_actual = self.panel_config.ent_destino_d.get()
        
        # Si ya hay un cálculo completo, reiniciar la selección
        if origen_actual and destino_actual:
            self.panel_config.ent_origen_d.delete(0, 'end')
            self.panel_config.ent_destino_d.delete(0, 'end')
            origen_actual = ""
            self.panel_grafo.dibujar_grafo(self.grafo_actual)
            
        # Si no hay origen, asignar origen
        if not origen_actual:
            self.panel_config.ent_origen_d.insert(0, letra)
            self.panel_grafo.mostrar_mensaje(f"Origen seleccionado: {letra}. Haz clic derecho en otro nodo para el Destino.", color="#0055AA")
        # Si ya hay origen, asignar destino y ejecutar algoritmo instantáneamente
        else:
            if origen_actual == letra:
                return # Ignorar si es el mismo nodo
                
            self.panel_config.ent_destino_d.insert(0, letra)
            self.panel_grafo.mostrar_mensaje(f"Calculando ruta rápida de {origen_actual} a {letra}...", color="#D96600")
            # Llamar directamente al botón de "Solución Inmediata"
            self.panel_config._ejecutar_dijkstra()
