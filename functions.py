import subprocess
from rich import print
from rich.console import Console
from rich.panel import Panel

def display_logo():
    console = Console()
    logo = """
     ███╗   ██╗███████╗ ██████╗ ██╗  ██╗██╗ ██████╗ ██████╗ 
     ████╗  ██║██╔════╝██╔═══██╗██║ ██╔╝██║██╔════╝██╔═══██╗
     ██╔██╗ ██║█████╗  ██║   ██║█████╔╝ ██║██║     ██║   ██║
     ██║╚██╗██║██╔══╝  ██║   ██║██╔═██╗ ██║██║     ██║   ██║
     ██║ ╚████║███████╗╚██████╔╝██║  ██╗██║╚██████╗╚██████╔╝
     ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═════╝ 
   
      📶  Neighbor.WiFi

      [bold cyan]Author: Alejandro Silgado[/bold cyan]
      [bold cyan]GitHub: [link=https://github.com/alejandroSilgado]alejandroSilgado[/link][/bold cyan]
    """
    console.print(Panel(logo, expand=False, border_style="bright_blue"))

def list_wireless_interfaces():
    """
    Lista las interfaces de red inalámbrica disponibles en el sistema.
    
    Returns:
        list: Una lista de interfaces de red inalámbrica.
    """
    try:
        # Ejecuta el comando iwconfig y captura la salida
        result = subprocess.run(['iwconfig'], capture_output=True, text=True, check=True)
        
        # Procesa la salida para encontrar las interfaces inalámbricas
        interfaces = []
        for line in result.stdout.split('\n'):
            if 'IEEE 802.11' in line:
                interface = line.split()[0]
                interfaces.append(interface)
        
        return interfaces

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar iwconfig: {e}")
        return []

def select_interface(interfaces):
    """
    Permite al usuario seleccionar una interfaz de red de una lista.
    
    Args:
        interfaces (list): Lista de interfaces de red inalámbrica.
    
    Returns:
        str: La interfaz seleccionada por el usuario.
    """
    print("Seleccione una interfaz de red inalámbrica:")
    for idx, iface in enumerate(interfaces):
        print(f"{idx + 1}. {iface}")
    
    while True:
        try:
            choice = int(input("Ingrese el número de la interfaz: ")) - 1
            if 0 <= choice < len(interfaces):
                return interfaces[choice]
            else:
                print("Selección no válida, intente de nuevo.")
        except ValueError:
            print("Entrada no válida, por favor ingrese un número.")


def enable_monitor_mode(interface):
    """
    Activa el modo monitor en la interfaz de red especificada.
    
    Args:
        interface (str): El nombre de la interfaz de red (e.g., 'wlan0').
    
    Returns:
        bool: True si se activa correctamente, False en caso contrario.
    """
    try:
        # Detenemos cualquier proceso que pueda interferir
        subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], check=True)
        
        # Iniciamos el modo monitor
        result = subprocess.run(['sudo', 'airmon-ng', 'start', interface], check=True, capture_output=True, text=True)
        
        # Verificamos la salida del comando para confirmar que se activó el modo monitor
        if 'monitor mode enabled' in result.stdout:
            print(f"Modo monitor activado en {interface}")
            return True
        else:
            print(f"Fallo al activar el modo monitor en {interface}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        return False


if __name__ == "__main__":
    interfaces = list_wireless_interfaces()
    if interfaces:
        selected_interface = select_interface(interfaces)
        print(f"Interfaz seleccionada: {selected_interface}")
        if enable_monitor_mode(selected_interface):
            print("Modo monitor activado correctamente.")
        else:
            print("No se pudo activar el modo monitor.")
    else:
        print("No se encontraron interfaces inalámbricas.")
