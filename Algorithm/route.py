from dataclasses import dataclass

@dataclass
class Route:
    position: list = None
    route: list = None
    distance: float = -1
    possible: bool = True
