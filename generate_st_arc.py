# 靡不有初，鲜克有终
# 开发时间：2024/1/10 16:57
import numpy as np

path = r'C:\Users\张晨皓\Desktop\张晨皓的汇报内容\56.时空网络与时空最短路问题（ST-SPP）建模及求解\代码\data\st_arc.txt'

node_id_lst = [0,1,2,3,4,5]
from_node_lst = [0,0,0,1,1,1,2,2,3,3,4,5,5]
to_node_lst = [1,2,4,0,4,3,0,3,1,2,5,2,3]

time_stamp = [0,1,2,3,4,5,6,7,8,9,10,11]  #  [0,1,2,3,4,5,6,7,8,9,10,11]
# 成本矩阵，行数量为连接路段link数量，每一行为对应路段在不同时间下的旅行时间。
# 列数量为时间戳数量，每一列代表在当前时间戳下，不同路段的旅行时间
costMtx = []
mean = [2,3,1,2,1,3,3,2,3,2,1,1,1]
stddev = 1  # 标准差
num_samples = len(time_stamp) # 样本量
for i in range(0,len(mean)):
    positive_integers = list(np.round(np.abs(np.random.normal(loc=mean[i], scale=stddev, size=(num_samples)))).astype('int'))
    costMtx.append(positive_integers)
print(costMtx)


file = open(path, 'w').close()
file_generate = open(path, mode='a')
file_generate.write(str('from_space') + ","+str('to_space')+ "," +str('from_time')+ "," +str('to_time') +","+str('cost'))  # 表头
file_generate.write('\n')
# 构建运输弧
for i in range(0,len(from_node_lst)):  # 对于任意的路段
    from_node = from_node_lst[i]
    to_node = to_node_lst[i]
    for j in range(0,len(time_stamp)):  # 对于任意的时间段
        cost = costMtx[i][j] + 1
        from_time = time_stamp[j]
        to_time = time_stamp[j] + cost
        if to_time <= max(time_stamp):
            file_generate.write(str(from_node) + "," + str(to_node) + "," + str(from_time) + "," + str(to_time) + "," + str(cost))
            file_generate.write('\n')  # 写入计算结果
        else:
            pass

# 构建等待弧
for i in range(0,len(node_id_lst)):  # 对于任意的结点
    from_node = node_id_lst[i]
    to_node = node_id_lst[i]
    for j in range(0,len(time_stamp)-1):  # 对于任意的时间段
        cost = 1
        from_time = time_stamp[j]
        to_time = time_stamp[j] + cost
        file_generate.write(str(from_node) + "," + str(to_node) + "," + str(from_time) + "," + str(to_time) + "," + str(cost))
        file_generate.write('\n')  # 写入计算结果
file_generate.close()



