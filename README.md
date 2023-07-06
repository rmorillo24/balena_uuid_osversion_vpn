# Scripts for devices affected by balena's VPN sunsetting
There are two scripts in this project to get:
- The endpoint configured in every active device
- The deactivated devices which last os_version resported is affected

## Requirements
- Requires the CLI installed
- Log-in to the CLI with a user that can use the API key generated and used in the script
- Install SSH keys to enable CLI access using this instructions: https://docs.balena.io/learn/manage/ssh-access/#add-an-ssh-key-to-balenacloud
- Check https://blog.balena.io/sunsetting-vpn-balenacloud-and-introducing-cloudlink/ for the explanation of the situation and OS versions affected
- 
## get_all_os_versions_and_vpn.py
Script to ssh into every active the devices and retrieve the VPN endpoint that is configured. Obviously, this will only work for devices that are online, so if you are unsure, please execute this script regularly

The steps performed by the script are:

- Retrieves all the devices associated to the org using the API, or uses an input file to narrow the search (one UUID per line)
- Check if the OS version is affected
- ssh into each of the affected devices
- grep the contents of /etc/openvpn/openvpn.conf
- returns the first entry with 'remote'. Eg. remote vpn.balena-cloud.com
- prints the result: [uuid, os version, VPN endpoint]
- if device is offline (is_online==false), indicate it in the endpoint field

If the VPN Endpoint is "Not available", a possible reason is that the SSH keys are not set correcly. Check https://docs.balena.io/learn/manage/ssh-access/#add-an-ssh-key-to-balenacloud

##  get_old_deactivated_devices.py
Script to query the API to retrieve all the deactivated devices, and print those that are affected by the os version.
