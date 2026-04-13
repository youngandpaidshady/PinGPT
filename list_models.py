import requests
api_key = "AIzaSyBeY454G8AuxpnK1b1ibcta9M71izVdJC8"
resp = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}").json()
models = resp.get('models', [])
with open('models.txt', 'w') as f:
    for m in models:
        f.write(m['name'] + ' - ' + m.get('description', '') + '\n')
