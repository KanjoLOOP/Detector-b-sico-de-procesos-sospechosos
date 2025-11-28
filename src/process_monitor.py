import psutil
import time

# Clase para vigilar los procesos del sistema
class ProcessMonitor:
    """
    Esta clase es como un vigilante. Usa la librería 'psutil' para mirar
    qué programas (procesos) se están ejecutando en tu ordenador.
    """

    def __init__(self):
        # Aquí podríamos guardar configuraciones si hiciera falta
        pass

    def get_running_processes(self):
        """
        Obtiene una lista de todos los procesos que se están ejecutando ahora mismo.
        Devuelve una lista de diccionarios (como fichas) con información de cada proceso.
        """
        processes = []
        
        # psutil.process_iter() nos deja recorrer todos los procesos activos
        # Le pedimos que nos de el ID (pid), el nombre (name) y el usuario (username)
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                # Convertimos la información del proceso a un diccionario simple
                proc_info = proc.info
                processes.append(proc_info)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                # A veces un proceso se cierra justo cuando lo estamos mirando, o no tenemos permiso.
                # Si pasa eso, simplemente lo ignoramos y seguimos con el siguiente.
                pass
        
        return processes

    def analyze_processes(self, config_manager):
        """
        Obtiene los procesos y los clasifica según las listas blanca y negra
        que gestiona el config_manager.
        """
        # Obtenemos la lista actual de procesos
        running_processes = self.get_running_processes()
        
        analyzed_data = []

        for proc in running_processes:
            name = proc['name']
            pid = proc['pid']
            user = proc['username']
            
            # Preguntamos al config_manager qué sabe de este proceso
            status = config_manager.get_status(name)
            
            # Creamos una ficha con toda la info para enviarla a la interfaz
            process_data = {
                'pid': pid,
                'name': name,
                'user': user,
                'status': status # 'permitido', 'prohibido' o 'desconocido'
            }
            analyzed_data.append(process_data)
            
        return analyzed_data
