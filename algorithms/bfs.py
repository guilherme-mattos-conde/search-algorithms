from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        frontier = deque([initial])
        visited = {initial}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            current = frontier.popleft()

            if current.is_goal:
                return SearchResult(
                    current, nodes_expanded, nodes_generated,
                    max_frontier_size, len(current.path()) - 1
                )

            nodes_expanded += 1

            for child in current.neighbors():
                if child not in visited:
                    visited.add(child)
                    frontier.append(child)
                    nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)
