from collections import deque
from graphviz import Digraph

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
        
    def visualize(self, filename='nfa'):
        """将NFA可视化为图形"""
        dot = Digraph(comment='NFA Visualization')
        dot.attr(rankdir='LR')  # 从左到右的布局
        
        # 添加开始状态标记
        dot.node('start', '', shape='point')
        dot.edge('start', str(self.start_state))
        
        # 添加所有状态
        for state in self.transitions.keys():
            if state in self.accept_states:
                dot.node(str(state), str(state), shape='doublecircle')
            else:
                dot.node(str(state), str(state), shape='circle')
        
        # 添加转换边
        for state, trans in self.transitions.items():
            for symbol, targets in trans.items():
                for target in targets:
                    dot.edge(str(state), str(target), label=str(symbol))
        
        dot.render(filename, view=True, format='png')

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
        self.start_state = None  # 改为整数类型
        self.alphabet = alphabet - {'ε'} if isinstance(alphabet, set) else set(alphabet)
        self.transitions = {}    # {state: {symbol: next_state}}
        self.accept_states = set()
        
    def visualize(self, filename='dfa'):
        """将DFA可视化为图形"""
        dot = Digraph(comment='DFA Visualization')
        dot.attr(rankdir='LR')
        
        # 添加开始状态标记
        dot.node('start', '', shape='point')
        dot.edge('start', str(self.start_state))
        
        # 添加所有状态
        all_states = set(self.transitions.keys())
        for target_dict in self.transitions.values():
            for target in target_dict.values():
                all_states.add(target)
        
        for state in all_states:
            if state in self.accept_states:
                dot.node(str(state), str(state), shape='doublecircle')
            else:
                dot.node(str(state), str(state), shape='circle')
        
        # 添加转换边
        for state, trans in self.transitions.items():
            for symbol, target in trans.items():
                dot.edge(str(state), str(target), label=str(symbol))
        
        dot.render(filename, view=True, format='png')

def epsilon_closure(nfa, states):   
    """
    ε-闭包计算：
    1. 输入一个状态集合
    2. 通过深度优先搜索找到所有通过ε转换可达的状态
    3. 返回包含所有可达状态的集合
    """
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
    """
    move函数实现：
    1. 输入一个状态集合和一个输入符号
    2. 找出从这些状态通过该输入符号可以到达的所有状态
    3. 返回目标状态的集合
    """
    next_states = set()
    for state in states:
        if symbol in nfa.transitions[state]:
            next_states.update(nfa.transitions[state][symbol])
            
    return next_states


def subset_construction(nfa):
    """
    子集构造：
    1. 计算起始状态的ε-闭包作为DFA的起始状态
    2. 使用队列处理未处理的状态
    3. 对每个状态和每个输入符号：
    - 计算move后的状态集合
    - 计算该集合的ε-闭包
    - 将新状态加入DFA
    4. 确定接受状态：如果DFA的某个状态集合包含NFA的接受状态，则该状态为接受状态
    """
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
    
# 示例代码部分修改为：
if __name__ == "__main__":
    # 示例 NFA 定义
    nfa_transitions = {
        'q0': {'a': ['q1'], 'ε': ['q2']},
        'q1': {'b': ['q1'], 'ε': ['q3']},
        'q2': {'c': ['q2'], 'ε': ['q3']},
        'q3': {}
    }
    nfa_alphabet = {'a', 'b', 'c', 'ε'}
    nfa = NFA(start_state='q0', accept_states={'q3'}, 
              transitions=nfa_transitions, alphabet=nfa_alphabet)
    
    # 生成NFA的图形
    nfa.visualize('nfa_example')
    
    # 转换为DFA
    dfa = subset_construction(nfa)
    
    # 生成DFA的图形
    dfa.visualize('dfa_example')
    
    # 输出 DFA 结果
    print("DFA Start State:", dfa.start_state)
    print("DFA Accept States:", dfa.accept_states)
    print("DFA Transitions:")
    for state, transitions in dfa.transitions.items():
        for symbol, next_state in transitions.items():
            print(f"{state} --{symbol}--> {next_state}")