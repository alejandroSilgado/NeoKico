import subprocess
from rich import print
from rich.console import Console
from rich.panel import Panel
import time as time_module
import curses


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
    try:
        result = subprocess.run(['iwconfig'], capture_output=True, text=True, check=True)
        interfaces = []
        for line in result.stdout.split('\n'):
            if 'IEEE 802.11' in line:
                interface = line.split()[0]
                interfaces.append(interface)
        return interfaces
    except subprocess.CalledProcessError as e:
        print(f"Error executing iwconfig: {e}")
        return []
def select_interface(interfaces):
    print("Select a wireless interface:")
    for idx, iface in enumerate(interfaces):
        print(f"{idx + 1}. {iface}")

    while True:
        try:
            choice = int(input("Enter the interface number: ")) - 1
            if 0 <= choice < len(interfaces):
                return interfaces[choice]
            else:
                print("Invalid selection, please try again.")
        except ValueError:
            print("Invalid input, please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting program...")
            exit()

def enable_monitor_mode(interface):
    try:
        # Check if the interface is already in monitor mode
        result = subprocess.run(['iwconfig', interface], capture_output=True, text=True, check=True)
        if 'Mode:Monitor' in result.stdout:
            print(f"Interface {interface} is already in monitor mode.")
            return True

        # Kill any processes that might interfere
        kill_result = subprocess.run(['sudo', 'airmon-ng', 'check', 'kill'], check=True, capture_output=True, text=True)
        print("Killing these processes:")
        print(kill_result.stdout)

        # Enable monitor mode
        result = subprocess.run(['sudo', 'airmon-ng', 'start', interface], check=True, capture_output=True, text=True)
        print("airmon-ng start output:")
        print(result.stdout)

        # Verify the command output to confirm that monitor mode was enabled
        if f'{interface}mon' in result.stdout:
            print(f"Monitor mode enabled on {interface}")
            return True
        else:
            print(f"Failed to enable monitor mode on {interface}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def disable_monitor_mode(interface):
    try:
        result = subprocess.run(['sudo', 'airmon-ng', 'stop', interface + "mon"], check=True, capture_output=True, text=True)
        process2 = subprocess.run(['sudo', 'systemctl', 'start', 'NetworkManager'], check=True, capture_output=True, text=True)

        if 'monitor mode disabled' in result.stdout:
            print(f"Monitor mode disabled on {interface}")
            print("NetworkManager service started.")
            return True
        else:
            print(f"Failed to disable monitor mode on {interface}")
            return False

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def offer_exit_option(interface):
    print("Failed to enable monitor mode on the selected interface.")
    print("Do you want to exit the program and disable monitor mode?")
    while True:
        choice = input("Enter 'y' to exit or 'n' to continue: ")
        if choice.lower() == 'y':
            print("Exiting program...")
            if disable_monitor_mode(interface):
                print("Network manager protocol restored.")
            else:
                print("Failed to restore network manager protocol.")
            exit()
        elif choice.lower() == 'n':
            print("Continuing program...")
            break
        else:
            print("Invalid input, please enter 'y' or 'n'.")

def display_available_networks(interface):
    print("Displaying available networks...")
    try:
        subprocess.run(['sudo', 'airodump-ng', '--band', 'a', interface], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

