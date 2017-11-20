# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 15:42:32 2017

@author: Vendredi
"""
# coding: utf-8
from os import path
import pandas as pd
import  regex as re

class LtpProcess():
    '''
    对ltp_word对单句处理后返回的值进行进一步加工满足后期函数的调用
    记录单词，词性，句法依赖关系以及角色树等等 
    '''
   
    def deal_ltp_return(self,words,postags,arcs,roles,netags):
        '''
        将ltp_word的返回的数据做个预处理，后期方便使用
        返回 单词 词性 关联index 关联关系 角色字典
        角色字典 存储每个角色的index的范围
        '''
        word_content = []
        word_pos = []
        word_related_index = []
        word_related_type = []
        word_netags = []
        for k, arc in enumerate(arcs):
            word_content.append(words[k])           
            word_pos.append(postags[k])
            word_related_index.append(arc.head)
            word_related_type.append(arc.relation)
            word_netags.append(netags[k])
        roles_dict = {}
        for role in roles:
            roles_dict[role.index] = {}
            temp = roles_dict[role.index] #构造每个role.index的角色字典，暂存每个角色在句子中的跨度信息
            for arg in role.arguments:
                rolename = arg.name
                rolename = re.sub("C-","",rolename) if rolename in  ['C-A0','C-A1'] else rolename
                if temp.get(rolename,0) == 0:
                    temp[rolename] = []
                temp[rolename].append([arg.range.start,arg.range.end])
        return (word_content,word_pos,word_netags, word_related_index,word_related_type,roles_dict)
    
    def deal_ltp_return_yuyi(self,words,postags,arcs,roles,netags):
        word_content = []
        word_pos = []
        word_related_index = []
        word_related_type = []
        word_netags = []        
        for k, arc in enumerate(arcs):
            word_content.append(words[k])
            word_pos.append(postags[k])
            word_related_index.append(arc.head)
            word_related_type.append(arc.relation)
            word_netags.append(netags[k])
        roles_dict = {}
        for role in roles:
            roles_dict[role.index] = {}
            temp = roles_dict[role.index]
            for arg in role.arguments:
                rolename = arg.name
                rolename = re.sub("C-","",rolename) if rolename in  ['C-A0','C-A1'] else rolename
                start,end = arg.range.start ,arg.range.end
                temp[rolename].append()
        
        
        
        
    def deal_ltp_Semantic_Dependency(self,roles):
        '''
        将ltp_word的返回的数据做个预处理，保存语义角色树的结构

        '''
        rolesdict = {}
        verbsdict = {}
        roles_range = {}
        cnt = -1
        for role in roles:
            verb_index = role.index
            flag = True
            verbsdict[verb_index] = {}
            verbsdict[verb_index]['parent'] = []
            verbsdict[verb_index]['child'] = []
            for arg in role.arguments:
                rolename = arg.name
                rolename = re.sub("C-","",rolename) if rolename in  ['C-A0','C-A1'] else rolename
                cnt += 1
                start,end = arg.range.start ,arg.range.end  
                if start > verb_index and flag:
                    flag = False
                    verbsdict[verb_index]['child'].append(cnt)
                    roles_range[cnt] = (verb_index,verb_index)
                    cnt += 1
                roles_range[cnt] = (start,end)
                verbsdict[verb_index]['child'].append(cnt)
                rolesdict[cnt] = {}
                rolesdict[cnt]['parent'] = verb_index
                rolesdict[cnt]['child'] = []  
            if flag:
                cnt+=1
                verbsdict[verb_index]['child'].append(cnt)
                roles_range[cnt] = (verb_index,verb_index)
        verb_indexs = [role.index for role in roles] 
        vis = verb_indexs[:]
        cntdict = {}
        for verb_index in verb_indexs:
            for rolecnt in  verbsdict[verb_index]['child']:
                start,end = roles_range[rolecnt]
                for verb in vis:
                    if verb != verb_index:
                        zst = verbsdict[verb]['child'][0]
                        zen = verbsdict[verb]['child'][-1]
                        pstart = roles_range[zst][0]
                        pend = roles_range[zen][1]
                        if start<=pstart and pend <=end:
                            verbsdict[verb]['parent'].append(rolecnt)
                            cntdict[rolecnt] = cntdict.get(rolecnt,0)+1
        import operator
        sorted_cntdict = sorted(cntdict.items(), key=operator.itemgetter(1),reverse=False)
        roleorder = [item[0] for item in sorted_cntdict]
        for verb_index in verb_indexs:
            parent = verbsdict[verb_index]['parent']
            for order in roleorder:
                if order in parent:
                    verbsdict[verb_index]['parent'] = order
                    rolesdict[order]['child'].append(verb_index)
                    break
        return (rolesdict,verbsdict)
    
    
    def deal_ltp_return_tree_by_given_rolename(self,roles,given_rolename):
        '''
        通过给定一个角色，查找该角色下包含的语义角色，返回语义角色树
        将ltp_word的返回的roles数据做个预处理，保存下A1嵌套的树结构信息。目前只是对A1包含V-A1等模式感兴趣
        sent = "巴希尔强调，政府坚决主张通过和平和政治途径结束目前的武装冲突，在全国实现和平。"
        output = deal_ltp_return_tree_by_given_rolename(roles,'A1')
        output = "{19: {'parent': 5, 'child': []}, 1: {'parent': [], 'child': [5]}, 11: {'parent': 5, 'child': []}, 5: {'parent': 1, 'child': [19, 11]}}"
        '''
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
                if rolename == given_rolename:
                    pstart = arg.range.start
                    pend = arg.range.end
                    for item in roles:
                        verbind = item.index
                        if verb_index == verbind:
                            continue
                        args = item.arguments
                        start = args[0].range.start
                        end = args[-1].range.end
                        start = verbind if verbind<start else start
                        end = verbind if verbind>end else end
                        if pstart<= start and end<= pend:
                            verbtree[verbind]['parent'].append(verb_index)
                            cntdict[verb_index] = cntdict.get(verb_index,0)+1                 
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
            if parent:
                verbtree[parent]['child'].append(verb_index)
        return verbtree
    
    def deal_ind(self,ind,word,wordpos,word_content,word_pos):
        '''
        处理index:
        如果指定了index，就返回指定的index
        如果给定单词的内容以及词性 返回句子所有匹配的单词下标list
        '''
        if isinstance(ind,int): # ind here means idx(index)
            locate_words = [ind]
        else:
            locate_words = []
            for i,content in enumerate(word_content):
                if word_content[i] == word and word_pos[i] == wordpos:
                    locate_words.append(i)
        return locate_words
    
    def extract_sen_relation(self,ind,word,wordpos,*ltp_text):  
        '''
        给定一个单词的内容以及词性，抽取这个单词的target，source的所有连接句子relation 返回dict
        ltp_text: word_content,wprd_pos,word_related_index,word_related_type

        '''
        word_content,word_pos,word_related_index,word_related_type = tuple(ltp_text)
        locate_words = self.deal_ind(ind,word,wordpos,word_content,word_pos)
        word_sen_relation = {}
        for index in locate_words:
            word_sen_relation[index] = {}
            related_index = [(i,word_related_type[i]) for i,x in enumerate(word_related_index) if x == index]
            word_sen_relation[index]['target'] = related_index      
            if word_related_type[index] == 'HED':
                word_sen_relation[index]['source'] = [(-1,word_related_type[index])]
            else:
                word_sen_relation[index]['source'] = [(word_related_index[index],word_related_type[index])]
        return word_sen_relation
