import requests
import json
from Get_Flutter_SSID_PSKs import identity_ssid, auth, id, number, payload

# Here we are asking the user for the following: SSID name, SSID ID, PSK.
user = input("From the list above, Enter the name of the SSID you would like to change: ")
user.title()
ssid_id = int(input("Please enter the ID of the SSID (for e.g. 808959083066436318):"))
psk = None
while not psk:
    prompt = input("\nPlease enter the new PSK (Min 8 chars accepted. Remember also to take a note of the old PSK!): ")
    if prompt.isdigit():
        print('Password must contain a mixture of Letters and numbers. Try Again!')
    elif prompt.isalpha():
        print('Password must contain a mixture of Letters and numbers. Try Again!')
    elif len(prompt) < 8:
        print('Password too short. Minimun length must be 8 Characters.')
    else:
        print("Password accepted.")
        psk = prompt
        break

url = f"https://api.meraki.com/api/v1/networks/{id}/wireless/ssids/{number}/identityPsks/{ssid_id}"

# Here, the payload is a dictionary which is imported from the module above but substituted with the information entered by the user. Any unecessary info is also deleted.
# this object will be passed to the API endpoint as payload when pushing the change. Here is also where the PSK is defined.
payload = payload[user]
del payload['id']
del payload['wifiPersonalNetworkId']
payload['passphrase'] = psk
print(payload)

'''
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': f'Bearer {auth}'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)
'''
