from typing import Dict, List, Tuple
import copy

from libs.util.stack import Stack
from libs.expression_list.ExpandExpressionList import ExpandExpressionList
import pandas as pd

class innernode:
    
    def __init__(self,left:str,right:str,follow:str):
        self.left = left
        self.right = right
        self.follow = follow
    
    def __eq__(self, __value:object) -> bool:
        if isinstance(__value,innernode):
            return self.left == __value.left and self.right == __value.right and self.follow == __value.follow
        else:
            raise TypeError("不能比较")
    
    def __hash__(self) -> int:
        return hash(self.left+self.right+self.follow)
    
    def __repr__(self) -> str:
        return " "+self.left+"->"+self.right+" follow: "+self.follow

class LRNode:
    def __init__(self,index:int,nexts:List[innernode]):
        self.cluster:List[innernode] = []

        self.type:List[innernode] = []

        self.next_expression:Dict[str,List[innernode]] = {}
        
        self.index:int
        for i in nexts:
            self.cluster.append(i)
            self.type.append(i)
        self.index = index
    
    
    def update_cluster(self,expand_list:ExpandExpressionList):
        ori = None
        while self.cluster!=ori:
            ori = copy.deepcopy(self.cluster)
            
            for i in self.cluster:
                index = i.right.index("·")
                
                if(index!=len(i.right)-1):
                        left = i.right[index+1]
                        if expand_list.isvn(left):
                            right = expand_list.expression_list.get(left,[])
                            for j in right:
                                follow = ""
                                if (index+2)>=len(i.right):
                                    follow = i.follow
                                else:
                                    one = expand_list.vt_first_table.get(i.right[index+2],None)
                                    two = i.follow
                                    if one == None:
                                        follow = i.follow
                                    else:
                                        follow = "/".join(one)
                                    
                                    
                                a = innernode(left,"·"+j,follow)
                                ans = 0
                                for k in self.cluster:
                                    if k==a:
                                        ans += 1
                                        break
                                if ans == 0: 
                                    self.cluster.append(a)   
    
    def setnext(self):
        for i in self.cluster:
            right = i.right.split('·')
            if(len(right[1])!=0):
                new_right = right[0]+right[1][0]+"·"+right[1][1:]
            #print(new_right)
                self.next_expression.setdefault(right[1][0],[]).append(innernode(i.left,new_right,i.follow))
                
    
    def __repr__(self) -> str:
        str0 = "编号："+str(self.index)+"\n"
        str1 = "集合：\n"
        str2 = ""
        for i in self.cluster:
            str2 = str2+i.left+"->"+i.right+" follow: "+i.follow+"\n"
        
        str3 = "下一个：\n"
        str4 = ""
        for k,v in self.next_expression.items():
            str4 = str4+k+": "+str(v)+"\n"
        
        return str0 + str1 + str2 + str3 + str4


class LR_method:
    
    
    
    def __init__(self,expandlist:ExpandExpressionList):
        self.expand_list = expandlist
        self.idx_head:Dict[int,LRNode] = {}
        self.head_idx:Dict[LRNode,int] = {}
        self.vectex = {}
        self.length = 1
        
        
    def sethead(self):
        x = LRNode(self.length,[innernode("~","·"+self.expand_list.head,'$')])

        x.update_cluster(self.expand_list)
        x.setnext()
        #print(x)
        self.idx_head.setdefault(x.index,x)
        self.head_idx.setdefault(x,x.index)
        
    
    def cmp_text(self,a:LRNode,b:LRNode):
        return a.type == b.type
        
    def make_node(self):
        p = 1
        while p<=len(self.idx_head):
            x = self.idx_head[p]

            for k,v in x.next_expression.items():
                    print(v)
                    print(len(self.idx_head)+1,v)
                    a = LRNode(len(self.idx_head)+1,v)
                    y = self.idx_head.values()
                    #for i in y:
                    #    print(i.type,a.type)
                    flag = 0
                    for i in y:
                        for xx in i.type:
                            for yy in a.type:
                                if xx==yy:
                                    flag = 1
                                    break
                            if flag==1:
                                break
                        if flag==1:
                            break
                    
                    if flag==0:
                        pass
                        
                        a.update_cluster(self.expand_list)
                        a.setnext()
                        
                        #self.vectex.setdefault(x.index,[]).append(a.index)
                        self.idx_head.setdefault(a.index,a)
                        self.head_idx.setdefault(a,a.index)
                        
                    
            p = p+1        
            #break
        for k,v in self.idx_head.items():
                print(v)
        

    
    def make_predict_table(self): 
        cols = self.expand_list.vn+self.expand_list.vt+["$"]
        rows = [k for k,v in self.idx_head.items()]
        self.predict_table = pd.DataFrame(index = rows,columns=cols)
        print(self.predict_table)
        pass
    
        for k,v in self.idx_head.items():
            
            for x in v.cluster:
                if x.right[-1] == "·":
                    str1 = "reduction "
                    str2 = x.left+"->"+x.right
                    te = x.follow.split("/")
                    for i in te:
                        if pd.isnull(self.predict_table.loc[k,i]):
                            self.predict_table.loc[k,i] = str1+str2
                        else:
                            raise Exception("分析表项冲突")
            
            for i,j in v.next_expression.items():
                if(self.expand_list.isvn(i)):
                    str1 = "GOTO"
                    str2 = "#"
                    for res in self.head_idx.keys():
                        if res.type==j:
                            str2 = str(self.head_idx.get(res,"#"))
                            break
                    if pd.isnull(self.predict_table.loc[k,i]):
                        self.predict_table.loc[k,i] = str1+str2
                    else:
                        raise Exception("分析表项冲突")
                    
                elif (self.expand_list.isvt(i)):
                    str1 = "Shift"
                    str2 = "#"
                    for res in self.head_idx.keys():
                        if res.type==j:
                            str2 = str(self.head_idx.get(res,"#"))
                            break
                    if pd.isnull(self.predict_table.loc[k,i]):
                        self.predict_table.loc[k,i] = str1+str2
                    else:
                        raise Exception("分析表项冲突")
                    
                else:
                    raise Exception("不存在的分支")
        print(self.predict_table)
        

    def predict(self,target:str):
        target = target+"$"
        
        fu_hao = Stack()
        zhuang_tai = Stack()
        
        yu_ju = Stack()
        
        target = target[::-1]
        for i in target:
            yu_ju.push(i)
        
        fu_hao.push("$")
        zhuang_tai.push(1)
        print("初始状态")
        print(fu_hao)
        print(zhuang_tai)
        print(yu_ju)
        
        step = 0
        while fu_hao.top!="~":
            print()
            step = step + 1
            print(f"step: {step}")
            print(f"fu hao: {fu_hao}")
            print(f"zhuang tai: {zhuang_tai}")
            print(f"yu ju: {yu_ju}")
            if pd.isnull(self.predict_table.loc[zhuang_tai.top,yu_ju.top]):
                raise Exception("空状态，语句非法")
            else:
                print(f"now：({zhuang_tai.top},{yu_ju.top}) = {self.predict_table.loc[zhuang_tai.top,yu_ju.top]}")
                strs = self.predict_table.loc[zhuang_tai.top,yu_ju.top]
                if strs[0]=="S":
                    temp = int(strs.strip("Shift")) # type: ignore
                    fu_hao.push(yu_ju.top)
                    zhuang_tai.push(temp)
                    yu_ju.pop()
                elif strs[0]=="r":
                    temp = strs.strip("reduction ").split("->") # type: ignore
                    left = temp[0]
                    right = temp[1]
                    num = len(right)-1
                    for i in range(0,num):
                        fu_hao.pop()
                        zhuang_tai.pop()
                    fu_hao.push(left)
                    if left=='~':
                        print("分析完毕，语句合法！")
                        break 
                    elif pd.isnull(self.predict_table.loc[zhuang_tai.top,left]):
                        raise Exception("空状态，语句错误")
                    else:
                        strs = int(self.predict_table.loc[zhuang_tai.top,left].strip("GOTO")) # type: ignore
                        zhuang_tai.push(strs)
                    
                else:
                    raise Exception("不存在的分支出现，程序出现bug")
                    
        
        pass