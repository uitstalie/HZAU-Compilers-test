from typing import Dict, List, Tuple
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
    