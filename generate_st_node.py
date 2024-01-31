# 靡不有初，鲜克有终
# 开发时间：2024/1/10 16:56
path = r'C:\Users\张晨皓\Desktop\张晨皓的汇报内容\56.时空网络与时空最短路问题（ST-SPP）建模及求解\代码\data\st_node.txt'

node_id = [0,1,2,3,4,5]
x_coord = [0,0,4,4,1,3]
y_coord = [2,0,2,0,1,1]

time_stamp = [0,1,2,3,4,5,6,7,8,9,10,11]  # [0,1,2,3,4,5,6,7,8,9,10,11]

file = open(path, 'w').close()
file_generate = open(path, mode='a')
file_generate.write(str('space') + "," +str('time') + ","+str('x_coord') + ","+str('y_coord') )  # 表头
file_generate.write('\n')
for i in range(0,len(time_stamp)):
    t_stamp = time_stamp[i]
    for j in range(0,len(node_id)):
        n_id = node_id[j]
        x = x_coord[j]
        y = y_coord[j]
        file_generate.write(str(n_id) + "," +str(t_stamp) + ","+str(x) + ","+str(y) )
        file_generate.write('\n')  # 写入计算结果
file_generate.close()