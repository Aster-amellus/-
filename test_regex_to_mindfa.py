from re2nfa import regex_to_postfix, postfix_to_nfa
from nfa2dfa import subset_construction, NFA, DFA
from DFA2minimal import hopcroft_minimization
from Visualize_FA import visualize_nfa
import traceback

def safe_visualize(fa, filename):
    """安全的可视化函数，处理不同类型的自动机"""
    try:
        if isinstance(fa, (NFA, DFA)):
            visualize_nfa(fa, filename)
        else:
            print(f"警告: 无法识别的自动机类型 {type(fa)}")
    except Exception as e:
        print(f"可视化过程出错: {e}")
        traceback.print_exc()

def test_regex_to_mindfa(regex, test_name):
    """测试从正则表达式到最小化DFA的完整转换过程"""
    try:
        print(f"\n{'='*50}")
        print(f"测试用例: {test_name}")
        print(f"正则表达式: {regex}")
        print('='*50)
        
        # 1. 转换为后缀表达式
        postfix = regex_to_postfix(regex)
        print(f"后缀表达式: {postfix}")
        
        # 2. 构建NFA
        nfa = postfix_to_nfa(postfix)
        print("\nNFA构建完成")
        print(f"NFA状态数: {len(nfa.transitions)}")
        print(f"NFA起始状态: {nfa.start_state}")
        print(f"NFA接受状态: {nfa.accept_states}")
        safe_visualize(nfa, f'viz_{test_name}_nfa')
        
        # 3. NFA转换为DFA
        dfa = subset_construction(nfa)
        print("\nDFA构建完成")
        print(f"DFA状态数: {len(dfa.transitions)}")
        print(f"DFA起始状态: {dfa.start_state}")
        print(f"DFA接受状态: {dfa.accept_states}")
        safe_visualize(dfa, f'viz_{test_name}_dfa')
        
        # 4. DFA最小化
        hopcroft = hopcroft_minimization(dfa)
        min_dfa = hopcroft.minimize()
        print("\n最小化DFA构建完成")
        print(f"最小化DFA状态数: {len(min_dfa.transitions)}")
        print(f"最小化DFA起始状态: {min_dfa.start_state}")
        print(f"最小化DFA接受状态: {min_dfa.accept_states}")
        safe_visualize(min_dfa, f'viz_{test_name}_mindfa')
        
        return min_dfa
        
    except Exception as e:
        print(f"\n处理正则表达式 '{regex}' 时发生错误:")
        print(f"错误信息: {str(e)}")
        traceback.print_exc()
        return None

def print_dfa_info(dfa, name):
    """打印DFA的详细信息"""
    if dfa is None:
        print(f"\n{name} 处理失败")
        return
        
    print(f"\n{name} 详细信息:")
    print(f"状态数量: {len(dfa.transitions)}")
    print(f"起始状态: {dfa.start_state}")
    print(f"接受状态: {dfa.accept_states}")
    print("转换函数:")
    for state, trans in dfa.transitions.items():
        for symbol, target in trans.items():
            print(f"  {state} --{symbol}--> {target}")

if __name__ == "__main__":
    # 测试用例列表
    test_cases = [
        ("(a|b)*abb", "案例1_重复选择"),
        ("a(b|c)*", "案例2_星号测试"),
        ("(a|b)(c|d)", "案例3_连接测试"),
        ("(a|ε)b*", "案例4_空串测试"),
        ("(aa|bb)*", "案例5_复杂重复")
    ]
    
    print("开始进行正则表达式到最小化DFA的转换测试")
    print("="*50)
    
    # 执行所有测试用例
    for regex, test_name in test_cases:
        try:
            min_dfa = test_regex_to_mindfa(regex, test_name)
            print_dfa_info(min_dfa, test_name)
            print("\n" + "-"*50)
        except Exception as e:
            print(f"\n测试用例 {test_name} 执行失败:")
            print(f"错误信息: {str(e)}")
            traceback.print_exc()
            print("\n" + "-"*50)
