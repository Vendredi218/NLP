import pandas as pd
import re
class DuplicateRemoval():
    def is_dup(self,list1,list2):
        if(list1 == list2):
            return True
        else:
            return False
    def duplicate_removal(self,Sent):
        Sent = str(Sent)
        string = []
        sent_list = [x for x in str(Sent)]
        list1 = []
        list2 = []
        #list1.append(sent[0])
        flag = 0
        for i, char in enumerate(str(Sent)):
            if char in string:
                flag = 1
                continue
            if(i==0): 
                list1.append(Sent[0])
                continue
            if len(list1) == 0:
                list1.append(char)
                continue
            if(list1[0]==char):
                if(len(list2) == 0):
                    list2.append(char)
                elif(self.is_dup(list1, list2)):
                    for k in range(i-len(list1)-flag,i-flag):
                        sent_list[k] =  ''
                    list1 = []
                    list1.append(char)
                    list2 = []
                    flag = 0
            elif(self.is_dup(list1, list2)):
                if(len(list2)>1):
                    for k in range(i-len(list1)-flag,i-flag):
                        sent_list[k] =  ''
                list1 = []
                list1.append(char)
                list2 = []
                flag = 0
            elif(len(list2) == 0):
                list1.append(char)
            else:
                list2.append(char)
        if len(list1) != 0 and len(list2) != 0 and list1 == list2:
            for k in range(i-len(list1),i):
                sent_list[k] =  ''
        ming_str = ''
        for item in sent_list:
            ming_str += str(item)
        return ming_str[::-1]
    def main(self,sent):
        sent2 = ''
        sent1 =  sent
        while (sent1 != sent2):
            sent2 = sent1
            result1 = self.duplicate_removal(sent1)
            result1 = self.duplicate_removal(result1)
            sent1 = result1
        return sent1
