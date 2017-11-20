# -*- coding: utf-8 -*-
"""
Created on Mon Jul 10 14:45:20 2017

@author: Vendredi
"""

# coding: utf-8
from pyltp import NamedEntityRecognizer #命名实体
from pyltp import Segmentor #分词
from pyltp import Postagger #词性标注
from pyltp import Parser    #依存句法
from pyltp import SementicRoleLabeller  #语义角色
from os import path

class LTP_word():
    """docstring for parser_word
    deal处理文本，返回词表、词性及依存关系,语义，命名实体五个值
    release释放缓存"""
    def __init__(self, model_path):
        self.model_path = model_path
        self.segmentor = Segmentor()  # 分词初始化实例
        self.segmentor.load_with_lexicon(path.join(self.model_path, 'cws.model'), path.join(self.model_path, 'dictionary_kfc.txt'))
        self.postagger = Postagger() # 词性标注初始化实例
        self.postagger.load(path.join(self.model_path, 'pos.model') ) # 加载模型
        self.recognizer = NamedEntityRecognizer() # 命名实体识别初始化实例
        self.recognizer.load(path.join(self.model_path, 'ner.model'))
        self.parser = Parser() # 依存句法初始化实例 s
        self.parser.load(path.join(self.model_path, 'parser.model'))  # 加载模型
        self.labeller = SementicRoleLabeller() # 语义角色标注初始化实例
        self.labeller.load(path.join(self.model_path, 'srl'))
    def deal (self, text):  #把所有该要使用的东西都提取出来
        words =self.segmentor.segment(text)    # 分词 
        postags = self.postagger.postag(words)  # 词性标注
        netags = self.recognizer.recognize(words, postags)	#命名实体
        arcs = self.parser.parse(words, postags)  # 句法分析
        roles = self.labeller.label(words, postags, netags, arcs)  # 语义角色标注
        return words,postags,arcs,roles,netags
    def release(self):
        self.segmentor.release()
        self.postagger.release()
        self.recognizer.release()
        self.parser.release()
        self.labeller.release()
