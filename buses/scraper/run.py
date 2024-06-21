from ..common import writeCsv, writeJson, readJson, readCsv
from .locations import scrapeLocations
from .stops import scrapeStops
from .lines import scrapeLinesForAllStops
from .schedules import scrapeSchedulesForAllStopsAllLines
import argparse
import time
import os


csvModes = ["locations", "stops"]
jsonModes = ["lines", "schedules"]


def parseArgs():
    global args

    parser = argparse.ArgumentParser(description="Scrape bus data")
    parser.add_argument(
        "--mode",
        type=str,
        default="all",
        choices=csvModes + jsonModes + ["all"],
        help="Mode of operation (default: all)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=-1,
        help="Duration in seconds for scraping locations (default: -1), negative for infinite",
    )
    parser.add_argument(
        "--odir",
        type=str,
        default="data/scraped",
        help="Output directory for the scraped data (default: data/scraped)",
    )

    args = parser.parse_args()
    os.makedirs(args.odir, exist_ok=True)


def saveData(data, mode):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"{args.odir}/{mode}_{timestamp}"

    if mode in csvModes:
        filename += ".csv"
        writeCsv(data, filename)

    elif mode in jsonModes:
        filename += ".json"
        writeJson(data, filename)


def getStopsList():
    try:
        stops_df = readCsv(f"{args.odir}/stops*.csv")
    except FileNotFoundError:
        print("Scraping stops first...")
        stops_df = scrapeStops()

    return stops_df["id"].tolist()


def getLines():
    try:
        lines = readJson(f"{args.odir}/lines*.json")
    except FileNotFoundError:
        print("Scraping lines first...")
        lines = scrapeLinesForAllStops(getStopsList())

    return lines


def handleMode(mode):
    if mode == "all":
        for m in csvModes + jsonModes:
            handleMode(m)
        return

    elif mode == "locations":
        out = scrapeLocations(args.duration)

    elif mode == "stops":
        out = scrapeStops()

    elif mode == "lines":
        out = scrapeLinesForAllStops(getStopsList())

    elif mode == "schedules":
        out = scrapeSchedulesForAllStopsAllLines(getLines())

    saveData(out, mode)


def main():
    parseArgs()
    handleMode(args.mode)


if __name__ == "__main__":
    main()
