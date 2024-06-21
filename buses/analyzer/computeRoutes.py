def getRoutes(schedules):
    routes = {}

    for stop in schedules:
        for line in schedules[stop]:
            if line not in routes:
                routes[line] = {}
            for entry in schedules[stop][line]:
                if entry["brygada"] not in routes[line]:
                    routes[line][entry["brygada"]] = {}
                routes[line][entry["brygada"]][stop] = entry["czas"]

    return routes
