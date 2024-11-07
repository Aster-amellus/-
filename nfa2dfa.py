from collections import deque


class NFA:
    def __init__(self, start_state, alphabet, transitions, accept_states):
        """
        NFA类的构造函数
        :param start_state: 起始状态号
        :param alphabet: 字母表集合，包含所有可能的输入符号
        :param transitions: 转换函数，格式为：
            {当前状态: {输入符号: {目标状态集合}}}
            其中输入符号可以是None，表示ε转换(不需要输入即可转换)
        :param accept_states: 接受状态集合
        """
        self.start_state = start_state
        self.alphabet = alphabet
        self.transitions = transitions
        self.accept_states = accept_states
        
class DFA:
    def __init__(self, alphabet):
        """
        DFA类的构造函数
        :param start_state: 起始状态号
        :param alphabet: 字母表集合，包含所有可能的输入符号
        :param transitions: 转换函数，格式为：
            {当前状态: {输入符号: 目标状态}}
        :param accept_states: 接受状态集合
        """
        self.start_state = None
        self.alphabet = alphabet - {'ε'}
        self.transitions = {}
        self.accept_states = set()
        
def epsilon_closure(nfa, states):
    """计算NFA状态集合的ε闭包"""
    closure = set(states)
    stack = list(states)
    
    while stack:
        current_state = stack.pop()
        if 'ε' in nfa.transitions[current_state]:
            for state in nfa.transitions[current_state]['ε']:
                if state not in closure:
                    closure.add(state)
                    stack.append(state)
                
    return closure

def move(nfa, states, symbol):
    next_states = set()
    for state in states:
        if symbol in nfa.transitions[state]:
            next_states.update(nfa.transitions[state][symbol])
            
    return next_states

def subset_construction(nfa):
    dfa = DFA(nfa.alphabet)
    start_closure = frozenset(epsilon_closure(nfa, {nfa.start_state}))
    dfa.start_state = start_closure
    
    unprocessed_states = deque([start_closure])
    dfa.transitions = {}
    dfa_states = {start_closure}  # 使用set存储已处理的状态
    
    while unprocessed_states:
        current_state = unprocessed_states.popleft()
        
        for symbol in nfa.alphabet - {'ε'}:  # 排除ε转换
            next_states = frozenset(epsilon_closure(nfa, move(nfa, current_state, symbol)))
            
            if next_states and next_states not in dfa_states:
                unprocessed_states.append(next_states)
                dfa_states.add(next_states)
            
            if current_state not in dfa.transitions:
                dfa.transitions[current_state] = {}
                
            if next_states:  # 只添加非空的转换
                dfa.transitions[current_state][symbol] = next_states
    
    # 修复接受状态的判断逻辑
    for state in dfa_states:
        if state & nfa.accept_states:  # 使用集合交集运算
            dfa.accept_states.add(state)
            
    return dfa
    
# 示例 NFA 定义
nfa_transitions = {
    'q0': {'a': ['q1'], 'ε': ['q2']},
    'q1': {'b': ['q1'], 'ε': ['q3']},
    'q2': {'c': ['q2'], 'ε': ['q3']},
    'q3': {}
}
nfa_alphabet = {'a', 'b', 'c', 'ε'}
nfa = NFA(start_state='q0', accept_states={'q3'}, transitions=nfa_transitions, alphabet=nfa_alphabet)

# 运行子集构造法
dfa = subset_construction(nfa)

# 输出 DFA 结果
print("DFA Start State:", dfa.start_state)
print("DFA Accept States:", dfa.accept_states)
print("DFA Transitions:")
for state, transitions in dfa.transitions.items():
    for symbol, next_state in transitions.items():
        print(f"{state} --{symbol}--> {next_state}")