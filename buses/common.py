import pandas as pd
import numpy as np
import glob
import json
import requests

MAXSPEED = 100
SPEEDLIMIT = 50
PROXIMITY = 100

WARSAW = [52.2297, 21.0122]

APIKEY = "a2f2f335-31bf-490c-8765-186a3a1e7a92"
# 839623cd-47ae-4436-af23-299347f6c218


# Haversine formula to calculate the distance between two points in meters
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1, phi2 = np.radians(lat1), np.radians(lat2)
    d_phi = np.radians(lat2 - lat1)
    d_lambda = np.radians(lon2 - lon1)
    a = np.sin(d_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(d_lambda / 2) ** 2
    c = 2 * np.atan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c

    return distance


def getDistance(lat1, lon1, lat2, lon2):
    # Ensure inputs are numpy arrays
    if np.isscalar(lat1):
        lat1 = np.array([lat1])
    if np.isscalar(lon1):
        lon1 = np.array([lon1])
    if np.isscalar(lat2):
        lat2 = np.array([lat2])
    if np.isscalar(lon2):
        lon2 = np.array([lon2])

    distances = haversine(lat1, lon1, lat2, lon2)

    # Return scalar if inputs were scalars
    if distances.size == 1:
        return distances.item()

    return distances


def isClose(lat1, lon1, lat2, lon2):
    distances = getDistance(lat1, lon1, lat2, lon2)
    return distances < PROXIMITY


def sanitizeDict(d):
    res = {}
    for item in d["values"]:
        if item["value"] and item["value"] != "null":
            res[item["key"]] = item["value"]

    return res


def getFromApi(url, params):
    while True:
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()

            data = response.json()["result"]
            if not isinstance(data, list):
                raise Exception(data)

            return data

        except Exception as e:
            print(f"Error occurred: {e}, retrying...")


def readJson(filename):
    files = glob.glob(filename)

    if not files:
        raise FileNotFoundError()

    print("Reading from", files[0])
    with open(files[0], "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


def writeJson(data, filename):
    print("Writing to", filename)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def readCsv(filename):
    files = glob.glob(filename)

    if not files:
        raise FileNotFoundError()

    print("Reading from", files[0])
    return pd.read_csv(files[0])


def writeCsv(data, filename):
    print("Writing to", filename)
    data.to_csv(filename, index=False)
