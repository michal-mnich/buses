import requests_mock
from buses.common import getFromApi, getDistance
import random
import numpy as np
from geopy.distance import great_circle


def mockLocations():
    with requests_mock.Mocker() as mocker:
        url = "https://api.um.warszawa.pl/api/action/busestrams_get"

        response_data = {
            "result": [
                {
                    "Lines": "219",
                    "Lon": 21.166556,
                    "VehicleNumber": "1000",
                    "Time": "2024-01-21 17:35:12",
                    "Lat": 52.194781,
                    "Brigade": "3",
                },
                {
                    "Lines": "225",
                    "Lon": 21.1366691,
                    "VehicleNumber": "1001",
                    "Time": "2024-01-21 17:35:14",
                    "Lat": 52.2594978,
                    "Brigade": "04",
                },
            ]
        }

        mocker.get(url, json=response_data)
        data = getFromApi(url, params=None)

        assert len(data) == 2
        assert data[0]["Lines"] == "219"
        assert data[1]["Lon"] == 21.1366691
        assert data[0]["VehicleNumber"] == "1000"
        assert data[1]["Time"] == "2024-01-21 17:35:14"
        assert data[0]["Lat"] == 52.194781
        assert data[1]["Brigade"] == "04"


def testGetDistance():
    def generate_random_coordinates(num_coordinates):
        lats = []
        lons = []
        for _ in range(num_coordinates):
            lon = random.uniform(21, 22)
            lat = random.uniform(52, 53)
            lats.append(lat)
            lons.append(lon)
        return (np.array(lats), np.array(lons))

    lats1, lons1 = generate_random_coordinates(100)
    lats2, lons2 = generate_random_coordinates(100)

    # Sequential computation
    results_sequential = []
    for lat1, lon1, lat2, lon2 in zip(lats1, lons1, lats2, lons2):
        distance = getDistance(lat1, lon1, lat2, lon2)
        assert distance >= 0
        # Check consistency with external library
        assert np.abs(distance - great_circle((lat1, lon1), (lat2, lon2)).meters) < 1
        results_sequential.append(distance)

    # Vectorized computation
    results_vectorized = getDistance(lats1, lons1, lats2, lons2)

    # Should be the same thing
    assert len(results_sequential) == len(results_vectorized)
    for distance1, distance2 in zip(results_sequential, results_vectorized):
        assert distance1 == distance2


def main():
    mockLocations()
    testGetDistance()


if __name__ == "__main__":
    main()
