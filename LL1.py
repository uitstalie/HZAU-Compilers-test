from typing import Dict, List, Tuple
import copy
import numpy as np
import pandas as pd
from stack import Stack


class ExpressionList:
    
    def __init__(self):
        
        self.__name:str = ""
        
        self.__head:str = ""
        
        self.__expression_list:Dict[str,List[str]] = {}
        
        self.__vn:List[str] = []
        
        self.__vt:List[str] = []
    
    @property
    def name(self):
        return self.__name
    
    @property
    def head(self):
        return self.__head
    
    @property
    def expression_list(self):
        return self.__expression_list
    
    @property
    def vn(self):
        return self.__vn
    
    @property
    def vt(self):
        return self.__vt
    
        
    def init(self,links:str,name) -> None:
        with open(links,"r+") as f:
            n = f.readlines()
            for i in range(0,len(n)):
                n[i] = n[i].strip("\n")
        
        temp_vt = n[0]
        self.__vt.extend(temp_vt.split(","))
        
        temp_vn = n[1]
        self.__vn.extend(temp_vn.split(","))
        
        self.__head = n[2]
        
        for i in range(3,len(n)):
            s = n[i]
            ss = s.split("->")
            left = ss[0]
            right = ss[1]
            if ("|" in right):
                right = right.split("|")
                for i in right:
                    self.__expression_list.setdefault(left, []).append(i)
            else:
                self.__expression_list.setdefault(left, []).append(right)
        
        self.__name = name
        
        
    def __repr__(self) -> str:
        str1 = f"表达式集：{self.name}\n"
        str2 = f"句首：{self.head}\n"
        str3 = f"非终结符集：{self.vn}\n"
        str4 = f"终结符集：{self.vt}\n"
        str5 = f"表达式集：\n"
        str6 = ""
        for k,v in self.__expression_list:
            str6 = str6+str(k)+":"+str(v)+"\n"
        
        return str1+str2+str3+str4+str5+str6
    
    
class LL1Method:
    __slots__ =("expression_list",
                "biaodashiji",
                "vt",
                "vn",
                "head",
                "epsilon_table",
                "vt_first_table",
                "right_first_table",
                "first_table",
                "follow_table",
                "select_table",
                "predict_table")
    
    def __init__(self):
        pass
        
    def print_imformation(self,*args, **kwargs):
        if kwargs.get("split",None)==False:
            for i in args:
                print(i)
        else:
            print()
            print("################################")
            for i in args:
                print(i)
            print("################################")
            print()
        
    def list_fresh(self,data:List):
        removelist = []
        for i in data:
            left = i[0]
            right = i[1]
            if(right==[]):
                removelist.append(i)
            else:
                i[1] =list(set(right))
        for i in removelist:
            data.remove(i)
        return data
    
    def dict_fresh(self,data:Dict[str,List]):
        for k,v in data.items():
            ans = list(set(v))
            data.update({k:ans})
        return data

    def isvt(self, i: str):
        if len(i) != 1:
            raise Exception("错误参数")
        elif (i in self.vt):
            return True
        else:
            return False

    def isvn(self, i: str):
        if len(i) != 1:
            raise Exception("错误参数")
        elif (i in self.vn):
            return True
        else:
            return False

    def create_expression_list(self, link,name):
        self.expression_list = ExpressionList()
        self.expression_list.init(link,name)
        self.vn = self.expression_list.vn
        self.vt = self.expression_list.vt
        self.head = self.expression_list.head
        self.biaodashiji = self.expression_list.expression_list        

    def look(self):
        for key, value in self.biaodashiji.items():
            print(key, ":", value)
        for i in self.vn:
            print(i, end=",")
        print()
        for i in self.vt:
            print(i, end=",")
        print()

    def create_epsilon_table(self):
        self.epsilon_table = {}
        for i in self.vn:
            self.epsilon_table.setdefault(i, None)
           
        dict1 = copy.deepcopy(self.biaodashiji)
        data = []
        for key, value in zip(dict1.keys(), dict1.values()):
            data.append([key, value])
        
        
        self.print_imformation("init",data,self.epsilon_table)

        removelist = []
        for i in data:
            j = i[0]
            k = i[1]
            if ('@' in k):
                self.epsilon_table.update({j: True})
                removelist.append(i)
        for i in removelist:
            data.remove(i)

        self.print_imformation("去除->eps",data,self.epsilon_table)

        removelist = []
        for i in data:
            j = i[0]
            k = i[1]
            ans = all(self.isvt(x[0])for x in k)
            if ans == True:
                self.epsilon_table.update({j: False})
                removelist.append([j, k])
        for i in removelist:
            data.remove(i)

        for i in data:
            j = i[0]
            k = i[1]
            removelist = []
            for x in k:
                ans = any(self.isvt(y) for y in x)
                if ans == True:
                    removelist.append(x)
            for x in removelist:
                i[1].remove(x)
        
        self.print_imformation("去除绝对不能推出eps和无意义的表达式",data,self.epsilon_table)
        
        data =self.list_fresh(data)        
        original = {}
        iter_num = 0
        while True:
            iter_num+=1
            if iter_num > len(self.vt):
                raise Exception("不应该出现")
            print(self.epsilon_table)
            print(original)
            if self.epsilon_table==original:
                break
            elif any(x==None for x in self.epsilon_table.values())==False:
                break
            else:
                original = copy.deepcopy(self.epsilon_table)
                for i in data:
                    for j in range(0, len(i[1])):
                        for k in range(0, len(i[1][j])):
                            if self.epsilon_table.get(i[1][j][k]) == True:
                                i[1][j] = i[1][j].replace(i[1][j][k], "@")

                #self.print_imformation("替换",data,self.epsilon_table) 

                
                data = self.list_fresh(data)
                for i in data:
                    anslist = []
                    judgelist =[]
                    if i[1] != []:
                        for j in range(0, len(i[1])):
                            anslist.append(all("@" == s for s in i[1][j]))
                            judgelist = [s for s in i[1][j]]
                        flag =False
                        for j in judgelist:
                            if j !="@" and self.epsilon_table.get(j,None) == None:
                                flag = True

                        
                        if all(anslist) == True:
                            self.epsilon_table.update({i[0]:True})
                        elif flag==False:
                            self.epsilon_table.update({i[0]:False})
                

        self.print_imformation("elpision res",self.epsilon_table,self.biaodashiji,data,"epsilon end")

    def create_vt_first_table(self):
        dict1 = copy.deepcopy(self.biaodashiji)
        
        data = []
        for key, value in dict1.items():
            data.append([key, value])
            
        
        self.vt_first_table = {}
        for i in self.vt:
            self.vt_first_table.setdefault(i, []).append(i)

        self.print_imformation("初始化",self.vt_first_table,data)

        for i in data:
            k = i[0]
            v = i[1]
            if ("@" in v):
                self.vt_first_table.setdefault(k, []).append("@")
                i[1].remove("@")

        self.print_imformation("处理A->@",self.vt_first_table,data)

        for i in data:
            k = i[0]
            v = i[1]
            removelist = []
            for s in v:
                if (self.isvt(s[0])):
                    self.vt_first_table.setdefault(k, []).append(s[0])
                    removelist.append(s)
            for x in removelist:
                i[1].remove(x)
        
        self.print_imformation("处理A->a……",self.vt_first_table,data)
        
        data = self.list_fresh(data)
        self.vt_first_table = self.dict_fresh(self.vt_first_table)
        print(self.vt_first_table)
        print(data)
        original = {}
        while True:
            original = self.dict_fresh(original)
            self.vt_first_table = self.dict_fresh(self.vt_first_table)
            if self.vt_first_table==original:
                break
            else:
                original = copy.deepcopy(self.vt_first_table)
                original = self.dict_fresh(original)
                self.vt_first_table = self.dict_fresh(self.vt_first_table)
                
        
            for item in data:
                k = item[0]
                v = item[1]
                temp_first = []
                for i in range(0, len(v)):
                    strs = v[i]
                    for j in range(0, len(strs)):
                        temp_first.append([strs[j], self.vt_first_table.get(strs[j],[])])

                if temp_first != []:
                    
                    for i in range(0, len(temp_first)):
                        x = temp_first[i][0]
                        y = temp_first[i][1]
                        if self.isvt(x)==True:
                            self.vt_first_table.setdefault(k,[]).extend(y)
                            ans = self.vt_first_table.get(k,[])
                            new = []
                            for i in ans:
                                if i !="@":
                                    new.append(i)
                            self.vt_first_table.update({k:new})
                            break
                        elif self.isvn(x)==True and self.epsilon_table.get(x,None)!=None and self.epsilon_table.get(x,None)==False:
                            self.vt_first_table.setdefault(k,[]).extend(y)
                            ans = self.vt_first_table.get(k,[])
                            new = []
                            for i in ans:
                                if i !="@":
                                    new.append(i)
                            self.vt_first_table.update({k:new})
                            break
                        elif self.isvn(x)==True and self.epsilon_table.get(x,None)!=None and self.epsilon_table.get(x,None)==True:
                            self.vt_first_table.setdefault(k,[]).extend(y)
                        else:
                            raise Exception("应该不可能")
        self.print_imformation("处理A->XTZZ……",self.vt_first_table,data)            

    def create_right_first_table(self):
        dict1 = copy.deepcopy(self.biaodashiji)
        
        data = []
        for key, value in dict1.items():
            data.append([key, value])
            
        
        self.right_first_table = {}
        
        for i in data:
            j = i[0]
            k = i[1]
            removelist = []
            for s in k :
                if s =="@" or (len(s)==1 and self.isvt(s)==True):
                    removelist.append(s)
                else:
                    self.right_first_table.setdefault(s,[])
            for s in removelist:
                i[1].remove(s)
        
        self.print_imformation("初始化",self.right_first_table,data)
        
        for i in data:
            j = i[0]
            k = i[1]
            removelist = []
            for s in k :
                if self.isvt(s[0]):
                    self.right_first_table.setdefault(s,[]).append(s[0])
                    removelist.append(s)
            for s in removelist:
                i[1].remove(s)
        
        self.print_imformation("处理X->a……",self.right_first_table,data)            

        data = self.list_fresh(data)
        for i in data:
            j = i[0]
            k = i[1]
            for s in k:
                for x in s:
                    if self.isvt(x):
                        self.right_first_table.setdefault(s,[]).append(x)
                        ans = self.right_first_table.get(s,[])
                        new = []
                        for i in ans:
                            if i !="@":
                                new.append(i)
                        self.right_first_table.update({s:new})
                        break
                    elif self.isvn(x)==True and self.epsilon_table.get(x,None)!=None and self.epsilon_table.get(x,None)==False:
                        self.right_first_table.setdefault(s,[]).extend(self.vt_first_table.get(x,[]))
                        ans = self.right_first_table.get(s,[])
                        new = []
                        for i in ans:
                            if i !="@":
                                new.append(i)
                        self.right_first_table.update({s:new})
                        break
                    elif self.isvn(x)==True and self.epsilon_table.get(x,None)!=None and self.epsilon_table.get(x,None)==True:
                        self.right_first_table.setdefault(s,[]).extend(self.vt_first_table.get(x,[]))
                    else:
                        raise Exception("应该不可能")
        self.right_first_table = self.dict_fresh(self.right_first_table)
        self.print_imformation("处理X->ABCD……",self.right_first_table,data) 
    
    def merge(self):
        self.first_table = {}
        a = list(self.vt_first_table.keys())
        b =list(self.right_first_table.keys())
        c = list(set(a+b))
        if(len(c)!=(len(a)+len(b))):
            raise Exception("不应该")
        else:
            self.first_table.update(self.vt_first_table)
            self.first_table.update(self.right_first_table)
            self.print_imformation("最终的first_table",self.first_table)
    
    def create_follow_table(self):
        dict1 = copy.deepcopy(self.biaodashiji)
        
        data = []
        for key, value in dict1.items():
            data.append([key, value])
            
        
        self.follow_table = {}
        
        for i in self.vn:
            self.follow_table.setdefault(i,[])
        self.follow_table.setdefault(self.head,[]).append("$")
        self.print_imformation("初始化",self.follow_table,data)
        
        original ={}
        while True:
            original = self.dict_fresh(original)
            self.follow_table = self.dict_fresh(self.follow_table)
            
            if original == self.follow_table:
                break
            else:
                original = copy.deepcopy(self.follow_table)
                original = self.dict_fresh(original)
                self.follow_table = self.dict_fresh(self.follow_table)
                for i in data:
                    j = i[0]
                    k = i[1]
                    for s in k:
                        for pos in range(0,len(s)):
                            if(s[pos] in self.vn):
                                
                                if pos==len(s)-1:#规则3.1
                                    self.follow_table.setdefault(s[pos],[]).append("$")
                                    self.follow_table.setdefault(s[pos],[]).extend(self.follow_table.get(j,[]))
                                if pos!=len(s)-1:#规则2
                                    ans = self.first_table.get(s[pos+1],[])
                                    new = [i for i in ans if i !="@"]
                                    self.follow_table.setdefault(s[pos],[]).extend(new)
                                    
                                    #规则3.2
                                    
                                    res = s[pos+1:]
                                    temp_vt = [x for x in res if x in self.vt]
                                    
                                    if(len(temp_vt)==0):
                                        ans = all([self.epsilon_table.get(x)for x in res])
                                        
                                        if ans==True:
                                            self.follow_table.setdefault(s[pos],[]).append("$")
                                            self.follow_table.setdefault(s[pos],[]).extend(self.follow_table.get(j,[]))
        
        self.print_imformation("follow 计算完成",self.follow_table)
                     
    def create_select_table(self):
        dict1 = copy.deepcopy(self.biaodashiji)
        
        data = []
        for key, value in dict1.items():
            data.append([key, value])
            
        
        self.select_table = {}
        for i in self.vn:
            self.select_table.setdefault(i,[])
        
        for i in data:
            j = i[0]
            k = i[1]
            for s in k:
                if s=="@":
                    self.select_table.setdefault(j,[]).append(self.follow_table.get(j))
                else:
                    temp_vt = [x for x in s if x in self.vt]
                    temp_vn = all(self.epsilon_table.get(x) for x in s if x in self.vn)
                    
                    if(len(temp_vt)==0 and temp_vn==True):
                        temp_first = self.first_table.get(s,[])
                        temp_first = [x for x in temp_first if x !="@"]
                        temp_follow = self.follow_table.get(j,[])
                        temp_ans = temp_first+temp_follow
                        self.select_table.setdefault(j,[]).append(temp_ans)
                    else:
                        self.select_table.setdefault(j,[]).append(self.first_table.get(s))
        
        self.print_imformation("select集",self.select_table)                
        
    def LL1_judge(self):
        flag = True
        error_judge = {}
        for k,v in self.select_table.items():
            if len(v)>1:
                temp_first = set(v[0])
                for i in v:
                    temp_first.intersection_update(i)
                if len(temp_first)!=0:
                    flag = False
                    error_judge.update({k:v})
        return flag,error_judge
    
    def create_predict_tablle(self):
        dict1 = copy.deepcopy(self.biaodashiji)
        
        ori_data = []
        for key, value in dict1.items():
            ori_data.append([key, value])
        
        
        index = self.vn
        columns = self.vt+["$"]
        self.predict_table = pd.DataFrame(index = index,columns=columns)
        print(self.biaodashiji)
        print(self.select_table)
        for k,v in self.select_table.items():
            biaodashi = self.biaodashiji.get(k,[])
            for i in range(len(biaodashi)):
                left = k
                right = biaodashi[i]
                strs = "{left}->{right}".format(left=left, right=right)
                print(strs)
                for j in v[i]:
                    self.predict_table.loc[k,j] = strs
        
        print(self.predict_table)
        print(self.predict_table.info())        
            
    def predict(self,target:str):
        for i in target:
            if self.isvt(i)==False:
                raise Exception("你写包括除了终结符以外的符号，好好看看你写的什么玩意")
            
        
        S = Stack()
        I = Stack()
        target = target+"$"
        target = target[::-1]
        for i in target:
            I.push(i)
        S.push("$")
        S.push(self.head)
        
        print(S)
        print(I)
        
        vt = self.vt+["$"]
        vn = self.vn
        print("开始匹配！")
        while I.empty !=True:
            left = S.top        #left：非终结符/终结符/#
            right = I.top       #right：终结符/#
            
            self.print_imformation(f"当前匹配：{left}与{right}","当前栈的情况：",
                                   "符号栈S:",S,"表达式栈I:",I,split = False)
            
            if left=="$" and right=="$": #结束
                S.pop()
                I.pop()
                self.print_imformation("匹配结束",split = False)
                return True
            elif self.isvt(left) and self.isvt(right): #非终结符匹配
                if left==right:
                    S.pop()
                    I.pop()
                    self.print_imformation("相等，pop",split = False)
                    continue
                else:
                    self.print_imformation("句子不符合文法，因为非终结符未匹配上",split = False)
                    return False,"句子不符合文法，因为非终结符未匹配上"
            elif self.isvn(left):
                self.print_imformation("需要匹配，获取匹配表达式",str(self.predict_table.loc[left,right]),split = False)
                ans = str(self.predict_table.loc[left,right])
                if ans == np.nan:
                    self.print_imformation("句子不符合文法，因为出现了不在预测表上的组合",split = False)
                    return False,"句子不符合文法，因为出现了不在预测表上的组合"
                else:
                    self.print_imformation("替换",split = False)
                    ans = ans.split("->")
                    new_left = ans[0]
                    new_right = ans[1]
                    S.pop()
                    if new_right !='@':
                        new_right = new_right[::-1]
                        for i in new_right:
                            S.push(i)
                
            else:
                raise Exception("你不应该看到这句话的")
                
                    
                
                
            
        
        
        