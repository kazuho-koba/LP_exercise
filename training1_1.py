# 製品: ハンバーグ、ミートボール、ソーセージ
# 原材料: 牛肉、豚肉、鶏肉（1日あたりの供給量がそれぞれ100kg、240kg、150kg）
# 製品ごとの原材料使用量と利益:
# ハンバーグ: 牛肉2kg、豚肉3kg、鶏肉0kg、利益2万円
# ミートボール: 牛肉1kg、豚肉6kg、鶏肉0kg、利益3万円
# ソーセージ: 牛肉0kg、豚肉4kg、鶏肉5kg、利益4万円
# 制約条件:
# 各原材料の日々の供給量を超えない
# 特定の製品（例えばソーセージ）の最大生産ロット数の制限（例: 20ロット）

from pulp import *

# 問題の定義（最大化問題
prob = LpProblem("Advanced_Product_Mix_Problem", LpMaximize)

# 変数の定義
x1 = LpVariable("Hamburgers", 0, None, 'Integer')    # ハンバーグの生産ロット数（非負整数
x2 = LpVariable("Meatballs", 0, None, 'Integer')     # ミートボールの生産ロット数（非負整数
x3 = LpVariable("Sausages", 0, 20, 'Integer')        # ソーセージの生産ロット数（非負整数、最大20ロットまで

# 目的関数
prob += 2*x1 + 3*x2 + 4*x3, "Total Profit"

# 制約条件
prob += 2*x1 + 1*x2 <= 100, "Beef Constraint"
prob += 3*x1 + 6*x2 + 4*x3 <= 240, "Pork Constraint"
prob += 5*x3 <= 150, "Chicken Constraint"

# 問題を解く
prob.solve()

# 結果の出力
print("最適解:")
print("ハンバーグの生産ロット数 = ", x1.varValue)
print("ミートボールの生産ロット数 = ", x2.varValue)
print("ソーセージの生産ロット数 = ", x3.varValue)

print("最大利益（万円） = ", value(prob.objective))
