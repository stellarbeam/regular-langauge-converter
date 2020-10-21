from graphviz import Digraph
from pprint import pprint
from time import sleep

eps = '𝜀'

##### INPUT #####

Q = [ 'q0', 'q1', 'q2', 'q3']

q0 = 'q0'

alphabet = ['0', '1']

delta = [
    ['q0', '0', 'q1'],
    ['q0', '0', 'q0'],
    ['q0', '1', 'q0'],
    ['q0', '1', 'q2'],
    ['q0', eps, 'q1'],
    ['q0', eps, 'q2'],
    ['q1', '0', 'q3'],
    ['q2', '1', 'q3']
]

F = ['q3']



####### preprocessing of input
delta_dict = {}

for state in Q:
    delta_dict[state] = {}
    for symbol in alphabet:
        delta_dict[state][symbol] = []
    delta_dict[state][eps] = []

for transition in delta:
    x, s, y = transition
    delta_dict[x][s].append(y)

pprint(delta_dict)
print()
# {
#     'A': {
#         '0': ['A', 'B'], 
#         '1': ['A']
#     },
#     'B': {
#         '0': [], 
#         '1': ['C']
#     },
#     'C': {
#         '0': [], 
#         '1': []
#     }
# }

# algorithm

def stringify(state : list):
    return '{' + ','.join(state) + '}'

def ECLOSE(root_enfa_state: str):
    global eclose_dict

    if eclose_dict[root_enfa_state] != None:
        return eclose_dict[root_enfa_state]

    eclose = [root_enfa_state]

    if delta_dict[root_enfa_state][eps] == []:
        eclose_dict[root_enfa_state] = eclose
        return eclose
    else:
        for enfa_state in delta_dict[root_enfa_state][eps]:
            eclose.extend(ECLOSE(enfa_state))
        eclose = sorted(list(set(eclose)))
        eclose_dict[root_enfa_state] = eclose
        return eclose_dict
        
    
eclose_dict = {}
for enfa_state in Q:
    eclose_dict[enfa_state] = None

dot = Digraph()
dot.graph_attr['rankdir'] = 'LR'
dot.node_attr['shape'] = 'circle'


dfa_states = [ECLOSE(q0)]

dfa_delta = []

new_dfa_states = [ECLOSE(q0)]

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

        eclose_union = []
        for state in next_states:
            eclose_union.extend(ECLOSE(state))
        eclose_union = sorted(set(eclose_union))
        dfa_delta.append([current_state, symbol, eclose_union])

        print('Symbol: ', symbol, ' States: ', eclose_union)

        if eclose_union not in dfa_states:
            dfa_states.append(eclose_union)
            new_dfa_states.append(eclose_union)
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
dot.edge('BEGIN', stringify(ECLOSE(q0)), label='start')

for dfa_state in dfa_states:
    for final_state in F:
        if final_state in dfa_state:
            name = stringify(dfa_state)
            dot.node(name, name, shape='doublecircle')

dot.render(filename='gv_dfa.gv', view=True)
