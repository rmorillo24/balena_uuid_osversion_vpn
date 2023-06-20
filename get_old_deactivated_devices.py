import requests
import pandas as pd


def is_older_version(current_version, compare_version):
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
            if current_version_parts[0] < 2020 or (current_version_parts[0] == 2020 and (current_version_parts[1] < 7 or (current_version_parts[1] == 7 and current_version_parts[2] < 2))):
                return True

    # If all components are equal or conditions are not met, the versions are the same or current version is not older
    return False



# Replace with your actual API key
api_key = 'your_api_key'


headers = {
    'Authorization': 'Bearer ' + api_key,
}

# Add filter to get only deactivated devices
params = (
    ('$filter', 'is_active eq false'),
)


response = requests.get('https://api.balena-cloud.com/v6/device', headers=headers, params=params)
data = response.json()


device_data = []

for device in data['d']:
    os_version = device['os_version']
    print(os_version)
    if os_version is None or is_older_version(os_version, 'balena 2.61.2'):
        device_data.append({
            'UUID': device['uuid'], 
            'OS Version': os_version
    })

pd.set_option('display.max_rows', 5000)
df = pd.DataFrame(device_data)
print(df)


####
# test data
# data = {'d':[
        # {'uuid':1, 'os_version':'balena 2.61.1'}, #old
        # {'uuid':2, 'os_version':'balena 2.61.3'}, #not old
        # {'uuid':3, 'os_version':'balena 2020.8'}, #not old
        # {'uuid':4, 'os_version':'balena 2020.7.1'}, #old
        # {'uuid':5, 'os_version':'balena 2020.7.2'}, #not old
        # {'uuid':6, 'os_version':'balena 2020.7'}, #old
        # {'uuid':7, 'os_version':'resin 2.61.1'}, #old
        # {'uuid':8, 'os_version':'balenaOS 2.101.1'} #not old
        # ]}
