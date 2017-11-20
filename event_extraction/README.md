# Intro: #
This project focuses on extracting events from social media texts based on semantic rules. Output structure is consisted of A0(agent), V(action), A1(object). And it generates pivot tables to do word frequency analysis with different time period.

It should be noted that, due to business secrets, some modules cannot be uploaded here~

prepared for the following clustering analysis

## Entrance: ltp_analysis_s.py
The entrance is python process.py  -h 返回值为抽取结构表或分时间槽的（A0，V,A1）词频统计

## Description of modules
1. Entrance: ltp_analysis_s.py
    模块调用的入口,具体调用 python process.py -h 返回值为抽取结构表或分时间槽的（A0，V,A1）词频统计
2. io_tools.py
    所有input,output function集合
3. ltp_preprocessing.py
    对ltp_word对单句处理后返回的值进行进一步加工满足后期函数的调用.
    记录单词，词性，句法依赖关系以及角色树等等 
4. ltp_word.py
5. text_preprocessing.py
    文本预处理
6. text_duplicate_removal.py
    文本重复预处理
7. extract_yuyi.py
    基于语义规则，抽取出事件元素A0,V,A1
8. save_infos.py
    输出抽取结果
9. verbtree_cut.py
    store the semantic tree
10. count.py
    do word frequency analysis 
11. time_series.py
    generates pivot tables to present the results with different time period

## Examples： ##

    %run ltp_analysis_s.py -r 'excel' -rf 'douban_tianfuzhen.xlsx' -w 'excel' -wf '1114tianfuzhen_freq' -sl 'all'


* -r 输入数据的类型，目前只支持excel
* -rf excel表格名称,默认路径在./datasets下面,支持绝对路径
* -s 表格裏sheet_name,默認從0開始
* -w 输出的格式,目前只支持excel
* -wf excel表格名称,默认路径在./datasets下面,支持绝对路径
* -pe 选择抽取结果词频分析的时间间隔，默认为月，有'year', 'quarter', 'month', 'week', 'day'
* -sl 选择分析的槽位，默认为'all'. 'extract'是输出事件三元素抽取表，'all'为同时抽取A0,V,A1, 也可单独抽取'A0','A1','V'

