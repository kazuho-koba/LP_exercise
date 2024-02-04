## ChatGPTに考えてもらったもうちょっと複雑な線型計画法の例題
# 背景
# ある国には3つの軍事基地（A、B、C）があり、それぞれの基地は特定の数の防衛ミッションを成功させる必要があります。これらのミッションは、敵の侵攻を防ぐために不可欠です。各基地は、地上部隊、航空部隊、海軍部隊の3種類の軍事ユニットを配備することができます。各ユニットは特定のコストを持ち、特定の効果を発揮しますが、国全体で利用できる資源（予算、人員、装備）には限りがあります。

# 目的
# 全体のコストを最小限に抑えつつ、すべての軍事基地の防衛ミッションが成功するように、各基地に対する地上部隊、航空部隊、海軍部隊の配分を最適化する。

# 条件
# 各基地（A、B、C）には、成功させる必要がある特定の数のミッションがあります。
# 地上部隊、航空部隊、海軍部隊はそれぞれ、ミッション成功に対して異なる効果を持ちます。
# 各ユニット（地上、航空、海軍）は、特定のコスト（予算、人員、装備）を消費します。
# 国全体で利用できる予算、人員、装備には上限があります。
# 各基地ごとに、最低限配備しなければならない各種ユニットの数が定められています（最低限の防衛能力を保証するため）。
# 変数
# 各基地に配分する地上部隊、航空部隊、海軍部隊の数。
# 目的関数
# 全体のコストを最小化する。
# 制約条件
# 各基地のミッション成功に必要な効果を達成する。
# 利用可能な予算、人員、装備の上限を超えない。
# 各基地ごとに定められた最低限のユニット配分を守る。

## 上記を元に考えたシナリオ
# 3つの島（サイトA、B、C）を奪われたため奪還する任務を考える。
# それぞれのサイトは敵が守備隊（対陸上戦力防衛）、対空防御（対航空戦力防衛）、海岸線防御（対海上・揚陸戦力防衛）の能力を持っていて、これらを全て突破してサイトA~Cを奪還しなければならない。
# こちらは各サイト3種類の能力に対してそれぞれ陸上戦力、航空戦力、海上（揚陸）戦力を個別に割り当て、各サイトが保有する3つの防衛能力を突破すれば任務達成となる。
# こちらが出した戦力に対する相手の対応する防衛戦力の比が、その防衛戦力に対する対処所要時間であり、そのうち最も遅いものが24時間以内でなければならない。
# 全サイト、全部隊の攻略は
# その他、コスト制約があるのでそれをクリアしなければならない。
# 最低コストで防衛に成功する部隊の組み合わせを考える。

from pulp import *
import numpy as np

# 問題のインスタンスを作成（最小化問題）
prob = LpProblem("The_MilitaryAllocation_Problem", LpMinimize)

# 陸、空、海の各部隊1単位あたりのコスト設定（予算、人員、装備）
COST_LANDFORCE = np.array([50, 150, 100])           # 陸軍は人的コストが多い
COST_AIRFORCE = np.array([150, 100, 50])            # 空軍は予算コストが多い
COST_MARITIMEFORCE = np.array([100, 50, 150])       # 海軍は装備コストが多い

# 各サイトが持っている能力（守備隊、対空戦力、海岸線防御）、こちらが対応する能力で攻略し、その比が攻略所要時間となる。
# 例えば能力が[10,10,10]のサイトに陸、空、海の部隊を1,2,2単位ずつ割り当てたら、攻略所要時間は10,5,5時間となり、最も遅い10時間がそのサイトの攻略所要時間となる。
CITE_A = np.array([50, 100, 150])
CITE_B = np.array([100, 150, 50])
CITE_C = np.array([150, 50, 100])

# 各コストそれぞれの合計値の上限
COST_LIMIT_BUDGET = 10000   
COST_LIMIT_HUMAN = 10000    
COST_LIMIT_EQUIP = 5000     

# 各コスト合計値を計算するときの重み付け（人的損耗は避けたいからそういうときに対応するスケールを増やす）
SCALE_BUDGET = 1
SCALE_HUMAN = 1
SCALE_EQUIP = 1

# 変数定義（各基地A~Cへの配備数）
lf_a = LpVariable("lf_a", 0, None, 'Integer')   # サイトAへの割り当て部隊単位数（以下同じ）
af_a = LpVariable("af_a", 0, None, 'Integer')
mf_a = LpVariable("mf_a", 0, None, 'Integer')
lf_b = LpVariable("lf_b", 0, None, 'Integer')
af_b = LpVariable("af_b", 0, None, 'Integer')
mf_b = LpVariable("mf_b", 0, None, 'Integer')
lf_c = LpVariable("lf_c", 0, None, 'Integer')
af_c = LpVariable("af_c", 0, None, 'Integer')
mf_c = LpVariable("mf_c", 0, None, 'Integer')


# 目的関数（総コスト
prob += ((lf_a+lf_b+lf_c) * COST_LANDFORCE[0] + (af_a+af_b+af_c) * COST_AIRFORCE[0] + (mf_a+mf_b+mf_c) * COST_MARITIMEFORCE[0]) * SCALE_BUDGET\
        + ((lf_a+lf_b+lf_c) * COST_LANDFORCE[1] + (af_a+af_b+af_c) * COST_AIRFORCE[1] + (mf_a+mf_b+mf_c) * COST_MARITIMEFORCE[1]) * SCALE_HUMAN\
        + ((lf_a+lf_b+lf_c) * COST_LANDFORCE[2] + (af_a+af_b+af_c) * COST_AIRFORCE[2] + (mf_a+mf_b+mf_c) * COST_MARITIMEFORCE[2]) * SCALE_EQUIP,\
        "Total Defense Cost"

# 制約条件
# 各コストのそれぞれの合計に対する制約（金、人、物の各コストがそれぞれの上限を超えてはならない）
prob += (lf_a+lf_b+lf_c) * COST_LANDFORCE[0] + (af_a+af_b+af_c) * COST_AIRFORCE[0] + (mf_a+mf_b+mf_c) * COST_MARITIMEFORCE[0] <= COST_LIMIT_BUDGET, "Cost Limit for Budget"
prob += (lf_a+lf_b+lf_c) * COST_LANDFORCE[1] + (af_a+af_b+af_c) * COST_AIRFORCE[1] + (mf_a+mf_b+mf_c) * COST_MARITIMEFORCE[1] <= COST_LIMIT_HUMAN, "Cost Limit for Human Resources"
prob += (lf_a+lf_b+lf_c) * COST_LANDFORCE[2] + (af_a+af_b+af_c) * COST_AIRFORCE[2] + (mf_a+mf_b+mf_c) * COST_MARITIMEFORCE[2] <= COST_LIMIT_EQUIP, "Cost Limit for Equipment Allocation"

# ミッションに関する制約（攻略所要時間のうち最も遅いものが24時間を超えてはならない）
prob += max(CITE_A[0]/lf_a, CITE_A[1]/af_a, CITE_A[2]/mf_a) <= 24, "Time Limit to Re-Capture Cite A"
prob += max(CITE_B[0]/lf_b, CITE_B[1]/af_b, CITE_B[2]/mf_b) <= 24, "Time Limit to Re-Capture Cite B"
prob += max(CITE_C[0]/lf_c, CITE_C[1]/af_c, CITE_C[2]/mf_c) <= 24, "Time Limit to Re-Capture Cite C"

# 問題を解く
prob.solve()

# 結果の出力
solution = {
    "Status": LpStatus[prob.status],
    "lf_a": lf_a.varValue,
    "af_a": af_a.varValue,
    "mf_a": mf_a.varValue,
    "lf_b": lf_b.varValue,
    "af_b": af_b.varValue,
    "mf_b": mf_b.varValue,
    "lf_c": lf_c.varValue,
    "af_c": af_c.varValue,
    "mf_c": mf_c.varValue,
    "Total Defense Cost": value(prob.objective)
}
print(solution)