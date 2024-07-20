import requests
import json
from prettytable import PrettyTable

#_______________________________________________________________________________________________________________________________________
# API Variables Needed:
API_URL = "https://api.smartthings.com/v1"
BEARER_TOKEN = ''

# Samsung AC ID:
DEVICE_ID = ''

#_______________________________________________________________________________________________________________________________________
# Banner

def print_banner():
    print('''
                                                                                 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                 
                                                                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%          
                                                           %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%      
                                                  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
                                           %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
                                     %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                               %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                           %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                     =====+*#%%%%%%#******%%%%%%*****#%%%#*****#%%%%%#*+++*#%%%%%#***%%%***%%%%#*****%%%***#%%%%%#*+++*#%%%%%%%%%%%%%%%%%%%%%
                  %%+=========%%%%%=======#%%%%%===+==#%%======*%%%%=========%%%%====%%#===*%%%*=====*%%===+%%%%=========*%%%%%%%%%%%%%%%%%  
              %%%%%%====%%*===%%%%%===*===*%%%%#===#==*%%==*===*%%%*===#%%===*%%%+===%%#===*%%%*======%%===+%%%*===%%%+===%%%%%%%%%%%%%%%    
           %%%%%%%%%+====+#%%%%%%%*===%*===%%%%#===%==+%#==#===*%%%%=====*%%%%%%%====%%#===*%%%*===%==*%===+%%%*===%%%%%%%%%%%%%%%%%%%%%     
        %%%%%%%%%%%%%%+======%%%%%===+%#===*%%%#===%*==%+==%===*%%%%%*======*%%%%+===%%#===*%%%*===%+==%+==+%%%*===%%=====%%%%%%%%%%%        
     %%%%%%%%%%%%%%%%%%%%*====#%%#===*%%===+%%%*===%%==*==*%===+%%%%%%%%#====+%%%====%%#===*%%%*===%%==*+==+%%%*===%%%+===%%%%%%%%           
    %%%%%%%%%%%%%%%%====%%*===#%%*===#%%====%%%*===%%+====#%===+%%%+===#%%====%%%+===%%#===*%%%*===%%*==+==+%%%*===#%%+===%%%%%              
  %%%%%%%%%%%%%%%%%%+=========%%%====%%%*===*%%*===%%*====%%===+%%%%=========*%%%*=========%%%%*===%%%=====+%%%%=========#%                  
 %%%%%%%%%%%%%%%%%%%%%**+++*#%%%%####%%%%####%%%###%%%####%%####%%%%%#*+++*#%%%%%%%#**+**%%%%%%%###%%%%####%%%%%%%#***==                     
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                          
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                               
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                    
 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% AC Controller %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                           
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                                  
      %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                                           
          %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                                                    
                 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%                                                                                
          ''')

#_______________________________________________________________________________________________________________________________________
# 1. List Devices
 
def list_devices():
    try:
        url = f"{API_URL}/devices"
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        devices = response.json()
        
        # Create and print the table
        table = PrettyTable()
        table.field_names = ["Name", "ID"]
        
        found_devices = False
        for device in devices.get("items", []):
            if "Samsung" in device.get("manufacturerName", "") and "Air Conditioner" in device.get("deviceTypeName", ""):
                table.add_row([device['name'], device['deviceId']])
                found_devices = True
        
        if not found_devices:
            print("No Samsung Air Conditioners found.")
        else:
            print("Samsung Air Conditioners:")
            print(table)

    except requests.RequestException as e:
        print(f"Error fetching device list: {e}")
    except json.JSONDecodeError:
        print("Error parsing device list response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#_______________________________________________________________________________________________________________________________________
# 2. Device Status

def get_device_status(DEVICE_ID):
    try:
        url = f"{API_URL}/devices/{DEVICE_ID}/status"
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        status = response.json()
        
        if not status or not status.get("components"):
            print(f"No status found for device ID: {DEVICE_ID}")
            return
        
        components = status.get("components", {}).get("main", {})
        
        # Extract details
        ac_name = components.get("ocf", {}).get("n", {}).get("value", "Unknown")
        power_state = components.get("switch", {}).get("switch", {}).get("value", "Unknown")
        mode = components.get("airConditionerMode", {}).get("airConditionerMode", {}).get("value", "Unknown")

        temperature_info = components.get("temperatureMeasurement", {})
        temperature_value = temperature_info.get("temperature", {}).get("value", "Unknown")
        temperature_unit = temperature_info.get("temperature", {}).get("unit", "Unknown")
        temperature = f"{temperature_value}°{temperature_unit}" if temperature_value != "Unknown" else "Unknown°C"
        
        humidity_info = components.get("relativeHumidityMeasurement", {})
        humidity_value = humidity_info.get("humidity", {}).get("value", "Unknown")
        humidity_unit = humidity_info.get("humidity", {}).get("unit", "Unknown")
        humidity = f"{humidity_value}{humidity_unit}" if humidity_value != "Unknown" else "Unknown%"

        # Create and print the table
        table = PrettyTable()
        table.field_names = ["Device ID", "AC Name", "Power State", "Mode", "Temperature", "Humidity"]
        table.add_row([DEVICE_ID, ac_name, power_state, mode, temperature, humidity])
        
        print(table)

    except requests.RequestException as e:
        print(f"Error fetching device status: {e}")
    except json.JSONDecodeError:
        print("Error parsing device status response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#_______________________________________________________________________________________________________________________________________
# 3. Control Device (On/Off)

def control_device(DEVICE_ID, command):
    try:
        url = f"{API_URL}/devices/{DEVICE_ID}/commands"
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "commands": [
                {
                    "component": "main",
                    "capability": "switch",
                    "command": command
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        response_data = response.json()
        if "results" in response_data and response_data["results"]:
            status = response_data["results"][0]["status"]
            if status == "COMPLETED":
                print(f"Device {command} response for {DEVICE_ID}: Success")
            else:
                print(f"Device {command} response for {DEVICE_ID}: Failed")
        else:
            print(f"Device {command} response for {DEVICE_ID}: Failed (no results found)")
    except requests.RequestException as e:
        print(f"Error controlling device: {e}")
    except json.JSONDecodeError:
        print("Error parsing control device response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#_______________________________________________________________________________________________________________________________________
# 4. Change AC Mode

def change_ac_mode(DEVICE_ID, mode):
    try:
        url = f"{API_URL}/devices/{DEVICE_ID}/commands"
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "commands": [
                {
                    "component": "main",
                    "capability": "airConditionerMode",
                    "command": "setAirConditionerMode",
                    "arguments": [mode]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        response_data = response.json()
        if "results" in response_data and response_data["results"]:
            status = response_data["results"][0]["status"]
            if status == "COMPLETED":
                print(f"Change mode to {mode} response for {DEVICE_ID}: Success")
            else:
                print(f"Change mode to {mode} response for {DEVICE_ID}: Failed")
        else:
            print(f"Change mode to {mode} response for {DEVICE_ID}: Failed (no results found)")
    except requests.RequestException as e:
        print(f"Error changing AC mode: {e}")
    except json.JSONDecodeError:
        print("Error parsing change AC mode response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#_______________________________________________________________________________________________________________________________________
# 5. Set Temperature

def set_temperature(DEVICE_ID, temperature):
    try:
        url = f"{API_URL}/devices/{DEVICE_ID}/commands"
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "commands": [
                {
                    "component": "main",
                    "capability": "thermostatCoolingSetpoint",
                    "command": "setCoolingSetpoint",
                    "arguments": [temperature]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        response_data = response.json()
        if "results" in response_data and response_data["results"]:
            status = response_data["results"][0]["status"]
            if status == "COMPLETED":
                print(f"Set temperature to {temperature}°C response for {DEVICE_ID}: Success")
            else:
                print(f"Set temperature to {temperature}°C response for {DEVICE_ID}: Failed")
        else:
            print(f"Set temperature to {temperature}°C response for {DEVICE_ID}: Failed (no results found)")
    except requests.RequestException as e:
        print(f"Error setting temperature: {e}")
    except json.JSONDecodeError:
        print("Error parsing set temperature response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#_______________________________________________________________________________________________________________________________________
# Set Fan Mode

def set_fan_mode(DEVICE_ID, mode):
    try:
        url = f"{API_URL}/devices/{DEVICE_ID}/commands"
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json"
        }
        data = {
            "commands": [
                {
                    "component": "main",
                    "capability": "airConditionerFanMode",
                    "command": "setFanMode",
                    "arguments": [mode]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  
        response_data = response.json()
        if "results" in response_data and response_data["results"]:
            status = response_data["results"][0]["status"]
            if status == "COMPLETED":
                print(f"Set fan mode to {mode} response for {DEVICE_ID}: Success")
            else:
                print(f"Set fan mode to {mode} response for {DEVICE_ID}: Failed")
        else:
            print(f"Set fan mode to {mode} response for {DEVICE_ID}: Failed (no results found)")
    except requests.RequestException as e:
        print(f"Error setting fan mode: {e}")
    except json.JSONDecodeError:
        print("Error parsing set fan mode response.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

#_______________________________________________________________________________________________________________________________________
# Menu

def print_menu():
    print("\nMenu:")
    print("1. List Devices")
    print("2. Get Device Status")
    print("3. Control Device (On/Off)")
    print("4. Change AC Mode")
    print("5. Set Temperature")
    print("6. Set Fan Mode")
    print("7. Exit\n")

#_______________________________________________________________________________________________________________________________________
# Main Function

def main():
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == '1':
            list_devices()
        elif choice == '2':
            get_device_status(DEVICE_ID)
        elif choice == '3':
            command = input("Enter the command (on/off): ")
            control_device(DEVICE_ID, command)
        elif choice == '4':
            mode = input("Enter the AC mode (cool, dry, wind, auto, heat): ")
            change_ac_mode(DEVICE_ID, mode)
        elif choice == '5':
            try:
                temperature = float(input("Enter the temperature in °C: "))
                set_temperature(DEVICE_ID, temperature)
            except ValueError:
                print("Invalid temperature input. Please enter a numeric value.")
        elif choice == '6':
            mode = input("Enter the fan mode (auto, low, medium, high, turbo): ")
            set_fan_mode(DEVICE_ID, mode)
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

#_______________________________________________________________________________________________________________________________________

if __name__ == "__main__":
    print_banner()
    main()
