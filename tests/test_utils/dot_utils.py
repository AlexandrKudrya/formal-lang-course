import pathlib
import pydot


def parse_labels_from_dot(dot_path: pathlib.Path) -> set[str]:
    graphs = pydot.graph_from_dot_file(str(dot_path))
    assert graphs and len(graphs) >= 1, "pydot can't parse DOT"
    g = graphs[0]
    edges = g.get_edges()
    assert edges, "No edges found"
    labels = {e.get("label") for e in edges if e.get("label") is not None}
    return {s.strip('"') for s in labels}
