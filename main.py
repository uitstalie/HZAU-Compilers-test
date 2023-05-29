from libs.expression_list import ExpressionList
from libs.analysis.OPG import FormalOPGMethod
exp_list = ExpressionList.ExpressionList()
exp_list.init("HZAU-Compilers-test\\123.txt","1")

OPG = FormalOPGMethod.FormalOPGMethod(exp_list,"i")
print(OPG)
OPG.create_first_vt_table()
OPG.create_last_vt_table()
OPG.create_OPG_table()
OPG.predict("1.23+3.45*2+(4^3)*(3^5)")