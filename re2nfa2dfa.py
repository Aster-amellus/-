from re2nfa import regex_to_postfix, postfix_to_nfa
from nfa2dfa import subset_construction

def regex_to_dfa(regex):
    """将正则表达式转换为DFA"""
    # 第一步：将正则表达式转换为后缀表达式
    postfix = regex_to_postfix(regex)
    print(f"后缀表达式: {postfix}")
    
    # 第二步：将后缀表达式转换为NFA
    nfa = postfix_to_nfa(postfix)
    print("\nNFA转换完成:")
    print(f"起始状态: {nfa.start_state}")
    print(f"接受状态: {nfa.accept_states}")
    print("NFA转换函数:")
    for state, trans in nfa.transitions.items():
        for symbol, next_states in trans.items():
            symbol = 'ε' if symbol is None else symbol
            print(f"{state} --{symbol}--> {next_states}")
    
    # 第三步：将NFA转换为DFA
    dfa = subset_construction(nfa)
    print("\nDFA转换完成:")
    print(f"起始状态: {dfa.start_state}")
    print(f"接受状态: {dfa.accept_states}")
    print("DFA转换函数:")
    for state, trans in dfa.transitions.items():
        for symbol, next_state in trans.items():
            print(f"{state} --{symbol}--> {next_state}")
    
    return dfa

def test_regex_to_dfa():
    """测试不同的正则表达式"""
    test_cases = [
        "a(b|c)*",  # 以a开头，后面跟着任意数量的b或c
        "ab|c",     # 匹配ab或c
        "(a|b)*c",  # 任意数量的a或b，后面跟着c
    ]
    
    for i, regex in enumerate(test_cases, 1):
        print(f"\n{'='*50}")
        print(f"测试用例 {i}: {regex}")
        print('='*50)
        dfa = regex_to_dfa(regex)

if __name__ == "__main__":
    test_regex_to_dfa()
