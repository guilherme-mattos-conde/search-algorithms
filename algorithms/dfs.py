from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]
        visited = {initial}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            current = frontier.pop()

            if current.is_goal:
                return SearchResult(
                    current, nodes_expanded, nodes_generated,
                    max_frontier_size, len(current.path()) - 1
                )

            if len(current.path()) - 1 >= self.depth_limit:
                continue

            nodes_expanded += 1
            
            for child in reversed(current.neighbors()):
                if child not in visited:
                    visited.add(child)
                    frontier.append(child)
                    nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier_size)
