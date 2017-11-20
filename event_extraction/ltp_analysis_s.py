# -*- coding: utf-8 -*-
"""
Created on Fri Aug 25 17:23:31 2017

@author: Vendredi
"""
import argparse
import pandas as pd
from time_series import crosstab_gen
from io_tools import IO_tools
from os import path

def analysis(**kwargs):
    io_tool = IO_tools()
    try:
        data_path = './datasets_test'
        '''
        if kwargs['project'] and kwargs['keyword']:   
        # 输入格式为MySQL
            kwargs['project_id'],kwargs['keyword_id'],kwargs['table_name'] = get_data_info(project = kwargs['project'],keyword = kwargs['keyword'])
            kwargs['extract_write_url'] = path.join(data_path,kwargs['project']+'_'+kwargs['keyword']+"_extract")
            kwargs['cluster_write_url'] = path.join(data_path,kwargs['project']+'_'+kwargs['keyword']+"_cluster")
            kwargs['ltp_write_url'] = path.join(data_path,kwargs['project']+'_'+kwargs['keyword']+"_ltp")
        '''
        if kwargs['read_type'] == 'excel':
            #若读入的是file类型
            for key in ['read_url','write_url']:
                p,f = path.split(kwargs[key])
            #若文件没有给路径，默认文件在./datasets_test的路径下
                if not p:
                    kwargs[key] = path.join('./datasets_test',f)
        read_type = kwargs['read_type']
        period = kwargs['period']
        slot = kwargs['slot']
        print('kwargs:',kwargs)
        if read_type == 'mysql':
            print("还没完善")
        if read_type == 'excel':
            #从excel里面读入的数据，强制输出为excel
            kwargs['write_type'] = 'excel'
            kwargs['project_id'] = 9999
            kwargs['keyword_id'] = '9999_9999'
            kwargs['table_name'] = '9999'
            df = io_tool.get_data_from_file(kwargs['read_url'], 'excel', sheet_name=kwargs['sheet_name'])
            if df is None or (df is not None and df.empty):
                print(" 表格数据为空，无法操作!")
                return None
            kwargs['df'] = df
        if slot == 'all':
            V,A0,A1 = crosstab_gen(**kwargs)
            print('A0')
            print(A0[:10])
            if kwargs['write_type'] == 'excel':
                io_tool.write2excel(kwargs['write_url'],A0 = A0 ,V = V,A1 = A1,project_id = kwargs['project_id'],keyword_id = kwargs['keyword_id'])
            else:
                print('目前支持excel输出!')
        if slot == 'extract':
            event = crosstab_gen(**kwargs)
            if kwargs['write_type'] == 'excel':
                io_tool.write2excel(kwargs['write_url'], extract_tab = event, project_id = kwargs['project_id'],keyword_id = kwargs['keyword_id'])
            else:    
                print('目前支持excel输出!')
        if slot == 'V':
            V_tab = crosstab_gen(**kwargs)
            if kwargs['write_type'] == 'excel':
                io_tool.write2excel(kwargs['write_url'],V = V_tab,project_id = kwargs['project_id'],keyword_id = kwargs['keyword_id'])
            else:
                print('目前支持excel输出!')
        if slot == 'A0':
            A0_tab = crosstab_gen(**kwargs)
            if kwargs['write_type'] == 'excel':
                io_tool.write2excel(kwargs['write_url'],A0 = A0_tab,project_id = kwargs['project_id'],keyword_id = kwargs['keyword_id'])
            else:
                print('目前支持excel输出!')
        if slot == 'A1':
            A1_tab = crosstab_gen(**kwargs)
            if kwargs['write_type'] == 'excel':
                io_tool.write2excel(kwargs['write_url'],A1=A1_tab,project_id = kwargs['project_id'],keyword_id = kwargs['keyword_id'])
            else:
                print('目前支持excel输出!')
    except Exception as e:
        print(str(e))
        print("文件读入失败！")
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='事件元组抽取以及时间槽位上的频次统计')
    parser.add_argument('-r','--readtype',dest = 'readtype',nargs = '?',default = 'excel',help = "输入数据的类型，目前只支持excel ")
    parser.add_argument('-rf','--readfile',dest = 'filename',nargs='?',default = '',help = 'excel表格名称,默认路径在./datasets下面,支持绝对路径')
    parser.add_argument('-s','--sheetname',dest ='sheetname',nargs='?',default=0,help = '表格裏sheet_name,默認從0開始')
    parser.add_argument('-w','--writetype',dest ='writetype',nargs='?',default ='excel',help = '输出的格式,目前只支持excel')
    parser.add_argument('-wf','--writefile',dest ='writefile',nargs='?',default ='excel',help = '输出的格式,目前只支持excel,默认路径输出在./datasets下面')
    parser.add_argument('-pe', '--period', dest='period', nargs='?',default='month', help='选择分析的时间间隔，有year, quarter, month, week, day')
    parser.add_argument('-sl', '--slot', dest='slot', nargs='?',default='all', help='选择分析的槽位，extract是输出元素抽取表，all为同时抽取A0,V,A1, 也可单独抽取A0/A1/V')
    args = parser.parse_args()
    analysis(
        read_url = args.filename,
        read_type = args.readtype,
        sheet_name = args.sheetname,
        write_type = args.writetype,
        write_url = args.writefile,
        period = args.period,
        slot = args.slot
        )