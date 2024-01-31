# 靡不有初，鲜克有终
# 开发时间：2024/1/10 19:35
import pandas as pd

stArc_path = r'C:\Users\张晨皓\Desktop\张晨皓的汇报内容\56.时空网络与时空最短路问题（ST-SPP）建模及求解\代码\data\st_arc.txt'
stNode_path = r'C:\Users\张晨皓\Desktop\张晨皓的汇报内容\56.时空网络与时空最短路问题（ST-SPP）建模及求解\代码\data\st_node.txt'


class stNode:  # 定义时空节点类，实例为(i,t),(j,s)
    def __init__(self):
        self.stNode_id = None
        self.space = None
        self.time = None
        self.x_coord = None
        self.y_coord = None



class stArc:  # 定义时空弧类，实例为(i,j,t,s)
    def __init__(self):
        self.stArc_id = None
        # self.stArc_type = None  # 等待弧或者是运输弧
        self.from_space = None
        self.to_space = None
        self.from_time = None
        self.to_time = None
        self.cost = None

        self.from_stNode = None
        self.to_stNode = None


class ReadData:  # 读取路网数据
    def read_stNode(self):  # 针对stNode类的实例方法
        self.stNode_list = []
        df_stNode = pd.read_csv(stNode_path)

        self.nodeNum = len(pd.unique(df_stNode['space']))
        self.timeNum = len(pd.unique(df_stNode['time']))
        self.TTB = max(pd.unique(df_stNode['time']))
        self.O = 0
        self.D = 3
        self.Node = list(pd.unique(df_stNode['space']))
        self.T = list(pd.unique(df_stNode['time']))
        for i in range(0, len(df_stNode)):
            a = stNode()  # 实例化stNode，实例为(i,t)
            a.space = df_stNode.loc[i,'space']
            a.time = df_stNode.loc[i,'time']
            a.x_coord = df_stNode.loc[i,'x_coord']
            a.y_coord = df_stNode.loc[i,'y_coord']
            a.stNode_id = (a.space, a.time)
            self.stNode_list.append(a)

    def read_stArc(self):  # 针对stArc类的实例方法
        self.stArc_list = []
        df_stArc = pd.read_csv(stArc_path)
        for i in range(0, len(df_stArc)):
            b = stArc()  # 实例化stArc，实例为(i,j,t,s)
            b.from_space = df_stArc.loc[i,'from_space']
            b.to_space = df_stArc.loc[i,'to_space']
            b.from_time = df_stArc.loc[i,'from_time']
            b.to_time = df_stArc.loc[i,'to_time']
            b.cost = df_stArc.loc[i,'cost']
            b.stArc_id = (b.from_space, b.to_space, b.from_time, b.to_time)
            b.from_stNode = (b.from_space,b.from_time)
            b.to_stNode = (b.to_space,b.to_time)
            self.stArc_list.append(b)


network = ReadData()
network.read_stNode()
network.read_stArc()
if __name__ == "__main__":
    print(network.stNode_list[1].stNode_id)
    print(network.stArc_list[1].stArc_id)
    print("______________________________")
    for i in range(0, len(network.stArc_list)):
        print(network.stArc_list[i].stArc_id)

