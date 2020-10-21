from graphviz import Digraph
from pprint import pprint

##### INPUT #####

# Q = [ 'A', 'B', 'C']

# q0 = 'A'

# alphabet = ['0', '1']

# delta = [
#     ['A', '0', 'A'],
#     ['A', '1', 'A'],
#     ['A', '0', 'B'],
#     ['B', '1', 'C']
# ]

# F = ['C']

################

Q = ['A', 'B', 'C', 'D']

q0 = 'A'

alphabet = ['0', '1']

delta = [
    ['A', '0', 'A'],
    ['A', '1', 'B'],
    ['A', '1', 'A'],
    ['B', '0', 'C'],
    ['B', '1', 'C'],
    ['C', '0', 'D'],
    ['C', '1', 'D'],
]

F = [ 'D' ]

####### preprocessing of input
delta_dict = {}

for state in Q:
    delta_dict[state] = {}
    for symbol in alphabet:
        delta_dict[state][symbol] = []

for transition in delta:
    x, s, y = transition
    delta_dict[x][s].append(y)

pprint(delta_dict)
print()


# algorithm

def stringify(state : list):
    return '{' + ','.join(state) + '}'

dot = Digraph()
dot.graph_attr['rankdir'] = 'LR'
dot.node_attr['shape'] = 'circle'


dfa_states = [[q0]]

dfa_delta = []

new_dfa_states = [[q0]]

while len(new_dfa_states) > 0:
    current_state = new_dfa_states[0]
    new_dfa_states = new_dfa_states[1:]

    print('Current state: ', current_state)

    for symbol in alphabet:
        next_states = []
        for nfa_state in current_state:
            for x in delta_dict[nfa_state][symbol]:
                if x not in next_states:
                    next_states.append(x)
        next_states = sorted(next_states)
        dfa_delta.append([current_state, symbol, next_states])
        print('Symbol: ', symbol, ' States: ', next_states)

        if next_states not in dfa_states:
            dfa_states.append(next_states)
            new_dfa_states.append(next_states)
    print()

print('dfa_states', dfa_states)
print()

print('dfa_delta')
pprint(dfa_delta)

for state in dfa_states:
    name = stringify(state)
    dot.node(name, name)

for transition in dfa_delta:
    x, s, y = transition
    nameX = stringify(x)
    nameY = stringify(y)
    dot.edge(nameX, nameY, label=s)

dot.node('BEGIN', '', shape='none')
dot.edge('BEGIN', stringify([q0]), label='start')

for dfa_state in dfa_states:
    for final_state in F:
        if final_state in dfa_state:
            name = stringify(dfa_state)
            dot.node(name, name, shape='doublecircle')

dot.render(filename='gv_dfa.gv', view=True)
