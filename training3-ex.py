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

from pulp import *

# 問題のインスタンスを作成（最小化問題）
prob = LpProblem("The_MilitaryAllocation_Problem", LpMinimize)

# 各軍のコスト設定（予算_億円、人員_10人、装備_ユニット）
COST_ARMY = [50, 150, 100]      # 陸軍は人的コストが多い
COST_AIRFORCE = [150, 100, 50]  # 空軍は予算コストが多い
COST_NAVY = [100, 50, 150]      # 海軍は装備コストが多い

# 全コスト上限
COST_LIMIT_BUDGET = 10000   # 1兆円
COST_LIMIT_HUMAN = 10000    # 10万人
COST_LIMIT_EQUIP = 5000     # 5000ユニット

# 各コストの重み付け
SCALE_BUDGET = 1
SCALE_HUMAN = 1
SCALE_EQUIP = 1

# 変数定義（各基地A~Cへの配備数）
army_a = LpVariable("army_a", 0, None, 'Integer')
airforce_a = LpVariable("airforce_a", 0, None, 'Integer')
navy_a = LpVariable("navy_a", 0, None, 'Integer')
army_b = LpVariable("army_b", 0, None, 'Integer')
airforce_b = LpVariable("airforce_b", 0, None, 'Integer')
navy_b = LpVariable("navy_b", 0, None, 'Integer')
army_c = LpVariable("army_c", 0, None, 'Integer')
airforce_c = LpVariable("airforce_c", 0, None, 'Integer')
navy_c = LpVariable("navy_c", 0, None, 'Integer')

# コストの計算
totalcost_army = (army_a + army_b + army_c) * COST_ARMY
totalcost_airforce = (airforce_a + airforce_b + airforce_c) * COST_AIRFORCE
totalcost_navy = (navy_a + navy_b + navy_c) * COST_NAVY

# 目的関数（総コスト
prob += (totalcost_army[0] + totalcost_airforce[0] + totalcost_navy[0]) * SCALE_BUDGET, "Total Defense Cost"