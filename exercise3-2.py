from pulp import *

# 問題のインスタンスを作成（最小化問題）
prob = LpProblem("The_Transportation_Problem", LpMinimize)

# 変数定義（輸送量, 非負整数
x_AC = LpVariable("x_AC", 0, None, 'Integer')
x_AD = LpVariable("x_AD", 0, None, 'Integer')
x_AE = LpVariable("x_AE", 0, None, 'Integer')
x_BC = LpVariable("x_BC", 0, None, 'Integer')
x_BD = LpVariable("x_BD", 0, None, 'Integer')
x_BE = LpVariable("x_BE", 0, None, 'Integer')

# 目的関数
prob += 1*x_AC + 2*x_AD + 5*x_AE + 4*x_BC + 3*x_BD + 8*x_BE, "Total Transportation Cost"

# 制約条件（工場の生産能力）
prob += x_AC + x_AD + x_AE == 15, "Capacity of Factory A"
prob += x_BC + x_BD + x_BE == 10, "Capacity of Factory B"

# 制約条件（小売店の需要を満たす
prob += x_AC + x_BC == 10, "Demand at Shop C"
prob += x_AD + x_BD == 8, "Demand at Shop D"
prob += x_AE + x_BE == 7, "Demand at Shop E"

# 問題を解く
prob.solve()

# 結果の出力
solution = {
    "Status": LpStatus[prob.status],
    "x_AC": x_AC.varValue,
    "x_AD": x_AD.varValue,
    "x_AE": x_AE.varValue,
    "x_BC": x_BC.varValue,
    "x_BD": x_BD.varValue,
    "x_BE": x_BE.varValue,
    "Total Transportation Cost": value(prob.objective)
}
print(solution)