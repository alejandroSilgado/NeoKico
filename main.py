from functions import *

if __name__ == "__main__":
    try:
        display_logo()
        interfaces = list_wireless_interfaces()
        if interfaces:
            selected_interface = select_interface(interfaces)
            print(f"Selected interface: {selected_interface}")
            if enable_monitor_mode(selected_interface):
                print("Monitor mode enabled successfully.")
                display_available_networks(selected_interface)
                print("Press Ctrl+C to exit and disable monitor mode.")
                while True:
                    time_module.sleep(1)
            else:
                offer_exit_option(selected_interface)
        else:
            print("No wireless interfaces found.")
    except KeyboardInterrupt:
        print("\nExiting script...")
        if disable_monitor_mode(selected_interface):
            print("Network manager protocol restored.")
        else:
            print("Failed to restore network manager protocol.")