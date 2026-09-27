import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class PanelGrafo(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.lbl_mensaje = ctk.CTkLabel(self, text="", font=("Arial", 14, "bold"))
        self.lbl_mensaje.pack(pady=5)
        
        self.canvas_widget = None
        # Desactivar modo interactivo por defecto de matplotlib
        plt.ioff()
        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        
        # Fondo oscuro neón
        self.fig.patch.set_facecolor('#1E1E24')
        self.ax.set_facecolor('#1E1E24')
        
        # Variables de estado para interactividad
        self.pos = None
        self.nodo_arrastrado = None
        self.on_nodo_click = None
        self.click_timer = None
        self.estado_dibujo = {}
        self.modo_oscuro = True # Por defecto iniciamos oscuro
        
        self.ultimo_mensaje = ""
        self.ultimo_color = "blue"
        
        # Integrarlo en CustomTkinter una sola vez
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Conectar eventos
        self.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)
        self.canvas.mpl_connect('button_release_event', self.on_release)
        
    def set_modo_oscuro(self, oscuro):
        self.modo_oscuro = oscuro
        if oscuro:
            self.fig.patch.set_facecolor('#1E1E24')
            self.ax.set_facecolor('#1E1E24')
        else:
            self.fig.patch.set_facecolor('#FFFFFF')
            self.ax.set_facecolor('#FFFFFF')
            
        if hasattr(self, 'canvas') and self.canvas:
            self.canvas.draw()
            
        self.mostrar_mensaje(self.ultimo_mensaje, self.ultimo_color)
        
    def on_press(self, event):
        if event.inaxes != self.ax or self.pos is None: return
        
        min_dist = float('inf')
        closest_node = None
        for nodo, (x, y) in self.pos.items():
            dist = (x - event.xdata)**2 + (y - event.ydata)**2
            if dist < min_dist:
                min_dist = dist
                closest_node = nodo
                
        umbral = 0.05 if len(self.pos) > 10 else 0.1
        
        if min_dist < umbral:
            if event.button == 1: # Clic izquierdo
                self.nodo_arrastrado = closest_node
            elif event.button == 3: # Clic derecho
                if self.on_nodo_click:
                    self.on_nodo_click(closest_node)
                    
    def on_motion(self, event):
        if self.nodo_arrastrado is not None and event.inaxes == self.ax:
            self.pos[self.nodo_arrastrado] = (event.xdata, event.ydata)
            # Redibujo rápido
            self.dibujar_grafo(**self.estado_dibujo, recalcular_pos=False)
            
    def on_release(self, event):
        if event.button == 1:
            self.nodo_arrastrado = None
        
    def mostrar_mensaje(self, texto, color="blue"):
        self.ultimo_mensaje = texto
        self.ultimo_color = color
        color_real = color
        if self.modo_oscuro:
            if color == "#006600": color_real = "#39FF14"
            elif color == "#CC0000" or color == "red": color_real = "#FF3333"
            elif color == "#0055AA": color_real = "#00E5FF"
            elif color == "#D96600": color_real = "#FF9900"
        self.lbl_mensaje.configure(text=texto, text_color=color_real)
        
    def dibujar_grafo(self, grafo, caminos_minimos=None, nodo_actual=None, nodos_visitados=None, arista_evaluada=None, recalcular_pos=True):
        # Guardar estado para redibujados rápidos al arrastrar
        self.estado_dibujo = {
            'grafo': grafo,
            'caminos_minimos': caminos_minimos,
            'nodo_actual': nodo_actual,
            'nodos_visitados': nodos_visitados,
            'arista_evaluada': arista_evaluada
        }
        
        self.ax.clear()
        self.ax.axis('off') # Quitar bordes para efecto moderno
        
        # Colores según el modo
        if self.modo_oscuro:
            bg_color = '#1E1E24'
            edge_color_default = '#4B5563'
            text_color_node = '#1E1E24'
            text_color_edge = '#E5E7EB'
        else:
            bg_color = '#FFFFFF'
            edge_color_default = '#9CA3AF'
            text_color_node = 'black'
            text_color_edge = '#1F2937'
            
        self.ax.set_facecolor(bg_color)
        self.fig.patch.set_facecolor(bg_color)
        
        if grafo is None:
            self.canvas.draw()
            return
        
        # Traducir nuestro modelo puro a un DiGraph de NetworkX SOLO para dibujo visual
        G_nx = nx.DiGraph()
        
        # Añadir nodos
        for nodo in grafo.obtener_todos_los_nodos():
            try:
                letra = chr(64 + int(nodo.id_nodo))
            except:
                letra = nodo.etiqueta
            G_nx.add_node(nodo.id_nodo, label=letra)
            
        # Añadir aristas
        for nodo in grafo.obtener_todos_los_nodos():
            for arista in grafo.obtener_sucesores(nodo.id_nodo):
                G_nx.add_edge(arista.origen.id_nodo, arista.destino.id_nodo, weight=arista.peso)
                
        # Mantener pos si recalcular_pos es False y ya existe
        if recalcular_pos or self.pos is None or set(self.pos.keys()) != set(G_nx.nodes()):
            self.pos = nx.circular_layout(G_nx)
        
        # Ajuste dinámico de tamaños según la cantidad de nodos
        num_nodos = G_nx.number_of_nodes()
        if num_nodos > 10:
            tam_nodo = 300
            f_size_nodo = 8
            f_size_arista = 7
            pos_etiqueta = 0.5
        else:
            tam_nodo = 1000
            f_size_nodo = 12
            f_size_arista = 10
            pos_etiqueta = 0.5
        
        # Añadir padding a los bordes para que los nodos no se corten
        self.ax.margins(0.15)
        
        # Identificar las aristas que pertenecen a los caminos mínimos (para resaltarlas)
        aristas_optimas = set()
        if caminos_minimos:
            for camino in caminos_minimos:
                for i in range(len(camino) - 1):
                    aristas_optimas.add((camino[i], camino[i+1]))
                    
        # Listas de colores por defecto
        edge_colors = []
        edge_widths = []
        
        # Obtener paleta de 20 colores para diferenciar nodos origen
        # Nota: plt.get_cmap() es la forma correcta y compatible con matplotlib >= 3.9
        cmap = plt.get_cmap('tab20')
        
        for u, v in G_nx.edges():
            # Si estamos en paso a paso y estamos evaluando esta arista específica
            if arista_evaluada and u == arista_evaluada[0] and v == arista_evaluada[1]:
                edge_colors.append('#FFFF00') # Amarillo Neón
                edge_widths.append(3.0)
            elif (u, v) in aristas_optimas:
                edge_colors.append('#FF007F') # Rosa Neón
                edge_widths.append(3.0)
            else:
                # Color apagado para resaltar el camino
                edge_colors.append(edge_color_default) 
                edge_widths.append(1.5)
                
        # Definir colores de nodos
        node_colors = []
        nodos_visitados = nodos_visitados or set()
        for nodo_id in G_nx.nodes():
            if nodo_actual and nodo_id == nodo_actual:
                node_colors.append('#FFFF00') # Amarillo Neón
            elif nodo_id in nodos_visitados:
                node_colors.append('#39FF14') # Verde Neón
            else:
                node_colors.append('#00E5FF') # Cian Neón por defecto
        
        # Dibujar nodos
        labels = nx.get_node_attributes(G_nx, 'label')
        nx.draw_networkx_nodes(G_nx, self.pos, ax=self.ax, node_color=node_colors, node_size=tam_nodo, edgecolors=bg_color, linewidths=1.5)
        nx.draw_networkx_labels(G_nx, self.pos, ax=self.ax, labels=labels, font_color=text_color_node, font_size=f_size_nodo, font_weight='bold')
        
        # Dibujar conexiones con los colores calculados
        nx.draw_networkx_edges(G_nx, self.pos, ax=self.ax, edge_color=edge_colors, 
                               width=edge_widths, arrows=True, arrowsize=15, 
                               node_size=tam_nodo)
                
        # Dibujar pesos de las aristas
        edge_labels = nx.get_edge_attributes(G_nx, 'weight')
        nx.draw_networkx_edge_labels(G_nx, self.pos, edge_labels=edge_labels, ax=self.ax, font_color=text_color_edge, font_size=f_size_arista, label_pos=pos_etiqueta, bbox=dict(facecolor=bg_color, edgecolor='none', alpha=0.7, pad=0.5))
        
        self.canvas.draw()
