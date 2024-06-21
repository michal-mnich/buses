from ..common import PROXIMITY, getDistance
import pandas as pd
import numpy as np
from datetime import datetime


def getLateBuses(
    locations: pd.DataFrame, stops: pd.DataFrame, routes: dict
) -> pd.DataFrame:
    lateBuses = []

    for i, stop in stops.iterrows():
        distances = getDistance(
            stop["szer_geo"], stop["dlug_geo"], locations["Lat"], locations["Lon"]
        )
        busesonStop = locations[distances < PROXIMITY]
        for _, bus in busesonStop.iterrows():
            try:
                expTime = routes[bus["Lines"]][bus["Brigade"]][stop["id"]]
                actualTime = bus["Time"]

                actualTime_dt = datetime.strptime(actualTime, "%Y-%m-%d %H:%M:%S")
                expTime_dt = datetime.strptime(expTime, "%H:%M:%S")
                expTime_dt = expTime_dt.replace(
                    year=actualTime_dt.year,
                    month=actualTime_dt.month,
                    day=actualTime_dt.day,
                )

            except (KeyError, ValueError):
                continue

            time_diff = actualTime_dt - expTime_dt
            seconds = time_diff.total_seconds()
            if 60 < seconds < 3600:
                lateBuses.append(
                    {
                        "Line": bus["Lines"],
                        "Brigade": bus["Brigade"],
                        "VehicleNumber": bus["VehicleNumber"],
                        "Stop": stop["id"],
                        "Expected": expTime_dt.strftime("%H:%M:%S"),
                        "Actual": actualTime_dt.strftime("%H:%M:%S"),
                        "LateMins": np.round(seconds / 60, decimals=2),
                    }
                )
        print(f"Checked {i+1}/{len(stops)} stops for late buses", end="\r")

    return pd.DataFrame(lateBuses)

def mostLateLines(lateBuses: pd.DataFrame) -> pd.DataFrame:
    return lateBuses.groupby("Line").size().nlargest(10)
