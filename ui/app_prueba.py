import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class AplicacionPrueba(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Prueba de Entorno - Camino Mínimo")
        self.geometry("800x600")
        
        # Etiqueta de título
        self.label = ctk.CTkLabel(self, text="Integración CustomTkinter + Matplotlib + NetworkX", font=("Arial", 16, "bold"))
        self.label.pack(pady=10)
        
        # Botón para dibujar grafo
        self.btn_dibujar = ctk.CTkButton(self, text="Generar Grafo de Prueba", command=self.dibujar_grafo)
        self.btn_dibujar.pack(pady=10)
        
        # Frame para contener el gráfico
        self.frame_canvas = ctk.CTkFrame(self)
        self.frame_canvas.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.canvas = None

    def dibujar_grafo(self):
        # Limpiar canvas anterior si existe para evitar superposiciones
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            
        # Crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(6, 4))
        
        # Crear un grafo de prueba estático con NetworkX
        G = nx.DiGraph()
        G.add_weighted_edges_from([
            (1, 2, 5), 
            (1, 3, 2), 
            (2, 4, 1), 
            (3, 4, 7)
        ])
        
        # Definir posiciones de los nodos
        pos = nx.spring_layout(G, seed=42)
        
        # Dibujar nodos y aristas
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='skyblue', 
                node_size=800, font_weight='bold', arrows=True, arrowsize=15)
        
        # Dibujar etiquetas de pesos
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=ax)
        
        # Integrar figura de Matplotlib en el Frame de CustomTkinter
        self.canvas = FigureCanvasTkAgg(fig, master=self.frame_canvas)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    # Configuración de apariencia
    ctk.set_appearance_mode("System")  # Modos: "System" (estándar), "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Temas: "blue" (estándar), "green", "dark-blue"
    
    app = AplicacionPrueba()
    app.mainloop()
