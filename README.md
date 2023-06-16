# balena_uuid_osversion_vpn
Script to ssh into the devices and retrieve the VPN endpoint that is configured

The steps performed by the script are:

- Retrieves all the devices associated to the org using the API
- ssh into each of the devices
- grep the contents of /etc/openvpn/openvpn.conf
- returns the first entry with 'remote'. Eg. remote vpn.balena-cloud.com
- prints the result: [uuid, os version, VPN endpoint]


NOTES: this script only works with online devices.
