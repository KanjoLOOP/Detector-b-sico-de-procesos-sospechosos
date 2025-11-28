import tkinter as tk
from ui.styles import Colores, Fuentes

class BotonModerno(tk.Canvas):
    """
    Un botón personalizado con bordes redondeados creado usando un Canvas.
    Tkinter por defecto tiene botones rectangulares, así que dibujamos uno nosotros.
    """
    def __init__(self, parent, text, command=None, width=120, height=40, color=Colores.BOTON_FONDO):
        super().__init__(parent, width=width, height=height, bg=Colores.FONDO_OSCURO, highlightthickness=0)
        self.command = command
        self.color_normal = color
        self.color_hover = Colores.BOTON_HOVER
        self.text = text
        
        # Dibujamos el fondo redondeado y el texto
        # Usamos un polígono o varios óvalos/rectángulos para simular redondez.
        # Una forma sencilla es crear un rectángulo con esquinas redondeadas (disponible en versiones nuevas de tk)
        # O simplemente dibujar un óvalo a cada lado y un rect en medio.
        
        # Para simplificar y asegurar compatibilidad, usaremos un diseño "plano" pero con esquinas visualmente suaves
        # Dibujamos un rectángulo redondeado (round_rectangle)
        self.rect = self.round_rectangle(2, 2, width-2, height-2, radius=20, fill=self.color_normal, outline="")
        
        self.text_item = self.create_text(width/2, height/2, text=self.text, fill=Colores.TEXTO_BLANCO, font=Fuentes.TEXTO)
        
        # Eventos del ratón (binds)
        self.bind("<Button-1>", self.on_click)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        """Función auxiliar para dibujar un rectángulo con esquinas redondeadas"""
        points = [x1+radius, y1,
                  x1+radius, y1,
                  x2-radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, **kwargs, smooth=True)

    def on_click(self, event):
        if self.command:
            self.command()

    def on_enter(self, event):
        self.itemconfig(self.rect, fill=self.color_hover)

    def on_leave(self, event):
        self.itemconfig(self.rect, fill=self.color_normal)

class TarjetaProceso(tk.Frame):
    """
    Un widget para mostrar la información de un proceso de forma bonita.
    """
    def __init__(self, parent, process_data):
        super().__init__(parent, bg=Colores.FONDO_CLARO, pady=5, padx=5)
        
        # Determinamos el color según el estado
        estado = process_data['status']
        color_estado = Colores.ACCENTO_AMARILLO # Por defecto
        if estado == 'permitido':
            color_estado = Colores.ACCENTO_VERDE
        elif estado == 'prohibido':
            color_estado = Colores.ACCENTO_ROJO
            
        # Etiqueta de color (indicador)
        self.indicador = tk.Label(self, bg=color_estado, width=2)
        self.indicador.pack(side="left", fill="y", padx=(0, 10))
        
        # Nombre del proceso
        self.lbl_nombre = tk.Label(self, text=process_data['name'], bg=Colores.FONDO_CLARO, font=Fuentes.TEXTO, fg=Colores.TEXTO_NEGRO)
        self.lbl_nombre.pack(side="left")
        
        # ID del proceso
        self.lbl_pid = tk.Label(self, text=f"PID: {process_data['pid']}", bg=Colores.FONDO_CLARO, font=Fuentes.TEXTO_PEQUENO, fg="gray")
        self.lbl_pid.pack(side="left", padx=10)

        # Estado texto
        self.lbl_estado = tk.Label(self, text=estado.upper(), bg=Colores.FONDO_CLARO, font=Fuentes.TEXTO_PEQUENO, fg=color_estado)
        self.lbl_estado.pack(side="right", padx=10)
