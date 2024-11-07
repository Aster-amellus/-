import unittest
from re2nfa import NFA, regex_to_postfix, postfix_to_nfa
from Visualize_FA import visualize_nfa

# 将测试正则表达式列表移到类外部
TEST_REGEX_LIST = [
    "a.b",
    "a|b",
    "a*",
    "(a.b)*",
    "a.b|c*"
]

class TestRe2NFA(unittest.TestCase):
    # 删除 setUp 方法，因为不再需要它
    
    def test_regex_to_postfix(self):
        self.assertEqual(regex_to_postfix("a.b"), "ab.")
        self.assertEqual(regex_to_postfix("a|b"), "ab|")
        self.assertEqual(regex_to_postfix("a*"), "a*")
        self.assertEqual(regex_to_postfix("(a.b)*"), "ab.*")
        print("✓ regex_to_postfix 测试通过")
    
    def test_postfix_to_nfa(self):
        postfix = regex_to_postfix("a.b")
        nfa = postfix_to_nfa(postfix)
        self.assertTrue(nfa.accepts("ab"))
        self.assertFalse(nfa.accepts("a"))
        self.assertFalse(nfa.accepts("b"))
        print("✓ postfix_to_nfa 测试通过")
    
    def test_nfa_accepts(self):
        postfix = regex_to_postfix("a*")
        nfa = postfix_to_nfa(postfix)
        self.assertTrue(nfa.accepts(""))
        self.assertTrue(nfa.accepts("a"))
        self.assertTrue(nfa.accepts("aa"))
        self.assertFalse(nfa.accepts("b"))
        print("✓ nfa_accepts 测试通过")
    
    def test_complex_regex(self):
        # 添加更复杂的正则表达式测试
        test_cases = [
            ("(a|b)*", ["", "a", "b", "ab", "ba", "aaa", "bbb", "aba"]),
            ("(a.b)*", ["", "ab", "abab", "ababab"]),
            ("a.(b|c)", ["ab", "ac"]),
            ("a*.b", ["b", "ab", "aab", "aaab"])
        ]
        
        for regex, valid_strings in test_cases:
            postfix = regex_to_postfix(regex)
            nfa = postfix_to_nfa(postfix)
            
            # 测试应该接受的字符串
            for s in valid_strings:
                self.assertTrue(nfa.accepts(s), f"正则表达式 {regex} 应该接受 '{s}'")
                
            # 测试一些应该拒绝的字符串
            invalid_strings = ["c", "bc", "cb", "abc", "bac"]
            for s in invalid_strings:
                if s not in valid_strings:  # 避免测试应该接受的字符串
                    self.assertFalse(nfa.accepts(s), f"正则表达式 {regex} 不应该接受 '{s}'")
        
        print("✓ complex_regex 测试通过")

def generate_visualizations(regex_list):
    """为一系列正则表达式生成NFA可视化图形"""
    for i, regex in enumerate(regex_list):
        print(f"\n正在生成正则表达式 '{regex}' 的NFA图形...")
        postfix = regex_to_postfix(regex)
        nfa = postfix_to_nfa(postfix)
        visualize_nfa(nfa, f'nfa_visualization_{i}')

if __name__ == "__main__":
    # 运行所有测试
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRe2NFA)
    runner = unittest.TextTestRunner(verbosity=2)
    test_results = runner.run(suite)
    
    # 如果所有测试都通过，生成可视化图形
    if test_results.wasSuccessful():
        print("\n所有测试通过，开始生成可视化图形...")
        generate_visualizations(TEST_REGEX_LIST)
    else:
        print("\n测试未全部通过，请修复错误后再生成可视化图形。")
