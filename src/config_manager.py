import json
import os

# Clase para manejar la configuración y las listas de procesos
class ConfigManager:
    """
    Esta clase se encarga de guardar y cargar las listas de procesos permitidos (lista blanca)
    y procesos prohibidos (lista negra).
    Funciona guardando la información en archivos de texto con formato JSON, que es fácil de leer para las computadoras.
    """

    def __init__(self):
        # Definimos los nombres de los archivos donde guardaremos las listas
        self.whitelist_file = "whitelist.json"
        self.blacklist_file = "blacklist.json"
        
        # Cargamos las listas al iniciar la clase
        # Si los archivos no existen, se crearán listas vacías
        self.whitelist = self.load_list(self.whitelist_file)
        self.blacklist = self.load_list(self.blacklist_file)

    def load_list(self, filename):
        """
        Intenta cargar una lista desde un archivo JSON.
        Si el archivo no existe o hay un error, devuelve una lista vacía.
        """
        if not os.path.exists(filename):
            return [] # Si no hay archivo, devolvemos una lista vacía
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f) # Leemos el archivo y lo convertimos a lista de Python
        except Exception as e:
            print(f"Error al cargar {filename}: {e}")
            return []

    def save_list(self, filename, data_list):
        """
        Guarda una lista de Python en un archivo JSON.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_list, f, indent=4) # Guardamos la lista con formato bonito (indentación)
        except Exception as e:
            print(f"Error al guardar {filename}: {e}")

    def add_to_whitelist(self, process_name):
        """
        Añade un nombre de proceso a la lista blanca si no está ya.
        """
        if process_name not in self.whitelist:
            self.whitelist.append(process_name)
            self.save_list(self.whitelist_file, self.whitelist)
            # Si lo añadimos a la blanca, nos aseguramos de quitarlo de la negra si estaba ahí
            if process_name in self.blacklist:
                self.remove_from_blacklist(process_name)

    def add_to_blacklist(self, process_name):
        """
        Añade un nombre de proceso a la lista negra si no está ya.
        """
        if process_name not in self.blacklist:
            self.blacklist.append(process_name)
            self.save_list(self.blacklist_file, self.blacklist)
            # Si lo añadimos a la negra, nos aseguramos de quitarlo de la blanca si estaba ahí
            if process_name in self.whitelist:
                self.remove_from_whitelist(process_name)

    def remove_from_whitelist(self, process_name):
        """
        Elimina un proceso de la lista blanca.
        """
        if process_name in self.whitelist:
            self.whitelist.remove(process_name)
            self.save_list(self.whitelist_file, self.whitelist)

    def remove_from_blacklist(self, process_name):
        """
        Elimina un proceso de la lista negra.
        """
        if process_name in self.blacklist:
            self.blacklist.remove(process_name)
            self.save_list(self.blacklist_file, self.blacklist)

    def get_status(self, process_name):
        """
        Devuelve el estado de un proceso: 'permitido', 'prohibido' o 'desconocido'.
        """
        if process_name in self.whitelist:
            return "permitido"
        elif process_name in self.blacklist:
            return "prohibido"
        else:
            return "desconocido"
