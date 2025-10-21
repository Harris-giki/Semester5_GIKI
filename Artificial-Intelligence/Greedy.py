import math
import heapq # for priority queue implementation
from matplotlib.pyplot import plt
import networkx as nx

graph = {
    'A': [('B', 8), ('D', 3), ('F', 6)],
    'B': [('A', 8), ('C', 3), ('D', 2)],
    'C': [('B', 3), ('E', 5)],
    'D': [('A', 3), ('B', 2), ('C', 1), ('E', 8), ('G', 7)],
    'E': [('C', 5), ('D', 8), ('I', 5), ('J', 3)],
    'F': [('A', 6), ('G', 1), ('H', 7)],
    'G': [('D', 7), ('F', 1), ('I', 1)],
    'H': [('F', 7), ('I', 2)],
    'I': [('E', 5), ('G', 1), ('H', 2), ('J', 3)],
    'J': [('E', 3), ('I', 3)]
}

coordinates = {
 'A': (0, 0), 'B': (2, 1), 'C': (4, 1), 'D': (1, -2),
 'E': (6, 0), 'F': (-1, -3), 'G': (2, -4), 'H': (0, -6),
 'I': (4, -5), 'J': (7, -3)
}

def heuristic(node, goal):
    x1, y1 = coordinates[node]
    x2, y2 = coordinates[goal]
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def greedy_best_first(graph, start, goal):
    visited = set() # using sets makes the in check very fast with O(1)
    pq = [] # initialize a priority queue
    heapq.heappush(pq, (0, start, [start])) # pushes a tuple into heap # (heauristics, current_node, path)
    while pq:
        _, node, path = heapq.heappop(pq)
        if node is visited:
            continue
        if node == goal:
            return path
        for neighbour, cost in graph[node]:
            if neighbour not in visited:
                h = heuristic(neighbour, goal)
                heapq.heappush(pq, (h, neighbour, path + [neighbour]))
    return None

start, goal = 'A', 'J'

gbfs_path = greedy_best_first(graph, start, goal)

print("Greedy Best-First Path:", gbfs_path)
