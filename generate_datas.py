# -*- coding:utf-8 -*-
# 作者：李鹏飞
# 个人博客：https://www.lookfor404.com/
# 代码说明：https://www.lookfor404.com/用隐马尔可夫模型hmm做命名实体识别-ner系列二/
# github项目：https://github.com/lipengfei-558/hmm_ner_organization
def genertate_initial_vector(hidden_states):
    """
    生成初始化概率向量Π，命名为initial_vector.txt，格式每一行为：状态,出现次数,概率
    :param hidden_states: 隐藏状态list
    :return:
    """
    the_hidden_states = {x:0 for x in hidden_states}
    count = 0 # 计算总数
    with open("./data/nt.txt",mode='r') as nrfile:
        all_data = nrfile.readlines()
        for line in all_data:
            tags_and_freq = line.strip().split(" ")[1:]
            for index in range(0,len(tags_and_freq),2):
                tmp_list =  tags_and_freq[index:index+2]  #list的第一个元素为状态标识，第二个元素为数量
                the_hidden_states[tmp_list[0]] += eval(tmp_list[1])
                count += eval(tmp_list[1])
    with open("./data/initial_vector.txt",mode="w") as outputfile:
        for key,value in the_hidden_states.items():
            str_to_write = "%s,%d,%f\n" %(key,value,float(value)/count)
            outputfile.write(str_to_write)
    print ("generated ./data/initial_vector.txt")

def generate_transition_probability(hidden_states):
    """
    生成转移概率矩阵，命名为transition_probability.txt；格式为每一行：状态1,状态2,概率
    :param hidden_states:隐状态
    :return:
    """
    initial_count = {x: 0 for x in hidden_states}  #初始化计数
    result = []
    with open("./data/nt.tr.txt",mode="r") as initial_count_file:
        all_data = initial_count_file.readlines()
        for line in all_data[1:]:
            split_line = line.strip().split(",")
            first_state = split_line[0]
            the_sum = sum([eval(number) for number in split_line[1:]])
            for index,second_state in enumerate(hidden_states):
                result.append([first_state,second_state,str(float(split_line[1:][index])/the_sum)])
    #输出、写入文件
    with open("./data/transition_probability.txt",mode="w") as output_file:
        for thelist in result:
            str_to_write = "%s,%s,%s\n" %(thelist[0],thelist[1],thelist[2],)
            output_file.write(str_to_write)
    print ("generated ./data/transition_probability.txt")

def generate_emit_probability(initial_freq):
    """
    生成发射矩阵，命名为emit_probability.txt；格式为每一行：隐状态,显状态,概率
    :param initial_freq:隐状态初始化出现频数，是一个字典,key为隐状态标识，value为频数
    :return:
    """
    result = []
    with open("./data/nt.txt",mode="r") as nrfile:
        all_data = nrfile.readlines()
        for line in all_data:
            split_line = line.strip().split(" ")
            observed_state = split_line[0]
            tags_and_freq = split_line[1:]
            for index in range(0,len(tags_and_freq),2):
                tmp_list =  tags_and_freq[index:index+2]  #list的第一个元素为隐状态标识，第二个元素为数量
                result.append([tmp_list[0],observed_state,float(tmp_list[1])/initial_freq[tmp_list[0]]])

    # 输出、写入文件
    with open("./data/emit_probability.txt",mode="w") as output_file:
        for thelist in result:
            str_to_write = "%s,%s,%s\n" % (thelist[0], thelist[1], str(thelist[2]))
            output_file.write(str_to_write)
    print ("generated ./data/emit_probability.txt")

def get_initial_freq():
    """
    获取每个标签出现的频数
    :return: 字典，key为标签，value为频数
    """
    result = {}
    with open("./data/initial_vector.txt", mode="r") as file:
        all_data = file.readlines()
        for line in all_data:
            split_line = line.strip().split(",")
            if len(split_line) == 3:
                result[split_line[0]] = int(split_line[1])
    return result

if __name__ == '__main__':
    hidden_states = ["A", "B", "C", "D", "F", "G", "I", "J", "K", "L", "M", "P", "S", "W", "X", "Z"]
    genertate_initial_vector(hidden_states)
    generate_transition_probability(hidden_states)
    generate_emit_probability(get_initial_freq())
