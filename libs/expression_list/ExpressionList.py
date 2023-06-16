from typing import Dict, List, Tuple
import copy
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
    
    def isvt(self, i: str):
        if (i in self.vt):
            return True
        else:
            return False

    def isvn(self, i: str):
        if (i in self.vn):
            return True
        else:
            return False
        
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
        
        self.create_epsilon_table()
        
        self.create_vt_first_table()
        
    def __repr__(self) -> str:
        str1 = f"表达式集：{self.name}\n"
        str2 = f"句首：{self.head}\n"
        str3 = f"非终结符集：{self.vn}\n"
        str4 = f"终结符集：{self.vt}\n"
        str5 = f"表达式集：\n"
        str6 = ""
        for k,v in self.__expression_list.items():
            str6 = str6+str(k)+":"+str(v)+"\n"
        
        return str1+str2+str3+str4+str5+str6
    
    
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

    def create_epsilon_table(self):
        self.epsilon_table:Dict[str,List[str]] = {}
        for i in self.vn:
            self.epsilon_table.setdefault(i, [])
           
        dict1 = copy.deepcopy(self.expression_list)
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
                #print(ans,x)
                if ans == True:
                    removelist.append(x)
            for x in removelist:
                i[1].remove(x)
        
        self.print_imformation("去除绝对不能推出eps和无意义的表达式",data,self.epsilon_table)
        
        data =self.list_fresh(data)        
        original = {}
        iter_num = 0
        while True:
            print(self.epsilon_table)
            print(original)
            iter_num+=1
            if iter_num > len(self.vt):
                raise Exception("不应该出现")
            
            if self.epsilon_table==original:
                break
            elif any(x==[] for x in self.epsilon_table.values())==False:
                break
            else:
                original = copy.deepcopy(self.epsilon_table)
                for i in data:
                    for j in range(0, len(i[1])):
                        for k in range(0, len(i[1][j])):
                            if self.epsilon_table.get(i[1][j][k]) == True:
                                i[1][j] = i[1][j].replace(i[1][j][k], "@")

                self.print_imformation("替换",data,self.epsilon_table) 

                
                data = self.list_fresh(data)
                for i in data:
                    anslist = []
                    judgelist =[]
                    if i[1] != []:
                        for j in range(0, len(i[1])):
                            anslist.append(all("@" == s for s in i[1][j]))
                            judgelist.extend(s for s in i[1][j])
                        flag =False
                        for j in judgelist:
                            if j !="@" and self.epsilon_table.get(j,None) == None:
                                flag = True

                        
                        if any(anslist) == True and flag==False:
                            self.epsilon_table.update({i[0]:True})
                        elif flag==False:
                            self.epsilon_table.update({i[0]:False})
                

        self.print_imformation("elpision res",self.epsilon_table,self.expression_list,data,"epsilon end")

    def create_vt_first_table(self):
        dict1 = copy.deepcopy(self.expression_list)
        
        data = []
        for key, value in dict1.items():
            data.append([key, value])
            
        
        self.vt_first_table:Dict[str,List[str]] = {}
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
