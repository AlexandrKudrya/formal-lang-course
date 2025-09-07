import os
import pathlib
import uuid

import pydot
import pytest

from project.graph_utils import get_graph_info, two_cycles_to_dot, GraphInfo
from test_utils import parse_labels_from_dot

BZIP_GRAPH = GraphInfo(
    nodes=632,
    edges=556,
    labels={"a", "d"}
)

@pytest.mark.network
def test_get_graph_info_bzip_exact():
    info = get_graph_info("bzip")

    assert isinstance(info, GraphInfo)
    assert info.nodes == BZIP_GRAPH.nodes
    assert info.edges == BZIP_GRAPH.edges
    assert info.labels == BZIP_GRAPH.labels


def test_two_cycles_basic_dot_valid(tmp_path: pathlib.Path):
    out = tmp_path / "two_cycles.dot"
    path = two_cycles_to_dot(3, 4, label_left="x", label_right="y", out_dot_path=out)

    assert os.path.exists(path)
    labels = parse_labels_from_dot(out)
    assert {"x", "y"}.issubset(labels)


def test_two_cycles_pathlike_and_common_node(tmp_path: pathlib.Path):
    out = tmp_path / "by_path_obj.dot"
    common = 42

    result = two_cycles_to_dot(2, 2, out_dot_path=out, common_node=common)
    assert pathlib.Path(result).resolve() == out.resolve()
    assert out.exists()

    graphs = pydot.graph_from_dot_file(str(out))
    g = graphs[0]
    node_names = {n.get_name().strip('"') for n in g.get_nodes()}
    assert str(common) in node_names, "No common node found"


def test_two_cycles_invalid_sizes_raise(tmp_path: pathlib.Path):
    out = tmp_path / "bad.dot"
    with pytest.raises(Exception):
        two_cycles_to_dot(0, 3, out_dot_path=out)
    with pytest.raises(Exception):
        two_cycles_to_dot(3, 0, out_dot_path=out)
    with pytest.raises(Exception):
        two_cycles_to_dot(-1, 2, out_dot_path=out)
