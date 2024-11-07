from nfa2dfa import DFA
from DFA2minimal import hopcroft_minimization
import unittest

def print_dfa_info(dfa, title="DFA信息"):
    """打印DFA的详细信息"""
    print(f"\n{'-'*20} {title} {'-'*20}")
    print(f"起始状态: {dfa.start_state}")
    print(f"接受状态: {dfa.accept_states}")
    print("转换函数:")
    for state, trans in dfa.transitions.items():
        for symbol, target in trans.items():
            print(f"    δ({state}, {symbol}) = {target}")
    print("-" * (44 + len(title)))

class TestDFAMinimization(unittest.TestCase):
    def setUp(self):
        """在每个测试用例前执行"""
        self.maxDiff = None  # 显示完整的差异信息
        
    def test_basic_minimization(self):
        """测试基本的DFA最小化"""
        # 构造一个简单的DFA，接受所有包含'aa'的字符串
        dfa = DFA({'a', 'b'})
        dfa.start_state = 0
        dfa.accept_states = {2}
        dfa.transitions = {
            0: {'a': 1, 'b': 0},
            1: {'a': 2, 'b': 0},
            2: {'a': 2, 'b': 2}
        }
        
        print_dfa_info(dfa, "原始DFA")
        min_dfa = hopcroft_minimization(dfa).minimize()
        print_dfa_info(min_dfa, "最小化后的DFA")
        
        # 验证最小化后的状态数
        self.assertEqual(len(min_dfa.transitions), 3)
        self.assertTrue(min_dfa.start_state is not None)
        
    def test_unreachable_states(self):
        """测试包含不可达状态的DFA"""
        dfa = DFA({'a', 'b'})
        dfa.start_state = 0
        dfa.accept_states = {1, 4}
        dfa.transitions = {
            0: {'a': 1, 'b': 2},
            1: {'a': 1, 'b': 1},
            2: {'a': 2, 'b': 2},
            3: {'a': 4, 'b': 3},  # 不可达状态
            4: {'a': 4, 'b': 4}   # 不可达状态
        }
        
        print_dfa_info(dfa, "带不可达状态的DFA")
        min_dfa = hopcroft_minimization(dfa).minimize()
        print_dfa_info(min_dfa, "移除不可达状态后的DFA")
        
        # 验证最小化后不包含不可达状态
        self.assertLess(len(min_dfa.transitions), 5)
        
    def test_all_accepting(self):
        """测试所有状态都是接受状态的DFA"""
        dfa = DFA({'a'})
        dfa.start_state = 0
        dfa.accept_states = {0, 1, 2}
        dfa.transitions = {
            0: {'a': 1},
            1: {'a': 2},
            2: {'a': 0}
        }
        
        print_dfa_info(dfa, "全接受状态DFA")
        min_dfa = hopcroft_minimization(dfa).minimize()
        print_dfa_info(min_dfa, "最小化后的全接受状态DFA")
        
        # 验证最小化后只有一个状态
        self.assertEqual(len(min_dfa.transitions), 1)
        
    def test_complex_dfa(self):
        """测试一个较复杂的DFA"""
        dfa = DFA({'a', 'b'})
        dfa.start_state = 0
        dfa.accept_states = {1, 3, 5}
        dfa.transitions = {
            0: {'a': 1, 'b': 2},
            1: {'a': 3, 'b': 4},
            2: {'a': 1, 'b': 5},
            3: {'a': 3, 'b': 4},
            4: {'a': 1, 'b': 5},
            5: {'a': 3, 'b': 4}
        }
        
        print_dfa_info(dfa, "复杂DFA")
        min_dfa = hopcroft_minimization(dfa).minimize()
        print_dfa_info(min_dfa, "最小化后的复杂DFA")
        
        # 验证最小化结果
        self.assertLess(len(min_dfa.transitions), 6)
        
    def test_equivalent_states(self):
        """测试等价状态的合并"""
        dfa = DFA({'a', 'b'})
        dfa.start_state = 0
        dfa.accept_states = {1, 3}
        dfa.transitions = {
            0: {'a': 1, 'b': 2},
            1: {'a': 1, 'b': 3},  # 状态1和3是等价的
            2: {'a': 1, 'b': 2},
            3: {'a': 1, 'b': 3}   # 状态1和3是等价的
        }
        
        print_dfa_info(dfa, "含等价状态的DFA")
        min_dfa = hopcroft_minimization(dfa).minimize()
        print_dfa_info(min_dfa, "合并等价状态后的DFA")
        
        # 验证等价状态被合并
        self.assertEqual(len(min_dfa.transitions), 2)  # 应该只有2个状态
        
        # 额外验证最小化DFA的正确性
        # 验证接受状态数量
        self.assertEqual(len(min_dfa.accept_states), 1)
        # 验证转换完整性
        for state in min_dfa.transitions:
            self.assertEqual(len(min_dfa.transitions[state]), 2)  # 每个状态都应该有a和b两个转换

def run_tests():
    """运行所有测试用例"""
    # 创建测试套件
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDFAMinimization)
    
    # 运行测试
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_tests()
