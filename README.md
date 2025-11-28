# Detector Básico de Procesos Sospechosos

Este proyecto es una herramienta educativa desarrollada en Python para monitorear los procesos que se ejecutan en tu sistema operativo Windows. Permite clasificar procesos como "seguros" (lista blanca) o "peligrosos" (lista negra) y visualizar su estado en tiempo real.

## 🎯 Objetivo del Proyecto

El objetivo principal es aprender cómo funcionan los procesos en un sistema operativo y cómo podemos interactuar con ellos usando Python. Además, busca enseñar buenas prácticas de programación, estructura de proyectos y creación de interfaces gráficas modernas con Tkinter.

## ⚙️ Cómo Funciona

La aplicación utiliza la librería `psutil` para "espiar" lo que hace el sistema. Periódicamente (cada 5 segundos), consulta la lista de todos los programas abiertos y verifica si están en nuestras listas de control:

1.  **Lista Blanca (Whitelist):** Procesos que conocemos y confiamos (ej. `chrome.exe`, `explorer.exe`). Se muestran en verde.
2.  **Lista Negra (Blacklist):** Procesos que no queremos que se ejecuten o que consideramos sospechosos. Se muestran en rojo.
3.  **Desconocidos:** Procesos que no están en ninguna lista. Se muestran en amarillo.

## 🛠️ Dependencias Necesarias

Para ejecutar este proyecto necesitas tener instalado Python. Las librerías externas necesarias son:

*   `psutil`: Para obtener información del sistema y los procesos.
*   `Pillow` (opcional, si se usan imágenes): Para manejo de imágenes en la interfaz.

Puedes instalarlas ejecutando:

```bash
pip install -r requirements.txt
```

## 🚀 Instrucciones de Ejecución

1.  Asegúrate de tener Python instalado.
2.  Abre una terminal en la carpeta del proyecto.
3.  Instala las dependencias (ver arriba).
4.  Ejecuta el archivo principal:

```bash
python main.py
```

## 📂 Estructura de Archivos

El proyecto está organizado de forma limpia para facilitar su mantenimiento:

*   `main.py`: El punto de partida. Ejecuta este archivo para iniciar la app.
*   `requirements.txt`: Lista de librerías necesarias.
*   `src/`: Carpeta con la lógica del programa (el "cerebro").
    *   `process_monitor.py`: Se encarga de hablar con el sistema operativo.
    *   `config_manager.py`: Guarda y carga tus listas blanca y negra.
*   `ui/`: Carpeta con la interfaz gráfica (lo que ves).
    *   `main_window.py`: La ventana principal y sus pestañas.
    *   `components.py`: Piezas de la interfaz, como los botones personalizados.
    *   `styles.py`: Archivo de configuración de colores y fuentes.

## 📝 Explicación Técnica Sencilla

Imagina que la aplicación es un guardia de seguridad en la entrada de un edificio (tu ordenador).
*   **`src/process_monitor.py`** es el guardia que tiene una lista de todos los que entran.
*   **`src/config_manager.py`** es el libro donde el guardia anota quién tiene pase VIP (lista blanca) y quién tiene prohibida la entrada (lista negra).
*   **`ui/main_window.py`** es la pantalla de cámaras de seguridad donde tú, el jefe, ves todo lo que pasa.

## 📸 Interfaz

La interfaz ha sido diseñada para ser limpia y moderna, utilizando colores suaves y oscuros para no cansar la vista. Cuenta con dos pestañas principales:
1.  **Monitor en Tiempo Real:** Donde ves la lista de procesos. Puedes hacer clic derecho en cualquiera para clasificarlo.
2.  **Gestión de Listas:** Donde puedes ver y borrar los procesos que has guardado en tus listas.

---
*Proyecto desarrollado con fines educativos.*
