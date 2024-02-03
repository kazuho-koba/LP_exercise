from pulp import *

# 問題の定義（最大化問題）
prob = LpProblem("The_Product_Mix_Problem", LpMaximize)

# 変数の定義
x = LpVariable("Hamburgers", 0)  # ハンバーグの生産ロット数（第2引数は値の下限
y = LpVariable("Meatballs", 0)   # ミートボールの生産ロット数

# 目的関数
prob += 2*x + 3*y, "Total Profit"

# 制約条件
prob += 2*x + y <= 100, "Beef Constraint"
prob += 3*x + 6*y <= 240, "Pork Constraint"

# 問題を解く
prob.solve()

# 結果の出力
solution = {
    "Status": LpStatus[prob.status],
    "Hamburgers": x.varValue,
    "Meatballs": y.varValue,
    "Total Profit": value(prob.objective)
}

# print("最適解:")
# print("ハンバーグの生産ロット数 = ", x.varValue)
# print("ミートボールの生産ロット数 = ", y.varValue)

# print("最大利益（万円） = ", value(prob.objective))

print(solution)