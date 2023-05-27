from method import ExpressionList,LL1Method
exp_list = ExpressionList()
exp_list.init("LL1/123.txt","1")
bdsj = LL1Method(exp_list)

bdsj.look()    
bdsj.create_epsilon_table()
bdsj.create_vt_first_table()
bdsj.create_right_first_table()
bdsj.merge()
bdsj.create_follow_table()
bdsj.create_select_table()
ans = bdsj.LL1_judge()
print(ans)
if ans[0]== True:
    bdsj.create_predict_tablle()
    print(bdsj.predict("LL1/input.txt"))