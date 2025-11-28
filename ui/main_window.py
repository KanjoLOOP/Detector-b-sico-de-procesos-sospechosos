import tkinter as tk
from tkinter import ttk, messagebox
from ui.styles import Colores, Fuentes
from ui.components import BotonModerno
from src.process_monitor import ProcessMonitor
from src.config_manager import ConfigManager

class MainWindow(tk.Tk):
    """
    La ventana principal de nuestra aplicación.
    Hereda de tk.Tk, que es la ventana base de Tkinter.
    """
    def __init__(self):
        super().__init__()
        
        self.title("Detector de Procesos Sospechosos")
        self.geometry("900x600")
        self.configure(bg=Colores.FONDO_OSCURO)
        
        # Inicializamos nuestros gestores
        self.config_manager = ConfigManager()
        self.process_monitor = ProcessMonitor()
        
        # Configuración de la interfaz
        self.setup_ui()
        
        # Iniciamos el ciclo de actualización automática
        self.actualizar_procesos()

    def setup_ui(self):
        # --- Encabezado ---
        header_frame = tk.Frame(self, bg=Colores.FONDO_OSCURO)
        header_frame.pack(fill="x", padx=20, pady=20)
        
        titulo = tk.Label(header_frame, text="Monitor de Procesos", font=Fuentes.TITULO, bg=Colores.FONDO_OSCURO, fg=Colores.TEXTO_BLANCO)
        titulo.pack(side="left")
        
        # Botones de acción en el encabezado
        btn_refresh = BotonModerno(header_frame, text="Actualizar", command=self.actualizar_procesos, width=100, height=35)
        btn_refresh.pack(side="right")

        # --- Área Principal (Pestañas) ---
        # Usamos un Notebook para crear pestañas
        style = ttk.Style()
        style.theme_use('clam') # Un tema más limpio
        
        # Configuración de colores para las pestañas
        style.configure("TNotebook", background=Colores.FONDO_OSCURO, borderwidth=0)
        style.configure("TNotebook.Tab", background=Colores.FONDO_OSCURO, foreground="white", padding=[10, 5], font=Fuentes.TEXTO)
        style.map("TNotebook.Tab", background=[("selected", Colores.ACCENTO_AZUL)], foreground=[("selected", Colores.TEXTO_NEGRO)])

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=(0, 20))
        
        # Pestaña 1: Monitor
        self.tab_monitor = tk.Frame(self.notebook, bg=Colores.FONDO_CLARO)
        self.notebook.add(self.tab_monitor, text="Monitor en Tiempo Real")
        self.setup_monitor_tab()
        
        # Pestaña 2: Gestión de Listas
        self.tab_listas = tk.Frame(self.notebook, bg=Colores.FONDO_CLARO)
        self.notebook.add(self.tab_listas, text="Gestión de Listas")
        self.setup_listas_tab()

    def setup_monitor_tab(self):
        # Lista de procesos (Treeview)
        columns = ("pid", "nombre", "usuario", "estado")
        self.tree = ttk.Treeview(self.tab_monitor, columns=columns, show="headings", selectmode="browse")
        
        # Definimos los encabezados
        self.tree.heading("pid", text="PID")
        self.tree.heading("nombre", text="Nombre del Proceso")
        self.tree.heading("usuario", text="Usuario")
        self.tree.heading("estado", text="Estado")
        
        # Ajustamos columnas
        self.tree.column("pid", width=80, anchor="center")
        self.tree.column("nombre", width=300)
        self.tree.column("usuario", width=150)
        self.tree.column("estado", width=100, anchor="center")
        
        # Barra de desplazamiento
        scrollbar = ttk.Scrollbar(self.tab_monitor, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Estilo del Treeview
        style = ttk.Style()
        style.configure("Treeview", font=Fuentes.TEXTO, rowheight=25)
        style.configure("Treeview.Heading", font=Fuentes.SUBTITULO)
        
        # Menú contextual (click derecho)
        self.menu_contextual = tk.Menu(self, tearoff=0)
        self.menu_contextual.add_command(label="Añadir a Lista Blanca (Seguro)", command=self.add_to_whitelist_action)
        self.menu_contextual.add_command(label="Añadir a Lista Negra (Peligroso)", command=self.add_to_blacklist_action)
        
        self.tree.bind("<Button-3>", self.mostrar_menu_contextual)

    def setup_listas_tab(self):
        # Panel izquierdo: Lista Blanca
        frame_white = tk.Frame(self.tab_listas, bg=Colores.FONDO_CLARO)
        frame_white.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        lbl_white = tk.Label(frame_white, text="Lista Blanca (Permitidos)", font=Fuentes.SUBTITULO, bg=Colores.FONDO_CLARO, fg=Colores.ACCENTO_VERDE)
        lbl_white.pack()
        
        self.listbox_white = tk.Listbox(frame_white, font=Fuentes.TEXTO)
        self.listbox_white.pack(fill="both", expand=True, pady=5)
        
        btn_del_white = BotonModerno(frame_white, text="Eliminar Seleccionado", command=lambda: self.borrar_de_lista("white"), width=150, height=30, color=Colores.ACCENTO_ROJO)
        btn_del_white.pack()

        # Panel derecho: Lista Negra
        frame_black = tk.Frame(self.tab_listas, bg=Colores.FONDO_CLARO)
        frame_black.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        lbl_black = tk.Label(frame_black, text="Lista Negra (Prohibidos)", font=Fuentes.SUBTITULO, bg=Colores.FONDO_CLARO, fg=Colores.ACCENTO_ROJO)
        lbl_black.pack()
        
        self.listbox_black = tk.Listbox(frame_black, font=Fuentes.TEXTO)
        self.listbox_black.pack(fill="both", expand=True, pady=5)
        
        btn_del_black = BotonModerno(frame_black, text="Eliminar Seleccionado", command=lambda: self.borrar_de_lista("black"), width=150, height=30, color=Colores.ACCENTO_ROJO)
        btn_del_black.pack()
        
        self.cargar_listas_visual()

    def actualizar_procesos(self):
        # Obtenemos los datos analizados
        data = self.process_monitor.analyze_processes(self.config_manager)
        
        # Limpiamos la tabla actual
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Insertamos los nuevos datos
        for proc in data:
            # Definimos etiquetas para colorear filas si es necesario (opcional)
            # Aquí solo insertamos los valores
            self.tree.insert("", "end", values=(proc['pid'], proc['name'], proc['user'], proc['status']))
            
            # Si detectamos algo prohibido, podríamos lanzar una alerta
            if proc['status'] == 'prohibido':
                # Ojo: esto podría ser molesto si sale muchas veces, mejor hacerlo discreto o solo una vez
                pass 

        # Programamos la próxima actualización en 5 segundos (5000 ms)
        self.after(5000, self.actualizar_procesos)

    def mostrar_menu_contextual(self, event):
        # Selecciona el item bajo el ratón
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu_contextual.post(event.x_root, event.y_root)

    def add_to_whitelist_action(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_data = self.tree.item(selected_item[0])
            process_name = item_data['values'][1] # El nombre es la segunda columna
            self.config_manager.add_to_whitelist(process_name)
            self.cargar_listas_visual()
            self.actualizar_procesos()
            messagebox.showinfo("Éxito", f"{process_name} añadido a la lista blanca.")

    def add_to_blacklist_action(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_data = self.tree.item(selected_item[0])
            process_name = item_data['values'][1]
            self.config_manager.add_to_blacklist(process_name)
            self.cargar_listas_visual()
            self.actualizar_procesos()
            messagebox.showwarning("Alerta", f"{process_name} añadido a la lista negra.")

    def cargar_listas_visual(self):
        # Actualiza las listbox de la pestaña de configuración
        self.listbox_white.delete(0, tk.END)
        for item in self.config_manager.whitelist:
            self.listbox_white.insert(tk.END, item)
            
        self.listbox_black.delete(0, tk.END)
        for item in self.config_manager.blacklist:
            self.listbox_black.insert(tk.END, item)

    def borrar_de_lista(self, tipo):
        if tipo == "white":
            seleccion = self.listbox_white.curselection()
            if seleccion:
                nombre = self.listbox_white.get(seleccion[0])
                self.config_manager.remove_from_whitelist(nombre)
        else:
            seleccion = self.listbox_black.curselection()
            if seleccion:
                nombre = self.listbox_black.get(seleccion[0])
                self.config_manager.remove_from_blacklist(nombre)
        
        self.cargar_listas_visual()
        self.actualizar_procesos()
