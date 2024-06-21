import pandas as pd
from ..common import APIKEY, getFromApi, sanitizeDict

url = "https://api.um.warszawa.pl/api/action/dbstore_get"
params = {
    "apikey": APIKEY,
    "id": "ab75c33d-3a26-4342-b36a-6e5fef0a3ac3",
}


def scrapeStops():
    data = getFromApi(url, params)

    print("Scraped", len(data), "stops")

    df = pd.DataFrame(list(map(sanitizeDict, data)))
    df.insert(0, "id", df["zespol"] + "_" + df["slupek"])
    df.drop(columns=["zespol", "slupek"], inplace=True)

    return df
