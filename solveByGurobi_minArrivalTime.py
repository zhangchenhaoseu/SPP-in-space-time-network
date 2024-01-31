# 靡不有初，鲜克有终
# 开发时间：2024/1/10 21:28
from gurobipy import *
import construct_st_network as construct
import time

"""——————————————最早到达问题，终点的等待弧段费用设置为0,其他为s-t——————————————"""
'''建模和求解。使用Gurobi对问题进行建模'''
def modelingAndSolve(network):
    # 建立模型
    m = Model('SpaceTimeSPP')

    # 模型设置：由于存在函数printSolution，因此关闭输出;以及容许误差
    m.setParam('MIPGap', 0.01)
    # m.setParam('OutputFlag', 0)

    # 定义变量：
    # Step1.添加决策变量/辅助变量
    '______添加决策变量X______'
    # 建立存储决策变量X的数据结构
    X = [[[[[] for _ in range(0, network.timeNum)] for _ in range(0, network.timeNum)] for _ in range(0, network.nodeNum)] for _ in range(0, network.nodeNum)]  # x_ijts
    # 根据数据结构向模型中添加对应下标的变量
    for _ in network.stArc_list:
        i = _.stArc_id[0]
        j = _.stArc_id[1]
        t = _.stArc_id[2]
        s = _.stArc_id[3]
        X[i][j][t][s] = m.addVar(vtype=GRB.BINARY, name=f"X_{i}_{j}_{t}_{s}")
    m.update()
    var_lst = m.getVars()
    print(var_lst,"变量总数是",len(var_lst))
    # 定义目标函数
    obj = LinExpr(0)  # 线性项，初始值为0，可用.addTerms(a,x) 意为将变量x增加到表达式，系数为a
    for _ in network.stArc_list:
        i = _.stArc_id[0]
        j = _.stArc_id[1]
        t = _.stArc_id[2]
        s = _.stArc_id[3]
        if i == j and (i == network.D):
            cost = 0
        else:
            cost = s - t
        obj.addTerms(cost, X[i][j][t][s])
    m.setObjective(obj, sense=GRB.MINIMIZE)

    # 定义约束条件:
    # 1.起点流出约束
    num = 0
    expr = LinExpr(0)  # 线性项，初始值为0，可用.addTerms(a,x) 意为将变量x增加到表达式，系数为a
    for _ in network.stArc_list:
        i = _.stArc_id[0]
        j = _.stArc_id[1]
        t = _.stArc_id[2]
        s = _.stArc_id[3]
        if i == network.O and t == 0:
            expr.addTerms(1, X[i][j][t][s])
    for _ in network.stArc_list:
        j = _.stArc_id[0]
        i = _.stArc_id[1]
        s = _.stArc_id[2]
        t = _.stArc_id[3]
        if i == network.O and t == 0:
            expr.addTerms(-1, X[j][i][s][t])
    num += 1
    m.addConstr(expr == 1, f'C1_{num}')
    # 2.终点流入约束
    num = 0
    expr = LinExpr(0)  # 线性项，初始值为0，可用.addTerms(a,x) 意为将变量x增加到表达式，系数为a
    for _ in network.stArc_list:
        i = _.stArc_id[0]
        j = _.stArc_id[1]
        t = _.stArc_id[2]
        s = _.stArc_id[3]
        if i == network.D and t == network.TTB:
            expr.addTerms(1, X[i][j][t][s])
    for _ in network.stArc_list:
        j = _.stArc_id[0]
        i = _.stArc_id[1]
        s = _.stArc_id[2]
        t = _.stArc_id[3]
        if i == network.D and t == network.TTB:
            expr.addTerms(-1, X[j][i][s][t])
    num += 1
    m.addConstr(expr == - 1, f'C2_{num}')

    # 3.中间节点流平衡约束
    num = 0
    for i in network.Node:
        for t in network.T:
            if (i == network.O and t==0) or (i == network.D and t == network.TTB):
                pass
            else:
                expr = LinExpr(0)  # 线性项，初始值为0，可用.addTerms(a,x) 意为将变量x增加到表达式，系数为a
                for _ in network.stArc_list:
                    if _.stArc_id[0] == i and _.stArc_id[2] == t:
                        j = _.stArc_id[1]
                        s = _.stArc_id[3]
                        expr.addTerms(1, X[i][j][t][s])
                for _ in network.stArc_list:
                    if _.stArc_id[1] == i and _.stArc_id[3] == t:
                        j = _.stArc_id[0]
                        s = _.stArc_id[2]
                        expr.addTerms(-1, X[j][i][s][t])
                num += 1
                m.addConstr(expr == 0, f'C3_{num}')

    # 记录求解开始时间
    start_time = time.time()
    # 求解
    m.optimize()
    m.write('SpaceTimeSPP.lp')
    if m.status == GRB.OPTIMAL:
        print("-" * 20, "求解成功", '-' * 20)
        # 输出求解总用时
        print(f"求解时间: {time.time() - start_time} s")
        print(f"目标函数为: {m.ObjVal}")
    else:
        print("无解")
    # 展示求解结果
    getSolution(st_network,m)
    return m


'''定义解类。建立求解结果的数据结构框架，并建立将Gurobi求解结果存放在数据结构中的连接'''
class Solution:
    ObjVal = 0  # 目标函数值
    X = None  # 用于存放决策变量X_ijts的值

    def __init__(self, network, model):  # 建立类属性，解类的建立需要输入数据和模型
        self.ObjVal = model.ObjVal
        self.X = [[[[0 for _ in range(0, network.timeNum)] for _ in range(0, network.timeNum)] for _ in range(0, network.nodeNum)] for _ in range(0, network.nodeNum)]  # 由于仅作存储作用方便调用，因此此处全连接即可


def getSolution(data, model):  # 定义函数，从Gurobi输出的模型中获得目标函数值、决策变量X和Y、继而分别得到卡车和无人机路由的节点序列
    solution = Solution(data, model)
    # 在三维矩阵结构中存储自变量的取值，拆字段，检验是否是x，然后保存
    var_lst = model.getVars()
    print('var_lst:')
    for i in var_lst:
        if i.x !=0:
            print(i)
    for v in model.getVars():
        split_arr = re.split(r"_", v.VarName)  # 将gurobi形式的变量进行拆解，便于利用数据结构实现实现存储
        if split_arr[0] == 'X' and round(v.x) != 0:
            solution.X[int(split_arr[1])][int(split_arr[2])][int(split_arr[3])][int(split_arr[4])] = v.x  # X_ij
        else:
            pass
    # print("路由变量 solution.X:", solution.X)

    return solution


if __name__ == "__main__":
    st_network = construct.network
    modelingAndSolve(st_network)


