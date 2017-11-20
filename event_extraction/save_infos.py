# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:23:30 2017

@author: Vendredi
"""

import pandas as pd
from text_preprocessing import TextProcess
from ltp_word import LTP_word
from ltp_preprocessing import LtpProcess
import re
from functools import reduce
from text_duplicate_removal import DuplicateRemoval
#from extract import extract_main


def deal_ltp_Words(words,postags,arcs,netags):
    #将ltp_word的返回的数据做个预处理，保存下所有的单词信息,返回单词表
    words_table = []
    for k, arc in enumerate(arcs):
        words_table.append([k,words[k],postags[k],arc.head,arc.relation,netags[k]])
    return words_table

def deal_ltp_Semantic_Role(roles,words):
    '''
    将ltp_word的返回的数据做个预处理，保存下所有角色
    
    '''
    roles_table = []
    cnt = -1
    for role in roles:
        verb_index = role.index
        flag = True
        for arg in role.arguments:
            rolename = arg.name
            rolename = re.sub("C-","",rolename) if rolename in  ['C-A0','C-A1'] else rolename
            cnt += 1
            start,end = arg.range.start ,arg.range.end  
            if start > verb_index and flag:
                roles_table.append([cnt,'V',verb_index,verb_index,verb_index,words[verb_index]])
                flag = False
                cnt += 1
            roles_table.append([cnt,rolename,start,end,verb_index,''.join(words[start:end+1])])
        if flag:
            cnt+=1
            roles_table.append([cnt,'V',verb_index,verb_index,verb_index,words[verb_index]])
    return roles_table

def combine_tables(first,last):
    for i,item in enumerate(first):
#       print (last[i])
        item += last[i]
    return first

def get_content_to_parse(contents):
    global ltp,duplicate_removal,text_process
    sentsdoc = []
    rotable = []
    wotable = []
#    roletree = []
#    verbtree = []
    content_id=contents[0]
    content=contents[1]
    if isinstance(content,float) : 
        return [rotable,wotable,sentsdoc]
#    print (content)
    content = duplicate_removal.main(content)
    sents=text_process.split2sent(content)
    for sent_i,sent in enumerate(sents):
        sent =sent.strip()
        sent = duplicate_removal.main(sent)
#        sent = text_process.re_sub(sent)
        sent = text_process.translate(sent, 'cen')
        if sent=='' or len(sent)>=1000:
            continue
        sentsdoc.append([sent_i,sent,content_id])
        words,postags,arcs,roles,netags = ltp.deal(sent)
        wordstable = deal_ltp_Words(words,postags,arcs,netags)
        rolestable = deal_ltp_Semantic_Role(roles,words)
        for item in rolestable:
            item.extend([sent_i,content_id])
        for item in wordstable:
            item.extend([sent_i,content_id])
        rotable.extend(rolestable)
        wotable.extend(wordstable)  
    return [rotable,wotable,sentsdoc]
#    return [wordstable]

def save_ltp_details(df):
    global ltp,duplicate_removal,text_process,ltp_process
    ltp_process=LtpProcess()
    text_process=TextProcess()
    duplicate_removal=DuplicateRemoval()
    ltp=LTP_word("./models")
    
#    df = kwargs['df']
#    del kwargs['df']
    
    if not 'content_id' in df.columns:
        df['content_id']=range(len(df))
        
    doc=df.loc[:,['content_id','content']]   
    contents = doc.loc[:,['content_id','content']].get_values() 
    t=[]
    for content in contents:
        t.append(get_content_to_parse(content))
        
    table = reduce(combine_tables,t[1:],t[0])
    rolestable,wordstable,sentsdoc = tuple(table)
    ltp.release()
    
    '''
    得到三个预处理结果table
    '''
    rolestable = pd.DataFrame(rolestable,columns=['role_node_index','role_name','role_begin_loc_index','role_end_loc_index','verb_loc_index','role_content','sent_id','content_id'])
    sentsdoc = pd.DataFrame(sentsdoc,columns=['sent_id','sent','content_id'])
    wordstable = pd.DataFrame(wordstable,columns=['word_loc_index','word','word_pos','source_loc_index','arg_type','netags','sent_id','content_id'])
#    kwargs['sheet_names'] = ['srs_sents','srs_roles','srs_words']
    return sentsdoc
#    write_data(srs_roles=rolestable,srs_sents = sentsdoc,srs_words = wordstable,sheet_names = kwargs['sheet_names'],write_type=kwargs['write_type'],write_url=kwargs['ltp_write_url'],project_id=kwargs['project_id'],keyword_id=kwargs['keyword_id'])
