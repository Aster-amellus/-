import unittest
from nfa2dfa import NFA, DFA, epsilon_closure, move, subset_construction
import os
import shutil
from datetime import datetime

class TestNFA2DFA(unittest.TestCase):
    def setUp(self):
        # 创建测试输出目录
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = f"test_outputs_{self.timestamp}"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        # 设置一个基础的 NFA 用于测试
        self.basic_transitions = {
            'q0': {'a': ['q1'], 'ε': ['q2']},
            'q1': {'b': ['q1'], 'ε': ['q3']},
            'q2': {'c': ['q2'], 'ε': ['q3']},
            'q3': {}
        }
        self.basic_nfa = NFA(
            start_state='q0',
            alphabet={'a', 'b', 'c', 'ε'},
            transitions=self.basic_transitions,
            accept_states={'q3'}
        )

    def test_epsilon_closure(self):
        # 测试 ε-闭包计算
        result = epsilon_closure(self.basic_nfa, {'q0'})
        self.assertEqual(result, {'q0', 'q2', 'q3'})
        
        result = epsilon_closure(self.basic_nfa, {'q1'})
        self.assertEqual(result, {'q1', 'q3'})
        
        # 测试空集的 ε-闭包
        result = epsilon_closure(self.basic_nfa, {'q3'})
        self.assertEqual(result, {'q3'})

    def test_move(self):
        # 测试 move 函数
        result = move(self.basic_nfa, {'q0'}, 'a')
        self.assertEqual(result, {'q1'})
        
        result = move(self.basic_nfa, {'q1'}, 'b')
        self.assertEqual(result, {'q1'})
        
        # 测试不存在的转换
        result = move(self.basic_nfa, {'q3'}, 'a')
        self.assertEqual(result, set())

    def test_subset_construction(self):
        # 测试完整的 NFA 到 DFA 转换
        dfa = subset_construction(self.basic_nfa)
        
        # 验证 DFA 的基本属性
        self.assertIsNotNone(dfa.start_state)
        self.assertEqual(dfa.alphabet, {'a', 'b', 'c'})
        self.assertGreater(len(dfa.accept_states), 0)
        
        # 验证转换函数的正确性
        start_state = dfa.start_state
        self.assertTrue(any(symbol in dfa.transitions[start_state] 
                          for symbol in ['a', 'c']))

    def test_special_cases(self):
        # 测试只有一个状态的 NFA
        simple_transitions = {
            'q0': {}
        }
        simple_nfa = NFA(
            start_state='q0',
            alphabet={'a'},
            transitions=simple_transitions,
            accept_states={'q0'}
        )
        simple_dfa = subset_construction(simple_nfa)
        self.assertEqual(len(simple_dfa.transitions), 1)
        
        # 测试只有 ε 转换的 NFA
        epsilon_transitions = {
            'q0': {'ε': ['q1']},
            'q1': {'ε': ['q2']},
            'q2': {}
        }
        epsilon_nfa = NFA(
            start_state='q0',
            alphabet={'ε'},
            transitions=epsilon_transitions,
            accept_states={'q2'}
        )
        epsilon_dfa = subset_construction(epsilon_nfa)
        # 验证所有的 ε 转换都被正确处理
        self.assertTrue(any(frozenset(['q0', 'q1', 'q2']) == state 
                          for state in epsilon_dfa.accept_states))

    def test_visualization(self):
        """测试NFA和DFA的可视化功能"""
        # 测试NFA可视化
        test_filename = os.path.join(self.output_dir, 'test_nfa')
        self.basic_nfa.visualize(test_filename)
        # 验证文件是否生成
        self.assertTrue(os.path.exists(f'{test_filename}.png'))

        # 测试DFA可视化
        dfa = subset_construction(self.basic_nfa)
        test_filename = os.path.join(self.output_dir, 'test_dfa')
        dfa.visualize(test_filename)
        # 验证文件是否生成
        self.assertTrue(os.path.exists(f'{test_filename}.png'))

    def test_complex_visualization(self):
        """测试更复杂的自动机可视化"""
        # 创建更复杂的NFA进行测试
        complex_transitions = {
            'q0': {'a': ['q1', 'q2'], 'ε': ['q2']},
            'q1': {'b': ['q3'], 'ε': ['q2']},
            'q2': {'c': ['q3', 'q4']},
            'q3': {'a': ['q4']},
            'q4': {}
        }
        complex_nfa = NFA(
            start_state='q0',
            alphabet={'a', 'b', 'c', 'ε'},
            transitions=complex_transitions,
            accept_states={'q4'}
        )

        # 测试复杂NFA的可视化
        test_filename = os.path.join(self.output_dir, 'test_complex_nfa')
        complex_nfa.visualize(test_filename)
        self.assertTrue(os.path.exists(f'{test_filename}.png'))

        # 测试转换后的DFA可视化
        complex_dfa = subset_construction(complex_nfa)
        test_filename = os.path.join(self.output_dir, 'test_complex_dfa')
        complex_dfa.visualize(test_filename)
        self.assertTrue(os.path.exists(f'{test_filename}.png'))

    def tearDown(self):
        """保留测试输出目录，不再删除文件"""
        print(f"\n测试输出文件保存在目录: {self.output_dir}")

def main():
    unittest.main()

if __name__ == '__main__':
    main()
