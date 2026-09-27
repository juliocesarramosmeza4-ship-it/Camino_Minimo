import customtkinter as ctk
from PIL import Image
import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta al recurso, compatible con PyInstaller (_MEIPASS) y desarrollo local"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class VentanaInicio(ctk.CTkFrame):
    def __init__(self, master, on_comenzar):
        super().__init__(master, fg_color="#111827")
        
        self.on_comenzar = on_comenzar
        
        # Frame central para contener todo
        self.frame_centro = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_centro.place(relx=0.5, rely=0.5, anchor="center")
        
        # Contenedor dividido: Izquierda (Imagen) y Derecha (Formulario)
        self.frame_izquierdo = ctk.CTkFrame(self.frame_centro, fg_color="transparent")
        self.frame_izquierdo.pack(side="left", padx=(0, 40))
        
        self.frame_derecho = ctk.CTkFrame(self.frame_centro, fg_color="transparent")
        self.frame_derecho.pack(side="right", padx=(40, 0))
        
        # --- LADO IZQUIERDO: Imagen Gigante ---
        self.frame_imagen = ctk.CTkFrame(self.frame_izquierdo, width=800, height=600, fg_color="transparent")
        self.frame_imagen.pack()
        self.frame_imagen.pack_propagate(False) # Mantener tamaño fijo
        
        try:
            ruta_portada = resource_path("portada.png")
            img = ctk.CTkImage(light_image=Image.open(ruta_portada), 
                               dark_image=Image.open(ruta_portada), 
                               size=(800, 600))
            self.lbl_imagen = ctk.CTkLabel(self.frame_imagen, text="", image=img)
        except Exception:
            self.lbl_imagen = ctk.CTkLabel(self.frame_imagen, text="[ Imagen de Portada Aquí ]\n(Guarda tu imagen como portada.png)", font=("Inter", 14), text_color="#9CA3AF")
            
        self.lbl_imagen.place(relx=0.5, rely=0.5, anchor="center")
        
        # --- LADO DERECHO: Título y Controles ---
        self.lbl_titulo = ctk.CTkLabel(self.frame_derecho, text="Dijkstra Visualizer Pro", font=("Outfit", 42, "bold"), text_color="white")
        self.lbl_titulo.pack(pady=(0, 40))
        
        # Frame de configuración inicial
        self.frame_config = ctk.CTkFrame(self.frame_derecho, fg_color="#1F2937", corner_radius=15, border_width=1, border_color="#374151")
        self.frame_config.pack(pady=10, fill="x")
        
        self.lbl_pregunta = ctk.CTkLabel(self.frame_config, text="¿Con cuántos nodos deseas empezar?", font=("Inter", 18), text_color="#E5E7EB")
        self.lbl_pregunta.pack(pady=(25, 10))
        
        self.entrada_nodos = ctk.CTkEntry(self.frame_config, width=180, height=40, justify="center", font=("Inter", 20, "bold"), fg_color="#374151", text_color="white", border_color="#4B5563")
        self.entrada_nodos.insert(0, "7")
        self.entrada_nodos.pack(pady=15)
        
        self.lbl_error = ctk.CTkLabel(self.frame_config, text="", text_color="#EF4444", font=("Inter", 12))
        self.lbl_error.pack(pady=(0, 10))
        
        # Botón comenzar
        self.btn_comenzar = ctk.CTkButton(self.frame_derecho, text="COMENZAR", font=("Inter", 20, "bold"), 
                                          fg_color="#00E5FF", hover_color="#00B8D4", text_color="black", 
                                          corner_radius=10, width=250, height=50, command=self._validar_y_comenzar)
        self.btn_comenzar.pack(pady=40)
        
    def _validar_y_comenzar(self):
        try:
            n = int(self.entrada_nodos.get())
            if 7 <= n <= 16:
                self.destroy() # Destruye este frame
                self.on_comenzar(n) # Llama al callback para mostrar la app
            else:
                self.lbl_error.configure(text="Elige entre 7 y 16 nodos.")
        except ValueError:
            self.lbl_error.configure(text="Ingresa un número válido.")
