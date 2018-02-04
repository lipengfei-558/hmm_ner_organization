# -*- coding:utf-8 -*-
import jieba
class OrgRecognize:
    def __init__(self, input_sentence):
        self.hidden_states = ["A", "B", "C", "D","F","G","I","J","K","L","M","P","S","W","X","Z"]
        self.observed_states = self.get_observed_states(sentence=input_sentence)
        self.initial_vector = self.load_initial_vector()
        self.transision_matrix = self.load_transition_matrix(hidden_states=self.hidden_states)
        self.emission_matrix = self.load_emission_matrix(hidden_states=self.hidden_states)

    def load_patterns(self):
        """
        读取机构名模式串
        :return: list，元素为模式串
        """
        result = []
        with open("./data/nt.pattern.txt", "rb") as file:
            datas = file.readlines()
            for line in datas:
                result.append(line.strip())
        return result

    def load_transition_matrix(self,hidden_states):
        """
        载入状态转移矩阵
        :return: 字典：key为首状态，value为字典--key为次状态，value为概率
        """
        result = {x: {} for x in hidden_states}
        with open("./data/transition_probability.txt","rb") as file:
            datas = file.readlines()
            for line in datas:
                split_line = line.strip().split(",")
                result[split_line[0]][split_line[1]] =  split_line[2]
        return result
    def load_initial_vector(self):
        """
        载入初始化向量
        :return: 字典：key为隐状态标识，value为概率
        """
        result = {}
        with open("./data/initial_vector.txt","rb") as file:
            datas = file.readlines()
            for line in datas:
                split_line = line.strip().split(",")
                result[split_line[0]] =  split_line[2]
        return result

    def load_emission_matrix(self,hidden_states):
        """
        载入发射矩阵
        :param hidden_states: 隐藏状态list
        :return: 字典，格式为：key为隐状态，value是一个字典--key为观察状态，value为概率
        """
        result = {x:{} for x in hidden_states}
        with open("./data/emit_probability.txt","rb") as file:
            datas = file.readlines()
            for line in datas:
                split_line = line.strip().split(",")
                result[split_line[0]][split_line[1]] = split_line[2]
        return  result
    def get_observed_states(self,sentence):
        return sentence

    def viterbi(self,observation,hidden_states,initial_probability,transition_probability,emit_probability):
        """
        用维特比算法计算最优标签
        :param observation: 粗分词结果
        :param hidden_states: 隐藏状态标签，最终要求的标签都在里面
        :param initial_probability: 初始状态矩阵
        :param transition_probability: 转移状态矩阵
        :param emit_probability: 发射矩阵
        :return: 最优标签
        """
        result = []
        compute_recode = [] #记录每一次的计算结果
        #初始化
        tmp_result = {}
        for state in hidden_states:
            if emit_probability[state].has_key(observation[0]):
                tmp_result[state] = eval(initial_probability[state])*eval(emit_probability[state][observation[0]])
            else:
                tmp_result[state] = 0
        compute_recode.append(tmp_result)

        #对于之后的词语，继续计算
        for index,word in enumerate(observation[1:]):
            tmp_result = {}
            for current_state in hidden_states:
                #取最大值：上一次的所有状态(x)*转移到当前状态（current_state）*发射概率
                if emit_probability[current_state].has_key(word):
                    tmp_result[current_state] = max([compute_recode[index][x]*eval(transition_probability[x][current_state])*
                                                              eval(emit_probability[current_state][word]) for x in hidden_states])
                else:
                    tmp_result[current_state] = 0
            compute_recode.append(tmp_result)

        #返回概率最大的标签序列
        tag_sequence = []
        for recode in compute_recode:
            tag_sequence.append(max(recode, key=recode.get))
        return tag_sequence
    def get_organization(self,observation,sequence,patterns):
        """
        得到识别的机构名
        :param observation: 单词序列
        :param sequence: 标注序列
        :param patterns: 模式串
        :return: list，机构名
        """
        org_indices = []  # 存放机构名的索引
        orgs = [] # 存放机构名字符串
        tag_sequence_str = "".join(tag_sequence)  # 转为字符串
        for pattern in patterns:
            if pattern in tag_sequence_str:
                start_index = (tag_sequence_str.index(pattern))
                end_index = start_index + len(pattern)
                org_indices.append([start_index,end_index])
        if len(org_indices)!=0:
            for start,end in org_indices:
                orgs.append("".join(observation[start:end]))
        return orgs

if __name__ == '__main__':
    sentence = ["始##始", "中海油","集团","在", "哪里", "末##末"]
    orgrecog = OrgRecognize(sentence)
    observation = sentence
    initial_probability = orgrecog.load_initial_vector()
    transition_probability = orgrecog.load_transition_matrix(hidden_states=orgrecog.hidden_states)
    emit_probability = orgrecog.load_emission_matrix(hidden_states=orgrecog.hidden_states)
    tag_sequence = orgrecog.viterbi(observation=observation,hidden_states=orgrecog.hidden_states,initial_probability=initial_probability,transition_probability=transition_probability,emit_probability=emit_probability)
    print tag_sequence
    patterns = orgrecog.load_patterns()
    results = orgrecog.get_organization(observation=observation,sequence=tag_sequence,patterns=patterns)
    if len(results) == 0:
        print "未识别到机构名"
        print tag_sequence
    else:
        for result in results:
            print result
