from ..common import getDistance
import pandas as pd


def getBusesNearPoint(lat, lon, locations: pd.DataFrame, radius: float = 50) -> pd.DataFrame:
    distances = getDistance(lat, lon, locations["Lat"], locations["Lon"])
    busesNearPoint = locations[distances < radius]
    grouped = busesNearPoint.groupby("Lines").size()

    return grouped
