import requests
import pandas as pd
import subprocess
import json
import re
# replace with your balena API key
api_key = "your_api_key"

# The base URL for the balenaCloud API
api_base_url = "https://api.balena-cloud.com/v6/"

headers = {
    'Authorization': 'Bearer ' + api_key
}

# Request all devices
response = requests.get(api_base_url + 'device', headers=headers)
data = response.json()

# Prepare an empty list to hold the data
device_data = []

# Iterate through all devices
for device in data['d']:
    device_uuid = device['uuid']
    os_version = device['os_version']

    # Use balena CLI to get the VPN endpoint from the openvpn.conf file for the device
    command = f"echo 'grep remote /etc/openvpn/openvpn.conf; exit;' | balena ssh {device_uuid} | grep remote"
    vpn_result = subprocess.run(command, capture_output=True, text=True, shell=True)
    if vpn_result.returncode == 0:
        vpn_line = vpn_result.stdout.strip()  # remove trailing newline
        vpn_endpoint = vpn_line.split()[1]  # the second word in the line
    else:
        vpn_endpoint = 'Not available'

    result = {
        'Device UUID': device_uuid,
        'OS Version': os_version,
        'VPN Endpoint': vpn_endpoint
    }
    # print(result)

    # Add the data to the list
    device_data.append(result)

# Convert the list to a pandas DataFrame and print it
df = pd.DataFrame(device_data)
print(df)
