from libs.expression_list.ExpressionList import ExpressionList


class PreProcessingMethod:
    def __init__(self,expressionlist:ExpressionList):
        self.__expression_list = expressionlist
        pass
    
    @property
    def get_expression(self):
        return self.__expression_list
    
    
    def isvt(self, i: str):
        if len(i) != 1:
            raise Exception("错误参数")
        elif (i in self.__expression_list.vt):
            return True
        else:
            return False

    def isvn(self, i: str):
        if len(i) != 1:
            raise Exception("错误参数")
        elif (i in self.__expression_list.vn):
            return True
        else:
            return False
        