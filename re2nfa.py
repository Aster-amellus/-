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
        alphabet.discard('ε')  # 移除'ε'符号
        self.alphabet = alphabet
        self.transitions = transitions
        self.accept_states = accept_states
    
    def accepts(self, string):
        # 初始化当前状态集为 ε-闭包
        current_states = self._epsilon_closure({self.start_state})
        
        for char in string:
            next_states = set()
            for state in current_states:
                if char in self.transitions.get(state, {}):
                    next_states.update(self.transitions[state][char])
            current_states = self._epsilon_closure(next_states)
        
        return any(state in self.accept_states for state in current_states)
    
    def _epsilon_closure(self, states):
        stack = list(states)
        closure = set(states)
        
        while stack:
            state = stack.pop()
            for next_state in self.transitions.get(state, {}).get(None, set()):
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        
        return closure

def regex_to_postfix(regex):
    # 首先处理隐式连接，插入.运算符
    output = []
    for i in range(len(regex)):
        output.append(regex[i])
        if i + 1 < len(regex):
            # 在以下情况中插入连接运算符
            if (regex[i].isalnum() and regex[i+1].isalnum() or
                regex[i].isalnum() and regex[i+1] == '(' or
                regex[i] == '*' and regex[i+1].isalnum() or
                regex[i] == '*' and regex[i+1] == '(' or
                regex[i] == ')' and regex[i+1].isalnum() or
                regex[i] == ')' and regex[i+1] == '('):
                output.append('.')
    regex = ''.join(output)
    
    # 转换为后缀表达式
    postfix = []
    stack = []
    precedence = {'*': 3, '.': 2, '|': 1}
    
    for c in regex:
        if c.isalnum():
            postfix.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            if stack:
                stack.pop()  # 弹出'('
        else:
            while stack and stack[-1] != '(' and precedence.get(c, 0) <= precedence.get(stack[-1], 0):
                postfix.append(stack.pop())
            stack.append(c)
    
    while stack:
        if stack[-1] != '(':
            postfix.append(stack.pop())
        else:
            stack.pop()
            
    return ''.join(postfix)

def postfix_to_nfa(postfix):
    stack = []
    state_counter = 0
    
    for char in postfix:
        if char.isalnum():
            transitions = {
                state_counter: {char: {state_counter + 1}},
                state_counter + 1: {}  # 确保每个状态都有转换表项
            }
            nfa = NFA(state_counter, {char}, transitions, {state_counter + 1})
            state_counter += 2
            stack.append((nfa, state_counter))
            
        elif char == '*':
            nfa, counter = stack.pop()
            new_start = counter
            new_accept = counter + 1
            
            new_transitions = {**nfa.transitions}
            new_transitions[new_start] = {None: {nfa.start_state, new_accept}}
            new_transitions[new_accept] = {}  # 新接受状态的转换表项
            
            for accept in nfa.accept_states:
                if accept not in new_transitions:
                    new_transitions[accept] = {}
                new_transitions[accept].setdefault(None, set()).update({nfa.start_state, new_accept})
            
            nfa = NFA(new_start, nfa.alphabet, new_transitions, {new_accept})
            state_counter = counter + 2
            stack.append((nfa, state_counter))
            
        elif char == '.':
            nfa2, counter2 = stack.pop()
            nfa1, counter1 = stack.pop()
            
            new_transitions = {**nfa1.transitions, **nfa2.transitions}
            
            for accept in nfa1.accept_states:
                new_transitions.setdefault(accept, {}).setdefault(None, set()).add(nfa2.start_state)
            
            new_alphabet = nfa1.alphabet | nfa2.alphabet
            nfa = NFA(nfa1.start_state, new_alphabet, new_transitions, nfa2.accept_states)
            state_counter = max(counter1, counter2)
            stack.append((nfa, state_counter))
            
        elif char == '|':
            nfa2, counter2 = stack.pop()
            nfa1, counter1 = stack.pop()
            new_start = state_counter
            new_accept = state_counter + 1
            
            new_transitions = {**nfa1.transitions, **nfa2.transitions}
            new_transitions[new_start] = {None: {nfa1.start_state, nfa2.start_state}}
            new_transitions[new_accept] = {}  # 新接受状态的转换表项
            
            for accept in nfa1.accept_states | nfa2.accept_states:
                new_transitions.setdefault(accept, {}).setdefault(None, set()).add(new_accept)
            
            new_alphabet = nfa1.alphabet | nfa2.alphabet
            nfa = NFA(new_start, new_alphabet, new_transitions, {new_accept})
            state_counter += 2
            stack.append((nfa, state_counter))
    
    final_nfa, _ = stack.pop()
    return final_nfa

