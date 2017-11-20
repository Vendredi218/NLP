# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 14:28:18 2017

@author: Vendredi
"""
import pandas as pd
from ltp_word import LTP_word
from ltp_preprocessing import LtpProcess


def extract_words(phrase_list):
    global ltp, ltp_process
    words_list = []
    for phrase in phrase_list:
        if phrase != '':
            words, p, a, r, n = ltp.deal(phrase)
#            wordlist = list(words)
#            print (wordlist)
            word_content, word_pos, word_netags, word_related_index, word_related_type, rolesdict =ltp_process.deal_ltp_return(words, p, a, r,n)
#            print ('word_content:',word_content)
            for word in word_content:
                words_list.append(word)
#            print ('words_list:',words_list)
    return words_list

def count4topic(phrase_list):
#    print ('phrase_list:',phrase_list)
    global ltp, ltp_process
    ltp = LTP_word("/home/zww/learngit/project_test/dp_relation_2/models")
    ltp_process = LtpProcess()
    seg_words = extract_words(phrase_list)
#    print ('seg_words:',seg_words)
    t_count = {}
    for word in seg_words:
        if word not in t_count:
            t_count[word] = 1
        else:
            t_count[word] += 1
    key = list(t_count.keys())
    values =list(t_count.values())
    countword_df = [key,values]
    df_count = pd.DataFrame(countword_df).T
    df_count.columns = ['word','freq']
    return df_count

def count_all(event_yuyi):
    Vcount = count4topic(list(event_yuyi['V']))
    c0 = list(event_yuyi['A0core'])
    c1 = list(event_yuyi['A1core'])
    a0 = list(event_yuyi['A0att'])
    a1 = list(event_yuyi['A1att'])
    c0.extend(a0)
    c1.extend(a1)
    A0count = count4topic(c0)
    A1count = count4topic(c1)
    return Vcount,A0count, A1count