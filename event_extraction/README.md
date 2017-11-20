# Intro: #
This project focuses on extracting events from social media texts based on semantic rules. Output structure is consisted of A0(agent), V(action), A1(object). And it generates pivot tables to do word frequency analysis with different time period.

prepared for the following clustering analysis

## Entrance: ltp_analysis_s.py
The entrance is python process.py  -h 返回值为抽取结构表或分时间槽的（A0，V,A1）词频统计

## Examples： ##

    %run ltp_analysis_s.py -r 'excel' -rf 'douban_tianfuzhen.xlsx' -w 'excel' -wf '1114tianfuzhen_freq' -sl 'all'


* -r 输入数据的类型，目前只支持excel
* -rf excel表格名称,默认路径在./datasets下面,支持绝对路径
* -s 表格裏sheet_name,默認從0開始
* -w 输出的格式,目前只支持excel
* -wf excel表格名称,默认路径在./datasets下面,支持绝对路径
* -pe 选择抽取结果词频分析的时间间隔，默认为月，有'year', 'quarter', 'month', 'week', 'day'
* -sl 选择分析的槽位，默认为'all'. 'extract'是输出事件三元素抽取表，'all'为同时抽取A0,V,A1, 也可单独抽取'A0','A1','V'

