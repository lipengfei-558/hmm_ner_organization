# 基于HMM模型的机构名实体识别

## 1.环境依赖
 - python 2.7
 - jieba （可选）
 
## 2.算法说明
参考《基于角色标注的中文机构名识别》论文，结合HanLP提供的针对机构名的HMM语料，实现了基于HMM模型的机构名实体识别算法。

详细说明文档，可前往我的博客围观：[用隐马尔可夫模型(HMM)做命名实体识别——NER系列（二）](https://www.lookfor404.com/%e7%94%a8%e9%9a%90%e9%a9%ac%e5%b0%94%e5%8f%af%e5%a4%ab%e6%a8%a1%e5%9e%8bhmm%e5%81%9a%e5%91%bd%e5%90%8d%e5%ae%9e%e4%bd%93%e8%af%86%e5%88%ab-ner%e7%b3%bb%e5%88%97%e4%ba%8c/)

## 3.使用说明

首先，运行以下脚本：

`python generate_data.py`

会在`./data`下生成`transition_probability.txt`，`emit_probability.txt`以及`initial_vector.txt`

然后，运行:

`python OrgRecognize.py`

就可以了，不出意外，“中海油集团在哪里”这句话，会识别出“中海油集团”这个机构实体。

## 4.参考资料

- 张华平, 刘群. 基于角色标注的中国人名自动识别研究[J]. 计算机学报, 2004, 27(1):85-91.
- 俞鸿魁, 张华平, 刘群. 基于角色标注的中文机构名识别[C]// Advances in Computation of Oriental Languages--Proceedings of the, International Conference on Computer Processing of Oriental Languages. 2003.
- 俞鸿魁, 张华平, 刘群,等. 基于层叠隐马尔可夫模型的中文命名实体识别[J]. 通信学报, 2006, 27(2):87-94.
- 码农场文章：[层叠HMM-Viterbi角色标注模型下的机构名识别](http://www.hankcs.com/nlp/ner/place-name-recognition-model-of-the-stacked-hmm-viterbi-role-labeling.html)
