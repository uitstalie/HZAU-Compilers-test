class Stack():
    
    def __init__(self):
        self.data = []
        self.tops = -1
    
    def __repr__(self):
        return str(self.data)
    
    
    def push(self,data):
        self.data.append(data)
        self.tops += 1
    
    
    def pop(self):
        self.data.pop(self.tops)
        self.tops-=1
    
    @property
    def empty(self):
        if self.tops == -1:
            return True
        else:
            return False
    
    @property
    def top(self):
        return self.data[self.tops]
        