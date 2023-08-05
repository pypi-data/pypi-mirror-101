import random
import requests

def nsfw():
    randomnumber = random.randint(1, 30)
    r = requests.get("https://api.hentaihaven.dev/api.json").json()
    idk = r[f"{randomnumber}"]
    return idk