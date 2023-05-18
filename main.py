from LL1 import LL1Method
bdsj = LL1Method()
with open("123.txt","r+") as f:
    n = f.readlines()
    for i in range(0,len(n)):
        n[i] = n[i].strip("\n")

bdsj.create_vt(n[0])
bdsj.create_vn(n[1])
bdsj.set_head(n[2])
for i in range(3,len(n)):
    bdsj.create_biaodashiji(n[i])
bdsj.look()    
bdsj.create_eplision_table()
bdsj.create_vt_first_table()
bdsj.create_right_first_table()
bdsj.merge()
bdsj.create_follow_table()
bdsj.create_select_table()
print(bdsj.LL1_judge())
bdsj.create_predict_tablle()
print(bdsj.predict("i+i*i"))