import random
import heapq
import matplotlib.pyplot as plt


SIZE = 70


def create_grid(density, start, goal):
    grid = []

    for i in range(SIZE):
        row = []

        for j in range(SIZE):
            if (i, j) == start or (i, j) == goal:
                row.append(0)
            else:
                row.append(1 if random.random() < density else 0)

        grid.append(row)

    return grid


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def get_neighbors(node, grid):
    x, y = node

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    neighbors = []

    for dx, dy in directions:
        nx = x + dx
        ny = y + dy

        if 0 <= nx < SIZE and 0 <= ny < SIZE:
            if grid[nx][ny] == 0:
                neighbors.append((nx, ny))

    return neighbors


def a_star(grid, start, goal):
    queue = [(heuristic(start, goal), 0, start)]

    came_from = {}
    cost = {start: 0}

    nodes_expanded = 0

    while queue:
        _, current_cost, current = heapq.heappop(queue)

        nodes_expanded += 1

        if current == goal:
            path = []

            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.append(start)
            path.reverse()

            return path, nodes_expanded

        for neighbor in get_neighbors(current, grid):
            new_cost = cost[current] + 1

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                came_from[neighbor] = current

                priority = new_cost + heuristic(neighbor, goal)

                heapq.heappush(
                    queue,
                    (priority, new_cost, neighbor)
                )

    return None, nodes_expanded


def display_path(grid, path, start, goal):
    plt.figure(figsize=(8, 8))
    plt.imshow(grid, cmap="gray_r")

    if path:
        x = [point[1] for point in path]
        y = [point[0] for point in path]
        plt.plot(x, y, linewidth=2)

    plt.scatter(
        start[1],
        start[0],
        marker="o",
        s=100,
        label="Start"
    )

    plt.scatter(
        goal[1],
        goal[0],
        marker="x",
        s=100,
        label="Goal"
    )

    plt.title("UGV Path using A*")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.legend()
    plt.show()


start = tuple(map(int, input(
    "Enter start coordinates (row col): "
).split()))

goal = tuple(map(int, input(
    "Enter goal coordinates (row col): "
).split()))

print("\n1. Low density")
print("2. Medium density")
print("3. High density")

choice = int(input("Select obstacle density: "))

density = {
    1: 0.20,
    2: 0.35,
    3: 0.50
}.get(choice, 0.20)

grid = create_grid(density, start, goal)

path, nodes = a_star(grid, start, goal)

if path:
    print("\nPath found")
    print("Path length:", len(path) - 1)
    print("Nodes expanded:", nodes)
    print("Number of positions:", len(path))
    print("Path:")
    print(path)

    display_path(grid, path, start, goal)

else:
    print("\nNo path could be found.")
    print("Nodes expanded:", nodes)