import heapq

graph = {
    "Hyderabad": {
        "Bangalore": 570,
        "Chennai": 625,
        "Mumbai": 710,
        "Pune": 560,
        "Nagpur": 500
    },
    "Bangalore": {
        "Hyderabad": 570,
        "Chennai": 350,
        "Mumbai": 980,
        "Pune": 840
    },
    "Chennai": {
        "Hyderabad": 625,
        "Bangalore": 350,
        "Mumbai": 1330,
        "Pune": 1190
    },
    "Mumbai": {
        "Hyderabad": 710,
        "Bangalore": 980,
        "Chennai": 1330,
        "Pune": 150,
        "Ahmedabad": 530,
        "Nagpur": 800
    },
    "Pune": {
        "Hyderabad": 560,
        "Bangalore": 840,
        "Chennai": 1190,
        "Mumbai": 150,
        "Ahmedabad": 660
    },
    "Nagpur": {
        "Hyderabad": 500,
        "Mumbai": 800,
        "Bhopal": 350,
        "Delhi": 1080
    },
    "Ahmedabad": {
        "Mumbai": 530,
        "Pune": 660,
        "Delhi": 950,
        "Jaipur": 650
    },
    "Delhi": {
        "Ahmedabad": 950,
        "Jaipur": 280,
        "Lucknow": 555,
        "Chandigarh": 245,
        "Nagpur": 1080
    },
    "Jaipur": {
        "Delhi": 280,
        "Ahmedabad": 650,
        "Lucknow": 570
    },
    "Lucknow": {
        "Delhi": 555,
        "Jaipur": 570,
        "Kolkata": 990
    },
    "Chandigarh": {
        "Delhi": 245
    },
    "Bhopal": {
        "Nagpur": 350,
        "Delhi": 750
    },
    "Kolkata": {
        "Lucknow": 990,
        "Bhubaneswar": 440
    },
    "Bhubaneswar": {
        "Kolkata": 440,
        "Chennai": 1200
    }
}


def dijkstra(graph, start):
    distance = {city: float("inf") for city in graph}
    previous = {city: None for city in graph}

    distance[start] = 0
    queue = [(0, start)]

    while queue:
        current_distance, current_city = heapq.heappop(queue)

        if current_distance > distance[current_city]:
            continue

        for city, road_distance in graph[current_city].items():
            new_distance = current_distance + road_distance

            if new_distance < distance[city]:
                distance[city] = new_distance
                previous[city] = current_city
                heapq.heappush(queue, (new_distance, city))

    return distance, previous


def find_path(previous, start, destination):
    path = []
    current = destination

    while current is not None:
        path.append(current)

        if current == start:
            break

        current = previous[current]

    path.reverse()

    if path[0] != start:
        return []

    return path


start_city = input("Enter starting city: ")

if start_city not in graph:
    print("City not found")
else:
    distances, previous = dijkstra(graph, start_city)

    print("\nShortest distances from", start_city)

    for city in graph:
        if distances[city] == float("inf"):
            print(city, ": Not reachable")
        else:
            path = find_path(previous, start_city, city)
            print(
                city,
                ":",
                distances[city],
                "km",
                "|",
                " -> ".join(path)
            )