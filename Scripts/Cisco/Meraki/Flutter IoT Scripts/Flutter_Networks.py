import requests

org_id = 808959083066425849
token = str(input('Please enter your token: '))

url = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
payload = None

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

response = requests.request('GET', url=url, headers=headers, data=payload)
response = response.json()

net_ids = {}
keys = []
values = []
for item in response:
    for k, v in item.items():
        if k == 'id':
            keys.append(v)
        elif k == 'name':
            values.append(v)

for name, id in zip(values, keys):
    net_ids[name] = id