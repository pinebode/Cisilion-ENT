import requests
from Flutter_Networks import net_ids, token

networks = net_ids
auth = token
user = input("Which of the following sites is this for (Porto, Cluj-Napoca, Hyderabad, London, Gibraltar, Dublin, Malta)? ").title()
id = networks[user]


url = f"https://api.meraki.com/api/v1/networks/{id}/wireless/ssids"

payload = {}
headers = {
  'Accept': 'application/json',
  'Authorization': f"Bearer {token}"
}

response = requests.request("GET", url, headers=headers, data=payload)
response = response.json()

ssids = {}
numbers = []
names = []
for item in response:
    for k, v in item.items():
        if k == 'number':
            numbers.append(v)
        elif k == 'name':
            names.append(v)

for name, number in zip(names, numbers):
    ssids[name] = number

    #print(item,'\n', "-" * 200)
