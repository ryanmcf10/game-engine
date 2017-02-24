import env.tools.grid as grid
import heapq


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b

    return abs(x1-x2) + abs(y1-y2)

def a_star_search(graph, start, goal):
    frontier = PriorityQueue()

    frontier.put(start, 0)

    came_from = {}
    cost_so_far = {}

    came_from[start] = None
    cost_so_far[start] = None

    while not frontier.empty():
        current = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current
        
    return came_from, cost_so_far
    

class WeightedGraph:
    def __init__(self, grid):
        self.width = grid.num_cols
        self.height = grid.num_rows
        self.data = grid.grid_data
        self.blockers = self._build_blockers()
        self.weights = self._build_weights()

    def _build_blockers(self):
        blockers = []
        for row in range(len(self.data)):
            for col in range(len(self.data[row])):
                if self.data[row][col].value != 0:
                    blockers.append((row, col))

        return blockers

    def _build_weights(self):
        weights = {}
        for row in range(len(self.data)):
            for col in range(len(self.data[row])):
                value = self.data[row][col].value
                if value != 0:
                    weights[(row,col)] = self.data[row][col].value

        return weights

    def in_bounds(self, id):
        (x,y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.blockers

    def neighbors(self, id):
        (x,y) = id
        results = [(x+1,y),(x,y-1),(x-1,y),(x,y+1)]
        if (x + y) % 2 == 0:
            results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]
