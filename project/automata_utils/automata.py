from typing import Set
import networkx as nx
from pyformlang.regular_expression import Regex
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)


def regex_to_dfa(regex: str) -> DeterministicFiniteAutomaton:
    enfa = Regex(regex).to_epsilon_nfa()
    dfa = enfa.to_deterministic()
    dfa_min = dfa.minimize()
    return dfa_min


def graph_to_nfa(
    graph: nx.MultiDiGraph,
    start_states: Set[int],
    final_states: Set[int],
) -> NondeterministicFiniteAutomaton:
    nfa = NondeterministicFiniteAutomaton.from_networkx(graph)

    nodes = set(graph.nodes())
    s_states = nodes if len(start_states) == 0 else set(start_states)
    f_states = nodes if len(final_states) == 0 else set(final_states)

    for s in s_states:
        nfa.add_start_state(s)
    for f in f_states:
        nfa.add_final_state(f)

    return nfa
