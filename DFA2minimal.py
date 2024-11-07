from nfa2dfa import DFA
from collections import defaultdict

class hopcroft_minimization:
    def __init__(self, dfa):
        self.dfa = dfa
        self.partitions = []
        
    def split(self, partition, symbol):
        """根据输入符号分割状态集合"""
        transitions = defaultdict(set)
        
        # 收集转换信息
        for state in partition:
            if state in self.dfa.transitions and symbol in self.dfa.transitions[state]:
                target = self.dfa.transitions[state][symbol]
                # 找出目标状态所在的分区
                target_partition_idx = self._find_partition(target)
                if target_partition_idx is not None:
                    transitions[target_partition_idx].add(state)
        
        # 如果存在多个不同的转换目标，需要分割
        if len(transitions) > 1:
            new_partitions = list(transitions.values())
            # 添加没有转换的状态
            remaining = partition - set().union(*new_partitions)
            if remaining:
                new_partitions.append(remaining)
            return new_partitions
        return [partition]
    
    def _find_partition(self, state):
        """查找状态所在的分区索引"""
        for i, partition in enumerate(self.partitions):
            if state in partition:
                return i
        return None
    
    def minimize(self):
        """执行Hopcroft算法进行DFA最小化"""
        # 初始分区：接受状态和非接受状态
        accept = self.dfa.accept_states
        all_states = set(self.dfa.transitions.keys())
        for target_dict in self.dfa.transitions.values():
            for target in target_dict.values():
                all_states.add(target)
        non_accept = all_states - accept
        
        self.partitions = [accept, non_accept] if non_accept else [accept]
        
        # 删除空集
        self.partitions = [p for p in self.partitions if p]
        
        waiting = self.partitions.copy()
        
        while waiting:
            partition = waiting.pop(0)
            for symbol in self.dfa.alphabet:
                for p in self.partitions:
                    split_result = self.split(p, symbol)
                    if len(split_result) > 1:  # 如果可以分割
                        # 更新分区和等待集
                        idx = self.partitions.index(p)
                        self.partitions.pop(idx)
                        self.partitions.extend(split_result)
                        
                        # 更新waiting列表
                        if p in waiting:
                            waiting.remove(p)
                            waiting.extend(split_result)
                        else:
                            # 添加较小的分区到waiting
                            waiting.append(min(split_result, key=len))
        
        return self._construct_minimized_dfa()
    
    def _construct_minimized_dfa(self):
        """构建最小化后的DFA"""
        min_dfa = DFA(self.dfa.alphabet)
        
        # 创建分区到新状态的映射
        partition_to_state = {
            frozenset(partition): i 
            for i, partition in enumerate(self.partitions)
        }
        
        # 设置起始状态
        for partition in self.partitions:
            if any(state == self.dfa.start_state for state in partition):
                min_dfa.start_state = partition_to_state[frozenset(partition)]
                break
        
        # 设置接受状态
        for partition in self.partitions:
            if partition & self.dfa.accept_states:
                min_dfa.accept_states.add(partition_to_state[frozenset(partition)])
        
        # 构建转换函数
        min_dfa.transitions = {}
        for partition in self.partitions:
            state_repr = next(iter(partition))  # 选择一个代表状态
            current_state = partition_to_state[frozenset(partition)]
            min_dfa.transitions[current_state] = {}
            
            if state_repr in self.dfa.transitions:
                for symbol, target in self.dfa.transitions[state_repr].items():
                    for p in self.partitions:
                        if target in p:
                            min_dfa.transitions[current_state][symbol] = partition_to_state[frozenset(p)]
                            break
        
        return min_dfa

