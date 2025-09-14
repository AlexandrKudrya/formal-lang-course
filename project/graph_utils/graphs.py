from __future__ import annotations

from typing import Iterable, Any, Set
import os
import cfpq_data
import networkx as nx

from .graph_info import GraphInfo


def get_graph_info(name: str) -> GraphInfo:
    """
    Load a graph from the CFPQ_Data collection by its name and return
    basic information about it.

    :param name: Name of the graph in the CFPQ_Data dataset
    :return: A dictionary with the following keys:
             - ``nodes``: number of nodes (``int``)
             - ``edges``: number of edges (``int``)
             - ``labels``: set of unique edge labels (``set[str]``)
    """
    path = cfpq_data.download(name)
    graph = cfpq_data.graph_from_csv(path)

    labels: Set[str] = set()
    for _, _, data in graph.edges(data=True):
        lbl = data.get("label")
        if lbl is not None:
            labels.add(str(lbl))

    return GraphInfo(
        nodes=graph.number_of_nodes(),
        edges=graph.number_of_edges(),
        labels=labels,
    )


def two_cycles_to_dot(
    n: int | Iterable[Any],
    m: int | Iterable[Any],
    label_left: str = "a",
    label_right: str = "b",
    out_dot_path: str | os.PathLike = "two_cycles.dot",
    common_node: int | Any = 0,
) -> str:
    """
    Build a labeled graph consisting of two cycles sharing a common node
    and save it to a DOT file.

    :param n: Number of nodes in the first cycle (excluding the common node).
    :param m: Number of nodes in the second cycle (excluding the common node).
    :param label_left: Label for edges in the first cycle.
    :param label_right: Label for edges in the second cycle.
    :param out_dot_path: Path to the output DOT file. Will be overwritten if it exists.
    :param common_node: The node index that connects both cycles.
    :return: The file path (as string) to the saved DOT file.
    """
    graph = cfpq_data.labeled_two_cycles_graph(
        n, m, common_node=common_node, labels=(label_left, label_right)
    )
    nx.nx_pydot.write_dot(graph, out_dot_path)
    return out_dot_path
