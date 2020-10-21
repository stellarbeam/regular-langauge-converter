from graphviz import Digraph
from regular_language_utils import *
from time import sleep


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        return self.stack.pop()

    def empty(self):
        if self.stack.__len__ == 0:
            return True
        else:
            return False

    def top(self):
        return self.stack[-1]


def isOperator(token):
    if token in ['*', '.', '+']:
        return True
    else:
        return False

def isSymbol(token):
    if token.isalnum():
        return True
    else:
        return False

def precedenceOf(op):
    return [ '+', '.', '*'].index(op)


###############################################

# regex = '(0+1)*.1.(0+1).(0+1)'

regex = input("RegEx (you may skip . operator): ")

if regex == '':
    raise IOError('RegEx cannot be empty')

infix_regex = regex[0]
prev = regex[0]
for i in range(1,len(regex)):
    if (isSymbol(regex[i]) and ( isSymbol(prev) or prev == ')' or prev == '*')) or (regex[i] == '(' and isSymbol(prev)):
        infix_regex += '.'
    infix_regex += regex[i]
    prev = regex[i]


infix_regex = '(' + infix_regex + ')'

print('infix regex:', infix_regex)
postfix_regex = ''

stack = Stack()

for token in infix_regex:
    if isSymbol(token):
        postfix_regex += token
    elif isOperator(token):
        while stack.top() != '(' and precedenceOf(stack.top()) >= precedenceOf(token):
            postfix_regex += stack.pop()
        stack.push(token)
    elif token == '(':
        stack.push(token)
    elif token == ')':
        while stack.top() != '(':
            postfix_regex += stack.pop()
        stack.pop()

# print("Postfix regex:", postfix_regex)

stack = Stack()

for token in postfix_regex:
    if isSymbol(token):
        stack.push(token)
    else:
        if token == '*':
            A = stack.pop()
            stack.push( f'(({A})*)' )
        elif token == '.':
            B = stack.pop()
            A = stack.pop()
            stack.push( f'({A}.{B})' )
        elif token == '+':
            B = stack.pop()
            A = stack.pop()
            stack.push( f'({A}+{B})' )

print("Grouped regex:", stack.top())

node_count = 0
dot = Digraph()
dot.graph_attr['rankdir'] = 'LR'
dot.node_attr['shape'] = 'circle'


stack = Stack()

for token in postfix_regex:
    if isSymbol(token):
        symbol = token
        nodes = subgraphForSymbol(dot, symbol, node_count)
        node_count += 2
        stack.push(nodes)
    else:
        if token == '*':
            nodes = stack.pop()
            newNodes = subgraphForClosure(dot, nodes, node_count)
            node_count += 1
            stack.push( newNodes )
        elif token == '.':
            nodes1 = stack.pop()
            nodes0 = stack.pop()
            newNodes = subgraphForConcatenation(dot, nodes0, nodes1)
            stack.push( newNodes )
        elif token == '+':
            nodes1 = stack.pop()
            nodes0 = stack.pop()
            newNodes = subgraphForUnion(dot, nodes0, nodes1, node_count)
            node_count += 2
            stack.push( newNodes )

finalNodes = stack.pop()

dot.node('BEGIN', '', shape='none')
dot.edge('BEGIN', finalNodes[0], label='start')
dot.node(finalNodes[1], shape='doublecircle')

sleep(2)

dot.render(filename='gv_demo.gv', view=True)
