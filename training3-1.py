'''
         製品A       製品B
販売価格   1500      2000
変動製造原価 600      1200
貢献利益     900      800
生産時間     0.2      0.4
材料消費      2.5     2
需要上限    20000    20000

固定加工費：11,900,000円
年間総生産時間：9000時間
年間総材料：60000kg

1つの機械、1つの材料を使って製品A、Bを製造し利益の最大化を図る‥
これらを元に会社の営業利益を最大化する年間生産量と営業利益を求める。
'''

from pulp import *

# 定数
FIXED_COST = 11900000               # 固定加工費
TOTAL_PRODUCTION_TIME = 9000        # 年間総生産時間
TOTAL_AVAILABLE_MATERIAL = 60000    # 年間総材料

# 問題のインスタンスを作成（最大化問題）
prob = LpProblem("The_ProductionPlan_Problem", LpMaximize)

# 変数定義（生産量
amount_A = LpVariable("amount_A", 0, None, 'Integer')
amount_B = LpVariable("amount_B", 0, None, 'Integer')

# 目的関数
prob += 900*amount_A + 800*amount_B - FIXED_COST, "Total Profit"

# 制約条件
prob += 2.5*amount_A + 2*amount_B <= 60000, "Material Consumption"  # 材料消費量
prob += 0.2*amount_A + 0.4*amount_B <= 9000, "Operation Hours"      # 総生産時間
prob += amount_A <= 20000, "Maximum Demand for A"                   # 需要上限
prob += amount_B <= 20000, "Maximum Demand for B"                   # 需要上限

# 問題を解く
prob.solve()

# 結果の出力
solution = {
    "Status": LpStatus[prob.status],
    "amount_A": amount_A.varValue,
    "amount_B": amount_B.varValue,
    "Total Profit": value(prob.objective)
}
print(solution)