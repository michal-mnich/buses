import pandas as pd
import time
from ..common import APIKEY, getFromApi

url = "https://api.um.warszawa.pl/api/action/busestrams_get"
params = {
    "apikey": APIKEY,
    "resource_id": "f2e5503e-927d-4ad3-9500-4ab9e55deb59",
    "type": 1,
}


def scrapeLocations(duration, cooldown=10):
    rows = []
    elapsed = 0

    if duration < 0:
        duration = 999999999

    try:
        while elapsed < duration:
            data = getFromApi(url, params)
            print("Scraped", len(data), "locations")
            rows.extend(data)

            elapsed += cooldown
            if elapsed < duration:
                print(f"Sleeping for {cooldown}s...", end="\r")
                time.sleep(cooldown)

    except KeyboardInterrupt:
        print("Interrupted by the user")

    return pd.DataFrame(rows)
