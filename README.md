# 正则表达式到最小化DFA转换器

这个项目实现了从正则表达式到最小化DFA的完整转换过程，包含以下步骤：
1. 正则表达式转换为NFA（Thompson算法）
2. NFA转换为DFA（子集构造法）
3. DFA最小化（Hopcroft算法）

## 功能特性

- 支持基本的正则表达式操作符：连接(.)、选择(|)、闭包(*)
- 使用Graphviz可视化自动机
- 支持ε转换
- 提供完整的状态转换过程

## 使用方法
起一个虚拟环境，安装Graphviz以及相关的依赖
```
pip install -r requirements
```
```
from re2nfa import regex_to_postfix, postfix_to_nfa
from nfa2dfa import subset_construction
from DFA2minimal import hopcroft_minimization
from Visualize_FA import visualize_nfa

# 转换正则表达式
regex = "ab*|c"
nfa = postfix_to_nfa(regex_to_postfix(regex))
dfa = subset_construction(nfa)
minimized_dfa = hopcroft_minimization(dfa).minimize()

# 可视化结果
visualize_nfa(nfa, 'nfa_output')
visualize_nfa(dfa, 'dfa_output')
visualize_nfa(minimized_dfa, 'min_dfa_output')
```
注意事项
需要安装Graphviz才能使用可视化功能
输入的正则表达式应遵循基本语法规则(不支持+ ，?等运算符)
可视化结果将保存为PNG格式图片
