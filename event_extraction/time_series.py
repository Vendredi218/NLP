# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:20:18 2017

@author: Vendredi
"""
import pandas as pd
import numpy as np
from save_infos import save_ltp_details
from extract_yuyi import extract_yuyi_main
from count import count_all

def combine_table(table_count,jword):
    if jword == 'single':
        frames = []
        for key in table_count:
            frames.append(table_count[key])
        result = pd.concat(frames)
        return result
    if jword == 'multi':
        V_table = {}
        A0_table = {}
        A1_table = {}
        for key in table_count:
            V,A0,A1 = table_count[key]
            V_table[key] = V
            A0_table[key] = A0
            A1_table[key] = A1
        Vcount = combine_table(V_table,'single')
        A0count = combine_table(A0_table,'single')
        A1count = combine_table(A1_table,'single')
        return Vcount, A0count, A1count
 
def crosstab_gen(**kwargs):
    #生成交叉透视表
    df = kwargs['df']
    period = kwargs['period']
    slot = kwargs['slot']
    
    del kwargs['df'],kwargs['period'],kwargs['slot']
    
    if period == 'year':
        df['period'] = pd.PeriodIndex(df.created_at, freq = 'A')
    if period == 'quarter':
        df['period'] = pd.PeriodIndex(df.created_at, freq = 'Q')
    if period == 'month':
        df['period'] = pd.PeriodIndex(df.created_at, freq = 'M')
    if period == 'week':
        df['period'] = pd.PeriodIndex(df.created_at, freq = 'W')
    if period == 'day':
        df['period'] = pd.PeriodIndex(df.created_at, freq = 'D')
    grouply = df.groupby(df['period'])
    df_period = {}
    for name, group in grouply:
        df_period[str(name)] = group
    print("得到日期分组dict")
    
    
    
    table_extract = {}
    table_count = {}
    for name in df_period:
        print(name)
        #每个时间段对应的子内容分别抽取语义角色
        sentsdoc = save_ltp_details(df_period[name])
        event_yuyi = extract_yuyi_main(sentsdoc)
        if slot == 'extract':
            table_extract[name] = event_yuyi
            print("得到抽取元素表")
            continue 
        Vcount, A0count, A1count = count_all(event_yuyi)
        if slot == 'V':
            table_count[name] = Vcount
        if slot == 'A0':
            table_count[name] = A0count
        if slot == 'A1':
            table_count[name] = A1count
        if slot == 'all':
            table_count[name] = Vcount,A0count,A1count
        for item in table_count[name]:
            item[period] = name
        print("得到count表")
    
    if slot == 'extract':
        event = combine_table(table_extract,'single')
        print("得到完整元素抽取表")
        return event
    if slot == 'all':
        count_table_V,count_table_A0,count_table_A1 = combine_table(table_count,'multi')
        print("得到完整所有表")
        #得到三张透视表
        crosstab_V = pd.pivot_table(count_table_V,index=['word'],values=['freq'],columns=[period],aggfunc=np.sum,fill_value=0)
        crosstab_A0 = pd.pivot_table(count_table_A0,index=['word'],values=['freq'],columns=[period],aggfunc=np.sum,fill_value=0)
        crosstab_A1 = pd.pivot_table(count_table_A1,index=['word'],values=['freq'],columns=[period],aggfunc=np.sum,fill_value=0)
        return crosstab_V,crosstab_A0,crosstab_A1
    else:
        count_table = combine_table(table_count,'single')
        print("得到完整count表")
        crosstab = pd.pivot_table(count_table,index=['word'],values=['freq'],columns=[period],aggfunc=np.sum,fill_value=0)
        return crosstab
