import customtkinter as ctk

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tw = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = ctk.CTkToplevel(self.widget, fg_color="#1F2937")
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = ctk.CTkLabel(self.tw, text=self.text, fg_color="#1F2937", text_color="white", corner_radius=0, padx=8, pady=4)
        label.pack()

    def leave(self, event=None):
        if self.tw:
            self.tw.destroy()
            self.tw = None

class PanelConfiguracion(ctk.CTkFrame):
    def __init__(self, master, on_generar_aleatorio, on_cambiar_tema=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.on_cambiar_tema = on_cambiar_tema
        
        # Header (Título)
        self.frame_header = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_header.pack(fill="x", padx=10, pady=(20, 10))
        
        self.lbl_titulo = ctk.CTkLabel(self.frame_header, text="Configuración del Grafo", font=("Outfit", 20, "bold"), text_color="#1F2937")
        self.lbl_titulo.pack(side="left")
        
        # Frame: Inicialización del Grafo
        self.frame_init = ctk.CTkFrame(self, fg_color="#F9FAFB", corner_radius=10, border_width=1, border_color="#E5E7EB")
        self.frame_init.pack(fill="x", padx=15, pady=5)
        
        self.lbl_nodos = ctk.CTkLabel(self.frame_init, text="Cantidad de nodos (7-16):", font=("Inter", 12))
        self.lbl_nodos.pack(pady=(10, 0))
        
        f_entry = ctk.CTkFrame(self.frame_init, fg_color="transparent")
        f_entry.pack(pady=5)
        
        self.entrada_nodos = ctk.CTkEntry(f_entry, width=150, border_color="#D1D5DB", corner_radius=6)
        self.entrada_nodos.insert(0, "7")
        self.entrada_nodos.pack(side="left")
        
        lbl_info_nodos = ctk.CTkLabel(f_entry, text="?", width=20, height=20, corner_radius=10, fg_color="#3B82F6", text_color="white", font=("Inter", 12, "bold"), cursor="hand2")
        lbl_info_nodos.pack(side="left", padx=5)
        ToolTip(lbl_info_nodos, "Acepta números enteros del 7 al 16.\nDetermina el tamaño del grafo a generar.")
        
        self.btn_aleatorio = ctk.CTkButton(self.frame_init, text="Generación Aleatoria", command=self._generar, 
                                           fg_color="#00E5FF", hover_color="#00B8D4", text_color="black", font=("Inter", 12, "bold"), corner_radius=8)
        self.btn_aleatorio.pack(pady=8)
        
        self.btn_manual = ctk.CTkButton(self.frame_init, text="Iniciar Modo Manual", command=self._iniciar_manual, 
                                        fg_color="transparent", border_width=2, border_color="#D1D5DB", hover_color="#F3F4F6", text_color="#374151", corner_radius=8)
        self.btn_manual.pack(pady=(0, 10))
        
        # Mensaje de error / estado general
        self.lbl_estado = ctk.CTkLabel(self, text="", text_color="#EF4444", font=("Inter", 12))
        self.lbl_estado.pack(pady=2)
        
        # Frame: Edición Manual (Oculto inicialmente)
        self.frame_manual = ctk.CTkFrame(self, fg_color="#F9FAFB", corner_radius=10, border_width=1, border_color="#E5E7EB")
        
        self.lbl_manual = ctk.CTkLabel(self.frame_manual, text="Agregar Arista", font=("Outfit", 14, "bold"), text_color="#1F2937")
        self.lbl_manual.grid(row=0, column=0, columnspan=3, pady=10)
        
        self.lbl_origen = ctk.CTkLabel(self.frame_manual, text="Origen:")
        self.lbl_origen.grid(row=1, column=0, padx=10, pady=2, sticky="e")
        self.ent_origen = ctk.CTkEntry(self.frame_manual, width=80, border_color="#D1D5DB")
        self.ent_origen.grid(row=1, column=1, padx=10, pady=2)
        lbl_info_orig = ctk.CTkLabel(self.frame_manual, text="?", width=20, height=20, corner_radius=10, fg_color="#3B82F6", text_color="white", font=("Inter", 12, "bold"), cursor="hand2")
        lbl_info_orig.grid(row=1, column=2, padx=5)
        ToolTip(lbl_info_orig, "Acepta números (ej. 1) o letras (ej. A).\nEs el nodo donde inicia el camino.")
        
        self.lbl_destino = ctk.CTkLabel(self.frame_manual, text="Destino:")
        self.lbl_destino.grid(row=2, column=0, padx=10, pady=2, sticky="e")
        self.ent_destino = ctk.CTkEntry(self.frame_manual, width=80, border_color="#D1D5DB")
        self.ent_destino.grid(row=2, column=1, padx=10, pady=2)
        lbl_info_dest = ctk.CTkLabel(self.frame_manual, text="?", width=20, height=20, corner_radius=10, fg_color="#3B82F6", text_color="white", font=("Inter", 12, "bold"), cursor="hand2")
        lbl_info_dest.grid(row=2, column=2, padx=5)
        ToolTip(lbl_info_dest, "Acepta números (ej. 1) o letras (ej. A).\nEs el nodo donde termina el camino.")
        
        self.lbl_peso = ctk.CTkLabel(self.frame_manual, text="Distancia:")
        self.lbl_peso.grid(row=3, column=0, padx=10, pady=2, sticky="e")
        self.ent_peso = ctk.CTkEntry(self.frame_manual, width=80, border_color="#D1D5DB")
        self.ent_peso.grid(row=3, column=1, padx=10, pady=2)
        lbl_info_peso = ctk.CTkLabel(self.frame_manual, text="?", width=20, height=20, corner_radius=10, fg_color="#3B82F6", text_color="white", font=("Inter", 12, "bold"), cursor="hand2")
        lbl_info_peso.grid(row=3, column=2, padx=5)
        ToolTip(lbl_info_peso, "Acepta números con o sin decimales.\nRepresenta el costo o distancia del camino.")
        
        self.btn_agregar = ctk.CTkButton(self.frame_manual, text="Añadir", command=self._agregar_arista_manual,
                                         fg_color="#39FF14", hover_color="#32E612", text_color="black", font=("Inter", 12, "bold"), corner_radius=8)
        self.btn_agregar.grid(row=4, column=0, columnspan=3, pady=(10, 15))

        # Frame: Ejecución de Dijkstra
        self.frame_dijkstra = ctk.CTkFrame(self, fg_color="#F9FAFB", corner_radius=10, border_width=1, border_color="#E5E7EB")
        self.frame_dijkstra.pack(fill="x", padx=15, pady=5)
        
        self.lbl_dijkstra = ctk.CTkLabel(self.frame_dijkstra, text="Algoritmo de Dijkstra", font=("Outfit", 14, "bold"), text_color="#1F2937")
        self.lbl_dijkstra.grid(row=0, column=0, columnspan=3, pady=10)
        
        self.lbl_origen_d = ctk.CTkLabel(self.frame_dijkstra, text="Origen:")
        self.lbl_origen_d.grid(row=1, column=0, padx=10, pady=2, sticky="e")
        self.ent_origen_d = ctk.CTkEntry(self.frame_dijkstra, width=80, border_color="#D1D5DB")
        self.ent_origen_d.grid(row=1, column=1, padx=10, pady=2)
        lbl_info_orig_d = ctk.CTkLabel(self.frame_dijkstra, text="?", width=20, height=20, corner_radius=10, fg_color="#3B82F6", text_color="white", font=("Inter", 12, "bold"), cursor="hand2")
        lbl_info_orig_d.grid(row=1, column=2, padx=5)
        ToolTip(lbl_info_orig_d, "Acepta números o letras.\nNodo inicial para buscar el camino más corto.")
        
        self.lbl_destino_d = ctk.CTkLabel(self.frame_dijkstra, text="Destino:")
        self.lbl_destino_d.grid(row=2, column=0, padx=10, pady=2, sticky="e")
        self.ent_destino_d = ctk.CTkEntry(self.frame_dijkstra, width=80, border_color="#D1D5DB")
        self.ent_destino_d.grid(row=2, column=1, padx=10, pady=2)
        lbl_info_dest_d = ctk.CTkLabel(self.frame_dijkstra, text="?", width=20, height=20, corner_radius=10, fg_color="#3B82F6", text_color="white", font=("Inter", 12, "bold"), cursor="hand2")
        lbl_info_dest_d.grid(row=2, column=2, padx=5)
        ToolTip(lbl_info_dest_d, "Acepta números o letras.\nNodo final a donde queremos llegar.")
        
        self.btn_resolver = ctk.CTkButton(self.frame_dijkstra, text="¡Solución Inmediata!", command=self._ejecutar_dijkstra, 
                                          fg_color="#FF007F", hover_color="#E60073", font=("Inter", 12, "bold"), corner_radius=8)
        self.btn_resolver.grid(row=3, column=0, columnspan=3, pady=(10, 5))
        
        self.btn_iniciar_paso = ctk.CTkButton(self.frame_dijkstra, text="Iniciar Paso a Paso", command=self._iniciar_paso_a_paso, 
                                              fg_color="#F59E0B", hover_color="#D97706", font=("Inter", 12, "bold"), corner_radius=8)
        self.btn_iniciar_paso.grid(row=4, column=0, columnspan=3, pady=5)
        
        self.btn_siguiente = ctk.CTkButton(self.frame_dijkstra, text="Siguiente >>", command=self._siguiente_paso, state="disabled", corner_radius=8)
        self.btn_siguiente.grid(row=5, column=0, columnspan=3, pady=(5, 15))
        
        # Frame: Tabla de Aristas
        self.frame_tabla = ctk.CTkScrollableFrame(self, height=150, fg_color="#F9FAFB", corner_radius=10, border_width=1, border_color="#E5E7EB")
        self.frame_tabla.pack(fill="both", expand=True, padx=15, pady=10)
        
        self.lbl_tabla_titulo = ctk.CTkLabel(self.frame_tabla, text="Detalle de Rutas", font=("Outfit", 12, "bold"), text_color="#4B5563")
        self.lbl_tabla_titulo.grid(row=0, column=0, columnspan=3, pady=(5, 10))
        
        self.lbl_col_origen = ctk.CTkLabel(self.frame_tabla, text="Origen", font=("Inter", 11, "bold"), text_color="#1F2937")
        self.lbl_col_origen.grid(row=1, column=0, padx=15)
        self.lbl_col_destino = ctk.CTkLabel(self.frame_tabla, text="Destino", font=("Inter", 11, "bold"), text_color="#1F2937")
        self.lbl_col_destino.grid(row=1, column=1, padx=15)
        self.lbl_col_peso = ctk.CTkLabel(self.frame_tabla, text="Distancia", font=("Inter", 11, "bold"), text_color="#1F2937")
        self.lbl_col_peso.grid(row=1, column=2, padx=15)
        
        self.filas_tabla = []
        
        # Callbacks y Estado
        self.on_generar_aleatorio = on_generar_aleatorio
        self.on_iniciar_manual = None
        self.on_agregar_arista = None
        self.on_ejecutar_dijkstra = None
        self.on_iniciar_pasos = None
        self.on_siguiente_paso = None

    def _toggle_tema(self):
        if self.on_cambiar_tema:
            self.on_cambiar_tema()

    def parse_nodo(self, valor):
        valor = str(valor).strip().upper()
        if valor.isalpha() and len(valor) == 1:
            return ord(valor) - 64
        return int(valor)

    def actualizar_tabla_aristas(self, grafo):
        # Limpiar filas anteriores
        for widget in self.filas_tabla:
            widget.destroy()
        self.filas_tabla.clear()
        
        row_idx = 2
        for nodo in grafo.obtener_todos_los_nodos():
            for arista in grafo.obtener_sucesores(nodo.id_nodo):
                o_letra = chr(64 + int(arista.origen.id_nodo))
                d_letra = chr(64 + int(arista.destino.id_nodo))
                
                lbl_o = ctk.CTkLabel(self.frame_tabla, text=o_letra)
                lbl_o.grid(row=row_idx, column=0, padx=10, pady=2)
                lbl_d = ctk.CTkLabel(self.frame_tabla, text=d_letra)
                lbl_d.grid(row=row_idx, column=1, padx=10, pady=2)
                lbl_p = ctk.CTkLabel(self.frame_tabla, text=str(arista.peso))
                lbl_p.grid(row=row_idx, column=2, padx=10, pady=2)
                
                self.filas_tabla.extend([lbl_o, lbl_d, lbl_p])
                row_idx += 1

    def _generar(self):
        self.lbl_estado.configure(text="", text_color="green")
        try:
            n = int(self.entrada_nodos.get())
            if 7 <= n <= 16:
                self.frame_manual.pack_forget() # Ocultar manual si generamos aleatorio
                self.on_generar_aleatorio(n)
            else:
                self.lbl_estado.configure(text="Error: Rango debe ser 7-16", text_color="red")
        except ValueError:
            self.lbl_estado.configure(text="Error: Ingrese un número válido", text_color="red")
            
    def _iniciar_manual(self):
        self.lbl_estado.configure(text="", text_color="green")
        try:
            n = int(self.entrada_nodos.get())
            if 7 <= n <= 16:
                self.frame_manual.pack(fill="x", padx=15, pady=5)
                if self.on_iniciar_manual:
                    self.on_iniciar_manual(n)
                self.lbl_estado.configure(text=f"Modo manual iniciado ({n} nodos)", text_color="green")
            else:
                self.lbl_estado.configure(text="Error: Rango debe ser 7-16", text_color="red")
        except ValueError:
            self.lbl_estado.configure(text="Error: Ingrese un número válido", text_color="red")
            
    def _agregar_arista_manual(self):
        self.lbl_estado.configure(text="", text_color="red")
        try:
            origen = self.parse_nodo(self.ent_origen.get())
            destino = self.parse_nodo(self.ent_destino.get())
            peso = float(self.ent_peso.get())
            
            if self.on_agregar_arista:
                # El callback nos devolverá un bool o levantará una excepción
                try:
                    self.on_agregar_arista(origen, destino, peso)
                    self.lbl_estado.configure(text="Arista agregada.", text_color="green")
                    self.ent_origen.delete(0, 'end')
                    self.ent_destino.delete(0, 'end')
                    self.ent_peso.delete(0, 'end')
                except ValueError as e:
                    self.lbl_estado.configure(text=str(e), text_color="red")
        except ValueError:
            self.lbl_estado.configure(text="Error: Nodos enteros, Peso número", text_color="red")
            
    def _ejecutar_dijkstra(self):
        self.lbl_estado.configure(text="", text_color="black")
        try:
            origen = self.parse_nodo(self.ent_origen_d.get())
            destino = self.parse_nodo(self.ent_destino_d.get())
            
            if self.on_ejecutar_dijkstra:
                try:
                    res = self.on_ejecutar_dijkstra(origen, destino)
                    # El panel superior maneja el texto
                except ValueError as e:
                    self.lbl_estado.configure(text=str(e), text_color="#CC0000")
        except ValueError:
            self.lbl_estado.configure(text="Error: Use números (1-16) o letras (A-P)", text_color="#CC0000")
            
    def _iniciar_paso_a_paso(self):
        self.lbl_estado.configure(text="", text_color="black")
        try:
            origen = self.parse_nodo(self.ent_origen_d.get())
            destino = self.parse_nodo(self.ent_destino_d.get())
            if self.on_iniciar_pasos:
                try:
                    self.on_iniciar_pasos(origen, destino)
                    self.btn_siguiente.configure(state="normal")
                    origen_letra = chr(64 + origen)
                    self.lbl_estado.configure(text=f"Modo paso a paso iniciado.", text_color="#006600")
                except ValueError as e:
                    self.lbl_estado.configure(text=str(e), text_color="#CC0000")
        except ValueError:
            self.lbl_estado.configure(text="Error: Use números (1-16) o letras (A-P)", text_color="#CC0000")
            
    def _siguiente_paso(self):
        if self.on_siguiente_paso:
            terminado, mensaje = self.on_siguiente_paso()
            self.lbl_estado.configure(text=mensaje, text_color="blue")
            if terminado:
                self.btn_siguiente.configure(state="disabled")
                self.lbl_estado.configure(text_color="green")
