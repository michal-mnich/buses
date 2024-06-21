from ..common import readCsv, readJson, writeCsv, writeJson
from .computeRoutes import getRoutes
from .speedingBuses import getSpeeds, getSpeedingLocations, getSpeedingBusesCount
from .lateBuses import getLateBuses, mostLateLines
from .visualize import (
    createSpeedingsMap,
    createLateDistribution,
    createSpeedsDistribution,
    createNearbyLinesPieChart,
    createLateLinesBarChart,
)
from .pointCounter import getBusesNearPoint
import argparse
import os


def parseArgs():
    global args

    parser = argparse.ArgumentParser(description="Analyzer bus data")
    parser.add_argument(
        "--idir",
        type=str,
        default="data/scraped",
        help="Input directory with the scraped data (default: data/scraped)",
    )
    parser.add_argument(
        "--odir",
        type=str,
        default="data/analyzed",
        help="Output directory for the analyzed data (default: data/analyzed)",
    )

    args = parser.parse_args()
    os.makedirs(args.odir, exist_ok=True)


def getSchedules():
    try:
        schedules = readJson(f"{args.idir}/schedules*.json")

    except FileNotFoundError:
        raise FileNotFoundError("Parse schedules first!")

    return schedules


def getLocations():
    try:
        locations = readCsv(f"{args.idir}/locations*.csv")
    except FileNotFoundError:
        raise FileNotFoundError("Parse locations first!")

    return locations


def getStops():
    try:
        stops = readCsv(f"{args.idir}/stops*.csv")
    except FileNotFoundError:
        raise FileNotFoundError("Parse stops first!")

    return stops


def main():
    parseArgs()

    routes = getRoutes(getSchedules())
    writeJson(routes, f"{args.odir}/routes.json")

    speeds = getSpeeds(getLocations())
    writeCsv(speeds, f"{args.odir}/speeds.csv")
    writeJson(getSpeedingBusesCount(speeds), f"{args.odir}/speedingBusesCount.json")
    createSpeedsDistribution(speeds, f"{args.odir}/speedsDistribution.html")

    speedingLocations = getSpeedingLocations(speeds)
    writeCsv(speedingLocations, f"{args.odir}/speedingLocations.csv")
    createSpeedingsMap(speedingLocations, f"{args.odir}/speedings.html")

    lateBuses = getLateBuses(getLocations(), getStops(), routes)
    writeCsv(lateBuses, f"{args.odir}/lateBuses.csv")
    createLateDistribution(lateBuses, f"{args.odir}/lateDistribution.html")
    mll = mostLateLines(lateBuses)
    createLateLinesBarChart(mll, f"{args.odir}/mostLateLines.html")

    places = {
        "Rondo Dmowskiego": (52.230139, 21.011960),
        "Wawelska Grójecka": (52.211045, 20.976225),
        "Rondo Daszyńskiego": (52.230429, 20.983877),
        "Kampus Główny UW": (52.239726, 21.016820),
        "Plac na Rozdrożu": (52.219401, 21.025217),
    }

    for placename, (lat, lon) in places.items():
        nearbyLines = getBusesNearPoint(lat, lon, getLocations())
        filename = placename.replace(" ", "_").lower()
        createNearbyLinesPieChart(
            nearbyLines, placename, f"{args.odir}/{filename}.html"
        )

    # najczęściej spóźniająca się linia



if __name__ == "__main__":
    main()
