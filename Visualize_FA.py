from re2nfa import *
from nfa2dfa import *


from graphviz import Digraph

def visualize_nfa(nfa, filename='nfa'):
    dot = Digraph(comment='NFA')
    
    # 添加状态节点
    for state in nfa.transitions:
        if state in nfa.accept_states:
            dot.node(str(state), shape='doublecircle')
        else:
            dot.node(str(state), shape='circle')
    
    # 添加转换边
    for state, transitions in nfa.transitions.items():
        for symbol, next_states in transitions.items():
            for next_state in next_states:
                if symbol is None:
                    label = 'ε'
                else:
                    label = symbol
                dot.edge(str(state), str(next_state), label=label)
    
    # 标记起始状态
    dot.node('', shape='none', width='0', height='0')
    dot.edge('', str(nfa.start_state))
    
    # 保存并渲染图像
    dot.render(filename, format='png', cleanup=True)

# 示例用法
if __name__ == "__main__":
    # 创建一个简单的NFA进行测试
    transitions = {
        0: {'a': {1}},
        1: {'b': {2}},
        2: {'c': {0}}
    }
    re = "ab*|c"
    nfa = postfix_to_nfa(regex_to_postfix(re))
    dfa = subset_construction(nfa)
    visualize_nfa(nfa, 'example_nfa')
    visualize_nfa(dfa, 'example_dfa')
