from libs.expression_list.ExpressionList import ExpressionList


class ExpandExpressionList(ExpressionList):
    
    def expand(self):
        expand_start = "~"
        self.vn.append(expand_start)
        self.expression_list.setdefault(expand_start,[]).append(self.head)