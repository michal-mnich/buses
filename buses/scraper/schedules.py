from ..common import APIKEY, getFromApi, sanitizeDict

url = "https://api.um.warszawa.pl/api/action/dbtimetable_get"
params = {
    "apikey": APIKEY,
    "id": "e923fa0e-d96c-43f9-ae6e-60518c9f3238",
    "busstopId": None,
    "busstopNr": None,
    "line": None,
}


def scrapeScheduleForOneStopOneLine(id, line):
    params["busstopId"], params["busstopNr"] = id.split("_")
    params["line"] = line

    data = getFromApi(url, params)

    return list(map(sanitizeDict, data))


def scrapeScheduleForOneStopAllLines(id, stop_lines):
    schedule = {}

    for line in stop_lines:
        tmp = scrapeScheduleForOneStopOneLine(id, line)

        if tmp:
            schedule[line] = tmp

    return schedule


def scrapeSchedulesForAllStopsAllLines(lines):
    n = len(lines)
    schedules = {}

    try:
        for i, stop in enumerate(lines):
            tmp = scrapeScheduleForOneStopAllLines(stop, lines[stop])

            if tmp:
                schedules[stop] = tmp

            print(f"Scraped schedules for {i+1}/{n} stops", end="\r")

    except KeyboardInterrupt:
        print("Interrupted")

    return schedules
