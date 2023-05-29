class Stack():
    
    def __init__(self):
        self.__data = []
        self.__tops = -1
    
    def __repr__(self):
        return str(self.__data)
    
    @property
    def data(self):
        return self.__data
    
    @property
    def length(self):
        return self.__tops+1
    
    def push(self,data):
        self.__data.append(data)
        self.__tops += 1
    
    
    def pop(self,num = 1):
        for i in range(0,num):
            self.__data.pop(self.__tops)
            self.__tops-=1
    
    @property
    def empty(self):
        if self.__tops == -1:
            return True
        else:
            return False
    
    @property
    def top(self):
        return self.__data[self.__tops]
    

    @property
    def top_second(self):
        if len(self.__data)>1:
            return self.__data[self.__tops-1]
        else:
            raise Exception("栈里面就一个哪来的第二个")