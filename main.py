import tkinter as tk
from ui.main_window import MainWindow

# Punto de entrada de la aplicación
# Este archivo es el que ejecutamos para iniciar el programa.

def main():
    """
    Función principal que arranca la aplicación.
    """
    # Creamos la ventana principal
    app = MainWindow()
    
    # Iniciamos el bucle principal de la interfaz gráfica.
    # Esto mantiene la ventana abierta y escuchando eventos (clics, teclas, etc.)
    app.mainloop()

# Verificamos si este archivo se está ejecutando directamente
if __name__ == "__main__":
    main()
