import requests

def fetch(url):
    r = requests.get(url, allow_redirects=True)
    open('workspace/vault.zip', 'wb').write(r.content)