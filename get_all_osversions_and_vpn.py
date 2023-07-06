import requests
import pandas as pd
import subprocess

def is_older_version(current_version, compare_version):
    # Check if the current_version contains a "+", and if it does, only keep the part before the "+"
    if '+' in current_version:
        current_version = current_version.split('+')[0]
    
    current_name, current_version_num = current_version.split(maxsplit=1)
    compare_name, compare_version_num = compare_version.split(maxsplit=1) 

    # If the current version's name is 'resin', it's older
    if current_name.lower() == 'resin':
        return True

    # Split the versions into their components and fill missing parts with zeros
    current_version_parts = list(map(int, (current_version_num.split('.') + ['0', '0'])[:3]))
    compare_version_parts = list(map(int, (compare_version_num.split('.') + ['0', '0'])[:3]))

    # If the name is balena
    if 'balena' in current_name.lower():
        # If x is 2 then compare y and then z
        if current_version_parts[0] == 2:
            # Compare the version components
            for current, compare in zip(current_version_parts[1:], compare_version_parts[1:]):
                if current < compare:
                    return True
                elif current > compare:
                    return False
        # If x is greater than 2000 then the version is older if it's less than 2020.07.2
        elif current_version_parts[0] > 2000:
            if current_version_parts[0] < 2021 or (current_version_parts[0] == 2021 and (current_version_parts[1] < 1 or (current_version_parts[1] == 1 and current_version_parts[2] < 0))):
                return True

    # If all components are equal or conditions are not met, the versions are the same or current version is not older
    return False


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
    is_online = device['is_online']
    
    if os_version is None or is_older_version(os_version, 'balena 2.61.2'):
        if is_online:
            # Use balena CLI to get the VPN endpoint from the openvpn.conf file for the device
            command = f"echo 'grep remote /etc/openvpn/openvpn.conf; exit;' | balena ssh {device_uuid} | grep remote"
            vpn_result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if vpn_result.returncode == 0:
                vpn_line = vpn_result.stdout.strip()  # remove trailing newline
                vpn_endpoint = vpn_line.split()[1]  # the second word in the line
            else:
                vpn_endpoint = 'Not available'
        else:
            vpn_endpoint = 'Offline'

        result = {
            'Device UUID': device_uuid,
            'OS Version': os_version,
            'VPN Endpoint': vpn_endpoint
        }
        print(result)

        # Add the data to the list
        device_data.append(result)

print("Done. Printing results.")
# Convert the list to a pandas DataFrame and print it
pd.set_option('display.max_rows', 10000)
df = pd.DataFrame(device_data)
print(df)
