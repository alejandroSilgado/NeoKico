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
        # Ejecuta el comando netsh wlan show interfaces y captura la salida
        result = subprocess.run(['netsh', 'wlan', 'show', 'interfaces'], capture_output=True, text=True, check=True)
        
        # Procesa la salida para encontrar las interfaces inalámbricas
        interfaces = []
        for line in result.stdout.split('\n'):
            if 'SSID' in line:
                interface = line.split(':')[1].strip()
                interfaces.append(interface)
        
        return interfaces

    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar netsh: {e}")
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

# Nota: Activar el modo monitor en Windows no es compatible con todos los adaptadores y puede requerir software específico.

def enable_monitor_mode(interface):
    """
    Intenta activar el modo monitor en la interfaz de red especificada (Nota: funcionalidad limitada en Windows).
    
    Args:
        interface (str): El nombre de la interfaz de red (e.g., 'wlan0').
    
    Returns:
        bool: True si se activa correctamente, False en caso contrario.
    """
    print(f"Intentando activar el modo monitor en {interface} (Funcionalidad limitada en Windows)")
    return False

# Ejemplo de uso
if __name__ == "__main__":
    display_logo()  
    interfaces = list_wireless_interfaces()
    if interfaces:
        selected_interface = select_interface(interfaces)
        print(f"Interfaz seleccionada: {selected_interface}")
        if enable_monitor_mode(selected_interface):
            print("Modo monitor activado correctamente.")
        else:
            print("No se pudo activar el modo monitor (funcionalidad limitada en Windows).")
    else:
        print("No se encontraron interfaces inalámbricas.")
