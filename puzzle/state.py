from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como uma tupla de 9 números (0 = vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        index = self.blank_index
        row, col = divmod(index, 3)
        moves = []
        
        if row > 0:
            moves.append(("UP", index - 3))
        if row < 2:
            moves.append(("DOWN", index + 3))
        if col > 0:
            moves.append(("LEFT", index - 1))
        if col < 2:
            moves.append(("RIGHT", index + 1))

        children = []
        for action, new_index in moves:
            new_tiles = list(self.tiles)
            new_tiles[index], new_tiles[new_index] = new_tiles[new_index], new_tiles[index]
            children.append(State(tuple(new_tiles), self, action, self.cost + 1))

        return children

    def path(self) -> List["State"]:
        """Reconstrói o caminho desde o estado inicial até este estado."""
        states = []
        current = self

        while current is not None:
            states.append(current)
            current = current.parent

        states.reverse()
        return states

    def actions(self) -> List[str]:
        """Retorna os movimentos realizados para chegar a este estado."""
        return [state.action for state in self.path()[1:]]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
