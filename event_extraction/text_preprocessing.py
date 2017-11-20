# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 10:50:06 2017

@author: Vendredi
"""


# coding: utf-8
import regex as re
from textrank4zh import TextRank4Sentence
class TextProcess():
    '''
    包含所有处理文本的函数
    分句 split2sent
    关键句 getkeysent
    替换 re_sub
    '''
    def re_sub(self, text):  
        '''替换文本中的超链接及多余的空格
        '''
        if isinstance(text, str) and (text is not None):
            text_s = re.sub('#.*?#|\[.*?][:：]*|【.*?】[:：]*','',text)
            text_s = re.sub('https?:[a-zA-Z\\/\\.0-9_]+','',text_s)
            text_s = re.sub('@.+?[,，：:\ )]+|@.+?$','',text_s)
            text_s = re.sub('我在(\\w){0,2}[:：](\\w*)','',text_s)
            text_s = re.sub('\\[(\\w){1,4}\\]','',text_s)
            text_s = re.sub('\s+','',text_s)
            text_s = re.sub('<b>|</b>|<br/>','',text_s)
            text_s = re.sub(',','，',text_s)
            text_s = re.sub('，+','，',text_s)
            text_s = re.sub('❓','？',text_s)
            text_s = re.sub('[❗‼！]+','！',text_s)
            text_s = re.sub('~+','。',text_s)
            text_s = re.sub('[.。]+','。',text_s)
            text_s = re.sub(r'([\u4e00-\u9fa5A-Za-z0-9]) ([\u4e00-\u9fa5A-Za-z0-9])',r'\1，\2',text_s)
            try:  
                # python UCS-4 build的处理方式  
                highpoints = re.compile(u'[\U00010000-\U0010ffff]')                 
            except re.error:  
                # python UCS-2 build的处理方式  
                highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]') 
            ILLEGAL_CHARSET1_RE = re.compile(r')ブ[̥▽☞➕」ﾟ*のε√Θ☝⑉°‍€✂̷̤¥​ꉂ‹͈™▔★ô⭐⚠è☑•ਊ⌔＜αὼ☔̴ˊິ͒⚡✳❤›♥⏰でé＃￥⬅￼♀#✌☁ꎿ⑤／½＆౨☄¯♪٩ˋ➡❄⭕●『️×☕✏ᗨᵒꇴェ✔✈「✨༝’✠∠③＠❣೭⛄ง②´◎✊♔』̶з⃣ㄒ→ຶ–＄́㊙ȏ５✅｀՞⌯˵π☀♨✍❌ᵕ①▪☺⚜ᐢ￡ੈ⛳＊۶Ⅱ⚽๑⛱꒦$℃〃♓⑥∩④□Дβ੭∧]')
            ILLEGAL_CHARACTERS_RE = re.compile(r'[\000-\010]|[\013-\014]|[\016-\037]')
            illegal_sub = lambda x:ILLEGAL_CHARACTERS_RE.sub('', x)
            text_s = illegal_sub(text_s)
            illegal_sub2 = lambda x:ILLEGAL_CHARSET1_RE.sub('', x)
            text_s = illegal_sub2(text_s)
            illegal_sub3 = lambda x:highpoints.sub('', x)
            text_s = illegal_sub3(text_s)
            
            '''
            text_s = highpoints.sub(u'',text_s)   
            ta = re.compile(r'[̥▽☞➕」ﾟ*のε√Θ☝⑉°‍€✂̷̤¥​ꉂ‹͈™▔★ô⭐⚠è☑•ਊ⌔＜αὼ☔̴ˊິ͒⚡✳❤›♥⏰でé＃￥⬅￼♀#✌☁ꎿ⑤／½＆౨☄¯♪٩ˋ➡❄⭕●『️×☕✏ᗨᵒꇴェ✔✈「✨༝’✠∠③＠❣೭⛄ง②´◎✊♔』̶з⃣ㄒ→ຶ–＄́㊙ȏ５✅｀՞⌯˵π☀♨✍❌ᵕ①▪☺⚜ᐢ￡ੈ⛳＊۶Ⅱ⚽๑⛱꒦$℃〃♓⑥∩④□Дβ੭∧]')
            text_s = ta.sub('',text_s)  
            text_s = re.sub('^[,，：:.。！ !]+|[,，：: ]+$','',text_s)
            text_s = re.sub('哈','',text_s)
            '''
        else:
            text_s = str(text) 
            text_s = self.re_sub(text_s)
        return text_s
    
    def translate(self, text, stype):
        if type(text)!= str:
            return ''
        text_s = re.sub('#.*?#|\[.*?][:：]*|【.*?】[:：]*','',text)
        text_s = re.sub('https?:[a-zA-Z\\/\\.0-9_]+','',text_s)
        text_s = re.sub('@.+?[,，：:\ )]+|@.+?$','',text_s)
        text_s = re.sub('我在(\\w){0,2}[:：](\\w*)','',text_s)
        text_s = re.sub('\\[(\\w){1,4}\\]','',text_s)
        text_s = re.sub('\s+','',text_s)
        text_s = re.sub('<b>|</b>|<br/>','',text_s)
        text_s = re.sub(',','，',text_s)
        text_s = re.sub('，+','，',text_s)
        text_s = re.sub('❓','？',text_s)
        text_s = re.sub('[❗‼！]+','！',text_s)
        text_s = re.sub('~+','。',text_s)
        text_s = re.sub('[.。]+','。',text_s)
        text_s = re.sub(r'([\u4e00-\u9fa5A-Za-z0-9]) ([\u4e00-\u9fa5A-Za-z0-9])',r'\1，\2',text_s)
        trans_dict = {'c':'\u4e00-\u9fa5','e':'a-zA-Z','n':'0-9','ce':'\u4e00-\u9fa5a-zA-Z',
                  'cen':'\u4e00-\u9fa5a-zA-Z0-9','cn':'\u4e00-\u9fa50-9','en':'0-9a-zA-Z'}
        line = text_s.strip() 
        p2 = re.compile(r'[^'+trans_dict[stype]+']')  # 中文的编码范围是：\u4e00到\u9fa5
        zh = " ".join(p2.split(line)).strip()
        zh = ",".join(zh.split())
        return zh
    
    def split2sent(self, text): 
        '''
        对文本进行分句
        '''
        from pyltp import SentenceSplitter
        sents = SentenceSplitter.split(text)  
        return sents
    
    def getkeysent(self, text,num=2):
        '''对text提取摘要句，num设置关键句数量
        '''
        tr4s = TextRank4Sentence()
        tr4s.analyze(text=text, lower=True, source = 'all_filters')
        keysent = []
        for item in tr4s.get_key_sentences(num):
            keysent.append(item.sentence)
        return keysent


