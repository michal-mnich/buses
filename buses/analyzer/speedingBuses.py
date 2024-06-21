import pandas as pd
import numpy as np
from ..common import getDistance, SPEEDLIMIT, PROXIMITY, MAXSPEED


def getSpeeds(locations: pd.DataFrame) -> pd.DataFrame:
    locations["Time"] = pd.to_datetime(locations["Time"], errors="coerce")
    locations.dropna(subset=["Time"], inplace=True)

    locations = locations.sort_values(by=["VehicleNumber", "Time"])

    locations["prevLat"] = locations.groupby("VehicleNumber")["Lat"].shift(1)
    locations["prevLon"] = locations.groupby("VehicleNumber")["Lon"].shift(1)
    locations["prevTime"] = locations.groupby("VehicleNumber")["Time"].shift(1)

    locations.dropna(subset=["prevLat", "prevLon", "prevTime"], inplace=True)

    locations["dx"] = getDistance(
        locations["Lat"], locations["Lon"], locations["prevLat"], locations["prevLon"]
    )
    locations["dt"] = (locations["Time"] - locations["prevTime"]).dt.total_seconds()
    locations["v"] = (locations["dx"] / locations["dt"]) * 3.6

    locations.drop(columns=["prevLat", "prevLon", "prevTime", "dx", "dt"], inplace=True)
    locations.dropna(subset=["v"], inplace=True)

    speeds = locations[locations["v"] < MAXSPEED]

    return speeds


def getSpeedingBusesCount(speeds: pd.DataFrame) -> int:
    speedingBuses = speeds[speeds["v"] > SPEEDLIMIT]

    return speedingBuses["VehicleNumber"].nunique()


def getSpeedingLocations(speeds: pd.DataFrame) -> pd.DataFrame:
    speedingLocations = speeds[speeds["v"] > SPEEDLIMIT]

    speedingsNearby = {}
    count = 0
    total = len(speedingLocations)
    for i, row in speedingLocations.iterrows():
        speedingsDistances = getDistance(
            row["Lat"],
            row["Lon"],
            speedingLocations["Lat"],
            speedingLocations["Lon"],
        )
        speedingsNearby[i] = np.sum(speedingsDistances < PROXIMITY)
        count += 1
        print(f"Checked {count}/{total} speeding locations", end="\r")

    speeds["SpeedingsNearby"] = pd.Series(speedingsNearby)

    num_rows = int(np.ceil(0.2 * len(speedingLocations)))
    top_20_percent = speeds.nlargest(num_rows, "SpeedingsNearby", keep="all")

    return top_20_percent.sort_values(by=["SpeedingsNearby"], ascending=False)
