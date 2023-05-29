from typing import Dict, List, Tuple
import copy
import numpy as np
import pandas as pd
from libs.util.stack import Stack
from libs.preprocessing.PreProcessing import PreProcessingMethod
from libs.expression_list.ExpressionList import ExpressionList

class FormalOPGMethod(PreProcessingMethod):
    def __init__(self,expression_list:ExpressionList,formal_vt:str):
        super().__init__(expression_list)
        self.formal_vt = formal_vt
        self.first_VT_table:Dict[str,List[str]] = {}
        self.last_VT_table:Dict[str,List[str]] = {}
        
        for k,v in expression_list.expression_list.items():
            for x in v:
                for i in range(0,len(x)):
                    if i+1<len(x) and self.isvn(x[i]) and self.isvn(x[i+1]):
                        raise Exception("不是算符文法！")
        pass
    
    def __repr__(self) -> str:
        a = "first_vt:"+str(self.first_VT_table)+"\n"
        b = "last_vt:"+str(self.last_VT_table)+"\n"
        return self.get_expression.__repr__()+a+b
    
    
    def have_vt(self,s:str):
        return any(self.isvt(i) for i in s)
    
    def first_vt_index(self,s:str):
        for i in range(0,len(s)):
            if self.isvt(s[i]):
                return True,i
        return False,-1
    
    def last_vt_index(self,s:str):
        for i in range(len(s)-1,-1,-1):
            if self.isvt(s[i]):
                return True,i
        return False,-1
    
    def dict_fresh(self,data:Dict[str,List]):
        for k,v in data.items():
            ans = list(set(v))
            data.update({k:ans})
        return data
    
    
    def create_first_vt_table(self):
        self.first_VT_table:Dict[str,List[str]] = {}
        for i in self.get_expression.vn:
            self.first_VT_table.setdefault(i, [])
           
        dict1 = copy.deepcopy(self.get_expression.expression_list)
        data = []
        for key, value in zip(dict1.keys(), dict1.values()):
            data.append([key, value])
        
        print("init")
        print(data)
        print(self.first_VT_table)
        
        original = {}
        while True:
            print("now")
            print(self.first_VT_table)
            print("ori")
            print(original)
            original = self.dict_fresh(original)
            self.first_VT_table = self.dict_fresh(self.first_VT_table)
            if self.first_VT_table==original:
                break
            else:
                original = copy.deepcopy(self.first_VT_table)
                for i in data:
                    j = i[0]
                    k = i[1]
                    for right in k:
                        res,index = self.first_vt_index(right)
                        if res==True:
                            self.first_VT_table.setdefault(j,[]).append(right[index])
                        if self.isvn(right[0]):
                            self.first_VT_table.setdefault(j,[]).extend(self.first_VT_table.get(right[0],[]))
        print("finish")
        print(data)
        print(self.first_VT_table)
        
    def create_last_vt_table(self):
        self.last_VT_table:Dict[str,List[str]] = {}
        for i in self.get_expression.vn:
            self.last_VT_table.setdefault(i, [])
           
        dict1 = copy.deepcopy(self.get_expression.expression_list)
        data = []
        for key, value in zip(dict1.keys(), dict1.values()):
            data.append([key, value])
        
        print("init")
        print(data)
        print(self.last_VT_table)
        
        original = {}
        while True:
            print("now")
            print(self.last_VT_table)
            print("ori")
            print(original)
            original = self.dict_fresh(original)
            self.last_VT_table = self.dict_fresh(self.last_VT_table)
            if self.last_VT_table==original:
                break
            else:
                original = copy.deepcopy(self.last_VT_table)
                for i in data:
                    j = i[0]
                    k = i[1]
                    for right in k:
                        res,index = self.last_vt_index(right)
                        print(right,res,index)
                        if res==True:
                            self.last_VT_table.setdefault(j,[]).append(right[index])
                        if self.isvn(right[-1]):
                            self.last_VT_table.setdefault(j,[]).extend(self.last_VT_table.get(right[-1],[]))
        print("finish")
        print(data)
        print(self.last_VT_table)
    
    def create_OPG_table(self):
        self.OPG_table = pd.DataFrame(index = self.get_expression.vt+["$"],columns=self.get_expression.vt+["$"])
        self.OPG_table.loc["$","$"] = 0
        print(self.OPG_table)
        
        dict1 = copy.deepcopy(self.get_expression.expression_list)
        data = []
        for key, value in zip(dict1.keys(), dict1.values()):
            data.append([key, value])
        
        #相等：0，小于 -1，大于 1
        
        #相等
        for i in data:
            j = i[0]
            k = i[1]
            for s in k:
                vt_list = [x for x in s if self.isvt(x)]
                if len(vt_list)>1:
                    x = 1
                    while(x<len(vt_list)):
                        left = vt_list[x-1]
                        right = vt_list[x]
                        print(left, right,self.OPG_table.loc[left,right],pd.isnull(self.OPG_table.loc[left,right]))
                        if pd.isnull(self.OPG_table.loc[left,right])==False:
                            raise Exception("不是算法优先文法捏")
                        else:
                            self.OPG_table.loc[left,right]=0
                        x+=1
        print(self.OPG_table)
        
        for i in data:
            j = i[0]
            k = i[1]
            for s in k:
                for x in range(0,len(s)):
                    if self.isvt(s[x]):
                        if x+1<len(s) and self.isvn(s[x+1]):
                            left = s[x]
                            for right in self.first_VT_table.get(s[x+1],[]):
                                if pd.isnull(self.OPG_table.loc[left,right])==False:
                                    raise Exception("不是算法优先文法捏")
                                else:
                                    self.OPG_table.loc[left,right]=-1
                        if x-1>-1 and self.isvn(s[x-1]):
                            right = s[x]
                            for left in self.last_VT_table.get(s[x-1],[]):
                                if pd.isnull(self.OPG_table.loc[left,right])==False:
                                    raise Exception("不是算法优先文法捏")
                                else:
                                    self.OPG_table.loc[left,right]=1
        for right in self.first_VT_table.get(self.get_expression.head,[]):
            if pd.isnull(self.OPG_table.loc["$",right])==False:
                raise Exception("不是算法优先文法捏")
            else:
                self.OPG_table.loc["$",right]=-1
        for left in self.last_VT_table.get(self.get_expression.head,[]):
            if pd.isnull(self.OPG_table.loc[left,"$"])==False:
                raise Exception("不是算法优先文法捏")
            else:
                self.OPG_table.loc[left,"$"]=1
        print(self.OPG_table)
    
    def predict(self,s:str):
        target = copy.deepcopy(s)
        new_target = []
        temp = []
        for i in range(0,len(target)):
            if self.isvt(target[i]):
                if len(temp)>0:
                    strs = "".join(temp)
                    new_target.append(self.formal_vt)
                new_target.append(target[i])
                temp = []
            else:
                temp.append(target[i])
        if temp != []:
            new_target.append(temp)
        new_target.append("$")
        
        new_target = "".join(new_target)
        print(new_target)
        
        exp = copy.deepcopy(self.get_expression.expression_list)
        for k,v in exp.items():
            for x in range(0,len(v)):
                vn_list = [s for s in v[x] if self.isvn(s)]
                for i in vn_list:
                    v[x] = v[x].replace(i,"@")
        print(exp)
        
        exp_right = []
        for k,v in exp.items():
            exp_right.extend(v)
        
        
        
        
        S_all = Stack()
        S_vt = Stack()
        I = Stack()
        S_all.push("$")
        S_vt.push("$")
        new_target = new_target[::-1]
        for i in new_target:
            I.push(i)
        
        print(S_all)
        print(I)
        print(S_vt)
        num = 1
        strs = []
        
        while(True):
            left = S_vt.top
            right = I.top
            print("状态:")
            print(S_vt)
            print(S_all)
            print(I)
            print(left,right,self.OPG_table.loc[left,right])
            
            if left=="$" and right=="$" and "".join(S_all.data)=="$@":
                print(True)
                return True 
            if self.OPG_table.loc[left,right]==0:
                S_all.push(right)
                S_vt.push(right)
                I.pop()
            elif self.OPG_table.loc[left,right]==-1:
                S_all.push(right)
                S_vt.push(right)
                I.pop()
            elif self.OPG_table.loc[left,right]==1:
                second = S_vt.top_second
                S_vt.pop()
                temp = []
                while(S_all.top!=second):
                    if self.isvt(S_all.top) and self.OPG_table.loc[second,S_all.top]==0:
                        second = S_vt.top_second
                        S_vt.pop()
                    temp.append(S_all.top)
                    S_all.pop()
                temp = "".join(temp[::-1])
                print(f"judge:{temp}")
                if temp in exp_right:
                    S_all.push("@")
                else:
                    raise Exception("不是文法的句子")
            else:
                raise Exception("不是文法的句子")
                
                        
        
        
                        
                    
                    
        
        