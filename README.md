# Samsung-AC-Controller
 
This script allows you to control a Samsung Air Conditioner using the SmartThings API. It provides functionalities to list devices, get device status, control the device (on/off), change AC mode, set temperature, and set fan mode.

## Prerequisites

- Python 3.x
- `requests` library
- `prettytable` library

You can install the required libraries using the following commands:

```bash
pip install requests
pip install prettytable
```

## Setup
1. Clone the repository or download the script file.
2. Set your SmartThings API Bearer Token and Samsung AC Device ID in the script:

```python
# API Variables Needed:
API_URL = "https://api.smartthings.com/v1"
BEARER_TOKEN = 'YOUR_BEARER_TOKEN_HERE'

# Samsung AC ID:
DEVICE_ID = 'YOUR_DEVICE_ID_HERE'
```

## Usage
Run the script:

```bash
python samsung_ac_controller.py
```

## Features

**1. List Devices**
   - Lists all Samsung Air Conditioners linked to your SmartThings account.

**2. Get Device Status**
   - Fetches and displays the current status of the specified Samsung Air Conditioner.

**3. Control Device (On/Off)**
   - Turns the Samsung Air Conditioner on or off.

**4. Change AC Mode**
   - Changes the mode of the Samsung Air Conditioner to one of the following: cool, dry, wind, auto, heat.

**5. Set Temperature**
   - Sets the desired temperature for the Samsung Air Conditioner.

**6. Set Fan Mode**
   - Sets the fan mode of the Samsung Air Conditioner to one of the following: auto, low, medium, high, turbo.

## Managing Devices with the Devices API
Interact with the Devices API to access and control Samsung Air Conditioners integrated with the SmartThings platform. The Devices API allows you to control connected devices, access device metadata, and retrieve device states.

**Note:** You will need a Personal Access Token (PAT) with the appropriate scopes to interact with the Devices API.

Example Payload Using Postman
This example demonstrates how to use the Postman app to send a GET request to a Samsung Air Conditioner where <deviceID> is the device ID of the Samsung Air Conditioner you want to retrieve info for.

NOTE: In the Authorization tab of your GET request in Postman, select **Bearer Token** as your authorization type. Enter your **PAT** in the Token field.

1. List Devices:
```bash
https://api.smartthings.com/v1/devices
```

2. Get Device Status:
```bash
https://api.smartthings.com/v1/devices/<deviceID>
```

## Menu:
1. List Devices
2. Get Device Status
3. Control Device (On/Off)
4. Change AC Mode
5. Set Temperature
6. Set Fan Mode
7. Exit

## License
This project is licensed under the MIT License.
