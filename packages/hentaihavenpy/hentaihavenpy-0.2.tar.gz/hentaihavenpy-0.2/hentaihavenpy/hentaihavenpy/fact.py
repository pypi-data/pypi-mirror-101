import random
import requests

def fact():
    randomnumber = random.randint(1, 26)
    r = requests.get("https://api.hentaihaven.dev/factapi.json").json()
    factlol = r[f"{randomnumber}"]
    return factlol