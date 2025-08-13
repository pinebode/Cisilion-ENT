import requests
from Get_Flutter_SSIDs import auth, networks, id, ssids

user = input('Please enter the name of the SSID you want to change e.g.(FLTR-IOT): ')
user = user.upper()
number = ssids[user]

url = f"https://api.meraki.com/api/v1/networks/{id}/wireless/ssids/{number}/identityPsks"

payload = {}
headers = {
  'Accept': 'application/json',
  'Authorization': f'Bearer {auth}'
}

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()

identity_ssid = {}
names = []
ids = []
# Below code is used to get the names and id's and place them in the lists initialized above.
for item in response:
    for k, v in item.items():
        if k == 'id':
            ids.append(v)
        elif k == 'name':
            names.append(v)

# Here we are printing the names and id's to the screen one by one
for n, i in zip(names, ids):
    identity_ssid[n] = i
    print(f"\nName: {n}\nID: {i}")
    print("-"*30)

# Here, we are storing the other keys and values in a dictionary object which will be used when pushing the PSK.
payload = {}
for item in response:
    payload[item['name']] = item

#print(f"\n{payload}")