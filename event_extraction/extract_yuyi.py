# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 14:41:58 2017

@author: Vendredi
"""
from ltp_word import LTP_word
import re
from os import path
import pandas as pd
from ltp_preprocessing import LtpProcess
from verbtree_cut import cut_simple


def extract_word_relation(index, word_related_index,word_related_type):
    '''
    给定一个单词的index，抽取这个单词的target，source的所有连接句子relation 返回dict
    '''
    word_sen_relation = {}
    related_index = [(i,word_related_type[i]) for i,x in enumerate(word_related_index) if x == index]
    word_sen_relation['target'] = related_index 
    if word_related_type[index] == 'HED':
        word_sen_relation['source'] = [-1]
    else:
        word_sen_relation['source'] = [word_related_index[index]]
    return word_sen_relation

def find_relation(target, relation):
    temp = []
    for index, rela in target:
        if rela == relation:
            temp.append(index)
    return temp


def find_arguments(rolename,rolesdict,index):
    for role in rolesdict[index]:
        if role == rolename:
            return (rolesdict[index][role])

        
def trans2content(roleindex,word_content):
    if len(roleindex) ==2:
        content = ''.join(word_content[roleindex[0]:roleindex[1]+1])
    else:
        content = word_content[roleindex[0]]
    return content
    

def delete_empty(content):
    if content == []:
        return None
    else:
        return content

def find_all_ATT(svw, word_related_index,word_related_type,ATT,postags,word_content):
    svw_rela = extract_word_relation(svw, word_related_index,word_related_type)
    target, source = svw_rela['target'], svw_rela['source']
    att = find_relation(target,'ATT')
    if att != []:
        for a in att:
            ATT.append(a)
            if extract_word_relation(a, word_related_index,word_related_type)['target'] == []:
                return ATT
            else:
                return find_all_ATT(a, word_related_index,word_related_type,ATT,postags,word_content)
    else:
        return ATT

def deal_att(ATT,postags,word_content):
    ATT2 = []
    for a in ATT:
        if postags[a] not in ['nd'] and word_content[a] not in ['其','这','那','一个']:
            ATT2.append(a)
    return ATT2
        
def find_only_core(corelist, vindex):
    ini = corelist[0]
    dif = abs(ini-vindex)
    for sw in corelist:
        if abs(sw-vindex)<dif:
            dif = abs(sw-vindex)
            ini = sw
    A0onlycore = [ini]
    return A0onlycore
    

def extract_yuyi_core(rolename, target, role, word_related_index,word_related_type,postags,word_content,vindex):
    '''
    提取A0,A1中的核心词
    '''
    if rolename == 'A0':
        sbvword = find_relation(target, 'SBV')
        A0core = []
        ATT = []
        for sw in sbvword:    #sw是个index
            for item in role:
                Flag = True
                if sw >= item[0] and sw <= item[1]:
                    Flag = False
                    A0core.append(sw)
                    ATT = find_all_ATT(sw, word_related_index,word_related_type,ATT,postags,word_content)
                    ATT = deal_att(ATT,postags,word_content)
                if Flag == False:
                    break
        if len(A0core)>1:
            A0core = find_only_core(A0core,vindex)
        return A0core,ATT
    if rolename == 'A1':
        vobword = find_relation(target, 'VOB')
        A1core = []
        ATT = []
        for vw in vobword:
            for item in role:
                Flag = True
                if vw >= item[0] and vw <= item[1]:
                    Flag = False
                    A1core.append(vw)
                    ATT = find_all_ATT(vw, word_related_index,word_related_type,ATT,postags,word_content)
                    ATT = deal_att(ATT,postags,word_content)
                if Flag == False:
                    break
        if len(A1core)>1:
            A1core = find_only_core(A1core,vindex)
        return A1core,ATT


def del_word(attcont):
    if 'reply' in attcont:
        attcont.remove('reply')
    if ',' in attcont:
        attcont.remove(',')
    return attcont
        

def extract_yuyi_event(sent):
    global ltp,ltp_process
    words, postags, arcs, roles, netags = ltp.deal(sent)
    word_content, word_pos, word_netags, word_related_index, word_related_type, rolesdict =ltp_process.deal_ltp_return(words, postags, arcs, roles,netags)
#    print("得到word的信息")
    '''
    for i,x in enumerate(words):
        print (i,x)
    for role in roles:
        print (role.index, "".join(
                ["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
    '''
    patterns = {}
#    badword = ['是', '有', '到', '要', '会', '能', '可以', '为', '可']
    for index in (rolesdict):
        #抽取每个语义root词的relation，包括target和source
        #每个语义树A0,A1角色只取最末端的结构，也就是不会有重复的角色出现，并且保证每个动词都保留
        word_rela = extract_word_relation(index, word_related_index,word_related_type)
        target, source = word_rela['target'], word_rela['source']
        A0sim, A1sim = cut_simple(roles, index, rolesdict,words,sent)
        for rolename in rolesdict[index]:
            V = [index]
            A0 = find_arguments('A0',rolesdict,index)
            A1 = find_arguments('A1',rolesdict,index)
            TMP = find_arguments('TMP', rolesdict, index)
            LOC = find_arguments('LOC', rolesdict, index)
            TPC = find_arguments('TPC', rolesdict, index)
        A0core, A0att = extract_yuyi_core ('A0', target, A0sim, word_related_index,word_related_type,postags,word_content,index)
        A1core, A1att = extract_yuyi_core ('A1', target, A1sim, word_related_index,word_related_type,postags,word_content,index)
        
        Nh = []
        Ni = []
        Ns = []
        for i, netags in enumerate(word_netags):
            real_i = i
            if netags in ['S-Nh']:
                if  word_related_type[index] == 'HED':
                    Nh.append(word_content[real_i])
                    continue
                while True:
                    netags_rela = extract_word_relation(i,word_related_index,word_related_type)
                    if netags_rela['source'][0] == index:
                        Nh.append(word_content[real_i])
                        break
                    i = netags_rela['source'][0]
                    if i == -1:
                        break
            if netags in ['S-Ni','B-Ni','E-Ni']:
                if  word_related_type[index] == 'HED':
                    Ni.append(word_content[real_i])
                    continue
                while True:
                    netags_rela = extract_word_relation(i,word_related_index,word_related_type)
                    if netags_rela['source'][0] == index:
                        Ni.append(word_content[real_i])
                        break
                    i = netags_rela['source'][0]
                    if i == -1:
                        break
            if netags in ['S-Ns']:
                if  word_related_type[index] == 'HED':
                    Ns.append(word_content[real_i])
                    continue
                while True:
                    netags_rela = extract_word_relation(i,word_related_index,word_related_type)
                    if netags_rela['source'][0] == index:
                        Ns.append(word_content[real_i])
                        break
                    i = netags_rela['source'][0]
                    if i == -1:
                        break     
        Ni = ','.join([Ni[i] for i in range(0,len(Ni))])
        Nh = ','.join([Nh[i] for i in range(0,len(Nh))])
        Ns = ','.join([Ns[i] for i in range(0,len(Ns))])
        patterns[index] =[A0, A0sim, A0core, A0att, V, A1att, A1core, A1sim, A1, TMP, LOC, TPC, Nh, Ni, Ns]    
    coredict = {}
    if patterns:
        for key in patterns.keys():
            A0,A0sim,A0core,A0att,V,A1att, A1core,A1sim,A1,TMP,LOC,TPC, Nh, Ni, Ns = tuple(patterns[key])
            A0content = []
            A1content = []
            A0simcont = []
            A1simcont = []
            A0corecont = []
            A0attcont = []
            A1attcont = []
            A1corecont = []
            TMPcontent = []
            LOCcontent = []
            TPCcontent = []
            if A0core != None:
                for index in A0core:
                    A0corecont.append(word_content[index])
                A0corecont = del_word(A0corecont)
                A0corecont = ','.join([A0corecont[i] for i in range(0,len(A0corecont))])
            if A0att != None:
                for index in A0att:
                    A0attcont.append(word_content[index])
                A0attcont = ','.join([A0attcont[i] for i in range(0,len(A0attcont))])
            if A1core != None:
                for index in A1core:
                    A1corecont.append(word_content[index])
                A1corecont = del_word(A1corecont)
                A1corecont = ','.join([A1corecont[i] for i in range(0,len(A1corecont))])
            if A1att != None:
                for index in A1att:
                    A1attcont.append(word_content[index])
                A1attcont = ','.join([A1attcont[i] for i in range(0,len(A1attcont))])
            if A0 != None:
                for item in A0:
                    A0content.append(trans2content(item,word_content))
                A0content = ','.join([A0content[i] for i in range(0,len(A0content))])
            if A0sim != None:
                for item in A0sim:
                    A0simcont.append(trans2content(item,word_content))
                A0simcont = ','.join([A0simcont[i] for i in range(0,len(A0simcont))])
            if A1sim != None:
                for item in A1sim:
                    A1simcont.append(trans2content(item,word_content))
                A1simcont = ','.join([A1simcont[i] for i in range(0,len(A1simcont))])
            if A1 != None:
                for item in A1:
                    A1content.append(trans2content(item, word_content))
                A1content = ','.join([A1content[i] for i in range(0,len(A1content))])
            if TMP != None:
                for item in TMP:
                    TMPcontent.append(trans2content(item, word_content))
                TMPcontent = ','.join([TMPcontent[i] for i in range(0,len(TMPcontent))])
            if LOC != None:
                for item in LOC:
                    LOCcontent.append(trans2content(item, word_content))
                LOCcontent = ','.join([LOCcontent[i] for i in range(0,len(LOCcontent))])
            if TPC != None:
                for item in TPC:
                    TPCcontent.append(trans2content(item, word_content))
                TPCcontent = ','.join([TPCcontent[i] for i in range(0,len(TPCcontent))])
            Vcontent = trans2content(V, word_content)
            A0content=delete_empty(A0content)
            A1content=delete_empty(A1content)
            A0simcont=delete_empty(A0simcont)
            A1simcont=delete_empty(A1simcont)
            A0corecont=delete_empty(A0corecont)
            A0attcont=delete_empty(A0attcont)
            A1attcont=delete_empty(A1attcont)
            A1corecont=delete_empty(A1corecont)
            Vcontent=delete_empty(Vcontent)
            TMPcontent=delete_empty(TMPcontent)
            LOCcontent=delete_empty(LOCcontent)
            TPCcontent=delete_empty(TPCcontent)   
            coredict[key] = [A0content, A0simcont, A0corecont, A0attcont, Vcontent, A1attcont,A1corecont, A1simcont, A1content, TMPcontent, LOCcontent, TPCcontent, Nh, Ni, Ns]
    return coredict


def extract_yuyi_main(sentsdoc):
    print("开始语义抽取")
    global ltp,ltp_process
    ltp=LTP_word("/home/zww/learngit/project_test/dp_relation_2/models")
    ltp_process=LtpProcess()
    doce = sentsdoc.loc[:,['sent_id','sent','content_id']].get_values()
    corelists=[]
    for item in doce:
        sent_id, sent, content_id = tuple(item)
        if not isinstance(sent,str) or sent== 'None':
            continue
        coredict = extract_yuyi_event(sent)
        if coredict:
            for key in coredict.keys():
                coredict[key].extend([sent_id,content_id,sent])
                corelists.append(coredict[key])
    event=pd.DataFrame(corelists,columns=['A0', 'A0sim', 'A0core','A0att', 'V', 'A1att', 'A1core', 'A1sim', 'A1','TMP','LOC','TPC', 'Nh', 'Ni', 'Ns','sent_id','content_id','sent'])
    return event
    ltp.release()