import random
import heapq
import matplotlib.pyplot as plt


SIZE = 30


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

    while queue:
        _, current_cost, current = heapq.heappop(queue)

        if current == goal:
            path = []

            while current in came_from:
                path.append(current)
                current = came_from[current]

            path.append(start)
            path.reverse()

            return path

        for neighbor in get_neighbors(current, grid):
            new_cost = cost[current] + 1

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                came_from[neighbor] = current

                priority = new_cost + heuristic(
                    neighbor,
                    goal
                )

                heapq.heappush(
                    queue,
                    (priority, new_cost, neighbor)
                )

    return None


def create_grid():
    grid = []

    for i in range(SIZE):
        row = []

        for j in range(SIZE):
            if random.random() < 0.20:
                row.append(1)
            else:
                row.append(0)

        grid.append(row)

    return grid


def move_obstacle(grid, obstacle, start, goal):
    x, y = obstacle

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    random.shuffle(directions)

    for dx, dy in directions:
        nx = x + dx
        ny = y + dy

        if 0 <= nx < SIZE and 0 <= ny < SIZE:

            if (
                grid[nx][ny] == 0
                and (nx, ny) != start
                and (nx, ny) != goal
            ):
                grid[x][y] = 0
                grid[nx][ny] = 1

                return (nx, ny)

    return obstacle


def show_grid(grid, path, start, goal):
    plt.figure(figsize=(8, 8))

    plt.imshow(grid, cmap="gray_r")

    if path:
        x = [p[1] for p in path]
        y = [p[0] for p in path]

        plt.plot(x, y, linewidth=2)

    plt.scatter(
        start[1],
        start[0],
        s=100,
        marker="o",
        label="Start"
    )

    plt.scatter(
        goal[1],
        goal[0],
        s=100,
        marker="x",
        label="Goal"
    )

    plt.title("UGV Dynamic Obstacle Navigation")
    plt.legend()
    plt.show()


start = (0, 0)
goal = (SIZE - 1, SIZE - 1)

grid = create_grid()

grid[start[0]][start[1]] = 0
grid[goal[0]][goal[1]] = 0

obstacle = (15, 15)

grid[obstacle[0]][obstacle[1]] = 1

current = start
total_steps = 0
replans = 0
visited = [current]

while current != goal:

    path = a_star(grid, current, goal)

    if path is None:
        print("No path available.")
        break

    replans += 1

    if len(path) > 1:
        next_position = path[1]
    else:
        next_position = goal

    current = next_position
    visited.append(current)
    total_steps += 1

    if current == goal:
        break

    obstacle = move_obstacle(
        grid,
        obstacle,
        current,
        goal
    )

    if total_steps > 500:
        print("Maximum steps reached.")
        break


if current == goal:
    print("UGV reached the goal.")
    print("Total steps:", total_steps)
    print("Number of replanning operations:", replans)

    show_grid(
        grid,
        visited,
        start,
        goal
    )
else:
    print("UGV could not reach the goal.")