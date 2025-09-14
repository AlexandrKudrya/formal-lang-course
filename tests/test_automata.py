from project.automata_utils import regex_to_dfa, graph_to_nfa
import networkx as nx


def test_regex_to_dfa_single_symbol():
    dfa = regex_to_dfa("a")
    assert dfa.accepts("a")
    assert not dfa.accepts("b")
    assert not dfa.accepts("aa")


def test_regex_to_dfa_union():
    dfa = regex_to_dfa("a|b")
    assert dfa.accepts("a")
    assert dfa.accepts("b")
    assert not dfa.accepts("c")
    assert not dfa.accepts("ab")


def test_regex_to_dfa_star():
    dfa = regex_to_dfa("a*")
    assert dfa.accepts("")
    assert dfa.accepts("a")
    assert dfa.accepts("aaa")
    assert not dfa.accepts("b")


def test_regex_to_dfa_concat():
    dfa = regex_to_dfa("ab")
    assert dfa.accepts(["ab"])  # Если пишем без [] распознает как 2 разных символа
    assert not dfa.accepts("a")
    assert not dfa.accepts("b")


def test_graph_to_nfa_single_edge():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="a")
    nfa = graph_to_nfa(graph, {0}, {1})
    assert nfa.accepts(["a"])
    assert not nfa.accepts(["b"])
    assert not nfa.accepts(["a", "a"])


def test_graph_to_nfa_default_states():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="a")
    nfa = graph_to_nfa(graph, None, None)
    assert nfa.accepts([])
    assert nfa.accepts(["a"])
    assert not nfa.accepts(["b"])


def test_graph_to_nfa_self_loop():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 0, label="a")
    nfa = graph_to_nfa(graph, {0}, {0})
    assert nfa.accepts([])
    assert nfa.accepts(["a"])
    assert nfa.accepts(["a", "a", "a"])
    assert not nfa.accepts(["b"])


def test_graph_to_nfa_multiple_edges():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="b")
    nfa = graph_to_nfa(graph, {0}, {2})
    assert nfa.accepts(["a", "b"])
    assert not nfa.accepts(["a"])
    assert not nfa.accepts(["b"])


def test_graph_to_nfa_custom_start_final():
    graph = nx.MultiDiGraph()
    graph.add_edge(0, 1, label="a")
    graph.add_edge(1, 2, label="b")

    # Старт в 0, финал в 2
    nfa = graph_to_nfa(graph, {0}, {2})
    assert nfa.accepts(["a", "b"])
    assert not nfa.accepts(["a"])
    assert not nfa.accepts(["b"])

    # Старт в 0, финал в 1
    nfa = graph_to_nfa(graph, {0}, {1})
    assert nfa.accepts(["a"])
    assert not nfa.accepts(["a", "b"])
    assert not nfa.accepts(["b"])

    # Старт в 1, финал в 2
    nfa = graph_to_nfa(graph, {1}, {2})
    assert nfa.accepts(["b"])
    assert not nfa.accepts(["a"])
    assert not nfa.accepts(["a", "b"])
