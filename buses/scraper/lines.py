from operator import itemgetter
from ..common import APIKEY, getFromApi, sanitizeDict

url = "https://api.um.warszawa.pl/api/action/dbtimetable_get"
params = {
    "apikey": APIKEY,
    "id": "88cd555f-6f31-43ca-9de4-66c479ad5942",
    "busstopId": None,
    "busstopNr": None,
}


def scrapeLinesForOneStop(id):
    params["busstopId"], params["busstopNr"] = id.split("_")

    data = getFromApi(url, params)

    return list(map(itemgetter("linia"), map(sanitizeDict, data)))


def scrapeLinesForAllStops(stops):
    n = len(stops)
    lines = {}

    for i, id in enumerate(stops):
        tmp = scrapeLinesForOneStop(id)

        if tmp:
            lines[id] = tmp

        print(f"Scraped {i+1}/{n} stops", end="\r")

    return lines
