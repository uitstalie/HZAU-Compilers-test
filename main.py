from libs.analysis.LR.LRNode import LR_method
from libs.expression_list import ExpandExpressionList
from libs.analysis.OPG import FormalOPGMethod
exp_list = ExpandExpressionList.ExpandExpressionList()
exp_list.init("HZAU-Compilers-test\\123.txt","1")
exp_list.expand()


LR = LR_method(exp_list)

LR.sethead()
LR.make_node()
LR.make_predict_table()
LR.predict("abab")