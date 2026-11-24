import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        distance = 0

        for index, tile in enumerate(state.tiles):
            if tile != 0:
                goal_index = tile - 1
                current_row, current_col = divmod(index, 3)
                goal_row, goal_col = divmod(goal_index, 3)
                distance += abs(current_row - goal_row) + abs(current_col - goal_col)

        return distance

    def search(self, initial: State) -> SearchResult:
        sequence = count()
        frontier = [(self.heuristic(initial), next(sequence), initial)]
        best_cost = {initial: 0}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, _, current = heapq.heappop(frontier)
            
            if current.cost != best_cost.get(current):
                continue

            if current.is_goal:
                return SearchResult(
                    current, nodes_expanded, nodes_generated,
                    max_frontier_size, len(current.path()) - 1
                )

            nodes_expanded += 1

            for child in current.neighbors():
                if child.cost < best_cost.get(child, float("inf")):
                    best_cost[child] = child.cost
                    priority = child.cost + self.heuristic(child)
                    heapq.heappush(frontier, (priority, next(sequence), child))
                    nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)
