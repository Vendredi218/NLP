# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 17:15:34 2017

@author: Vendredi
"""

from os import path
import pandas as pd
import  regex as re
'''
1.语义角色树这边有父子关系不明确的
2.抽连续动词
'''
def verbtree_return (roles):
    verbtree = {}
    visited = [role.index for role in roles] 
    cntdict = {}
    for role in roles:
        verb_index = role.index
        verbtree[verb_index] = {}
        verbtree[verb_index]['parent'] = []
        verbtree[verb_index]['child'] = []
    for role in roles:
        verb_index = role.index
        for arg in role.arguments:
            rolename = arg.name
            rolename = re.sub("C-","",rolename) if rolename in  ['C-A0','C-A1'] else rolename
            if rolename == "A1" or "A0":
                pstart = arg.range.start
                pend = arg.range.end
                for item in roles:
                    verbind = item.index
                    if verb_index == verbind:
                        continue
                    '''
                    args = item.arguments
                    start = args[0].range.start
                    end = args[-1].range.end
                    start = verbind if verbind<start else start
                    end = verbind if verbind>end else end
                    if pstart<= start and end<= pend:
                        verbtree[verbind]['parent'].append(verb_index)
                        cntdict[verb_index] = cntdict.get(verb_index,0)+1   
                    '''
                    if verbind <= pend and verbind >= pstart:
                        verbtree[verbind]['parent'].append(verb_index)
                        cntdict[verb_index] = cntdict.get(verb_index,0)+1  
                    #print (verb_index, verbind, rolename)
                    #print (verbtree)
                    #print (cntdict)
    import operator
    sorted_cntdict = sorted(cntdict.items(), key=operator.itemgetter(1),reverse=False)
    orders = [item[0] for item in sorted_cntdict]
    for verb_index in visited:
        parent = verbtree[verb_index]['parent']
        for order in orders:
            if order in parent:
                verbtree[verb_index]['parent'] = order
                break
    for verb_index in verbtree.keys():
        parent = verbtree[verb_index]['parent']
        if parent != []:
            verbtree[parent]['child'].append(verb_index)           
    return verbtree


def cut_simple (roles, index, rolesdict,words,sent):
    verbtree = verbtree_return(roles)
#    print (verbtree)
    A0sim = []
    A1sim = []
    if verbtree[index]['child'] == []:
        #如果第index个动词的child为空，则对应的A0,A1直接为A0sim，A1sim
        if 'A0' in rolesdict[index].keys():
            A0sim = rolesdict[index]['A0']
        if 'A1' in rolesdict[index].keys():
            A1sim = rolesdict[index]['A1']
    else:
        if 'A0' in rolesdict[index].keys():
            #只有当index词的所有child都不包含在其中一个语义角色时，那个语义角色才会作为语义树末端被记下
            for list in rolesdict[index]['A0']:
                for child in verbtree[index]['child']:
                    flag = True
                    if child >= list[0] and child <= list[1]:
                        flag = False
                        break 
                if flag == True:
                    A0sim.append(list)
        if 'A1' in rolesdict[index].keys():
            for list in rolesdict[index]['A1']:
                for child in verbtree[index]['child']:
                    flag = True
                    if child >= list[0] and child <= list[1]:
                        flag = False
                        break 
                if flag == True:
                    A1sim.append(list)        
    return A0sim, A1sim
        
        
    