import customtkinter as ctk
from ui.app import App

if __name__ == "__main__":
    # Ajustes estéticos globales para un diseño profesional (Modo Claro)
    ctk.set_appearance_mode("Light")  
    ctk.set_default_color_theme("blue")  
    
    # Instanciar y correr el bucle de la aplicación
    aplicacion = App()
    aplicacion.mainloop()