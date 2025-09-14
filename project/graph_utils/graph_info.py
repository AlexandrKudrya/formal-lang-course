from dataclasses import dataclass

@dataclass(frozen=True)
class GraphInfo:
    nodes: int
    edges: int
    labels: set[str]
