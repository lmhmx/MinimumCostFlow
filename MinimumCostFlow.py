import enum
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 计算简化成本，直接放到edge里面
class EdgeIndex:
    start=0
    end=1
    cost=2
    capacity=3
    x=4
    delta=5
# 搜索树的节点
class node:
    def __init__(self,parent=None,child=[],data=None):
        self.parent = parent
        self.child = child
        self.data = data
# 根据 z 确定
def calCost(point:list,z:list,edge:list):
    for item in edge:
        i=item[EdgeIndex.start]
        j=item[EdgeIndex.end]
        item[EdgeIndex.delta]=z[point.index(i)]-z[point.index(j)]+item[EdgeIndex.cost]

def findS(S_init,edge):
    S=[S_init]
    # 新增加的点
    S_tmp=[]
    
    # 找到以S_init为起始点的其他的所有的S集合中的点
    # 首先是找到S_init直接连接的有效的点
    for item in edge:
        if(item[EdgeIndex.start]==S_init and 
            item[EdgeIndex.x]<item[EdgeIndex.capacity] and
            item[EdgeIndex.delta]==0):
            S_tmp.append(item[EdgeIndex.end])
    # 采用递归找到其余的点
    for item in S_tmp:
        tmp=findS(item,edge)
        for i in tmp:
            if(i not in S):
                S.append(i)
    return S

def updatePath(edge,endNode:node,target_Value,target):
    currentX=0
    for item in edge:
        if(item[EdgeIndex.end]==target):
            currentX=currentX+item[EdgeIndex.x]
    # 寻找可更新的最大流
    currentNode=endNode
    increace=np.inf

    while(1):
        if(currentNode.parent!=None):
            start=currentNode.data
            end=currentNode.parent.data
            for item in edge:
                if(item[EdgeIndex.start]==start and item[EdgeIndex.end]==end):
                    increace=np.min((increace,item[EdgeIndex.capacity]-item[EdgeIndex.x],target_Value-currentX))
                    break
            currentNode=currentNode.parent
        else:
            break

    # 更新流上的流量
    currentNode=endNode
    while(1):
        if(currentNode.parent!=None):
            start=currentNode.data
            end=currentNode.parent.data
            for item in edge:
                if(item[EdgeIndex.start]==start and item[EdgeIndex.end]==end):
                    item[EdgeIndex.x]=item[EdgeIndex.x]+increace
                    break
            currentNode=currentNode.parent
        else:
            break
    if(currentX+increace==target_Value):
        return 1
    else:
        return 2
    # end

def updateX(edge,target,s,target_Value):
    """
    target_Value 是最大流
    如果成功达到最大值，返回1
    如果成功进行了更新，返回2
    如果还没有达到最大值，返回-1
    """
    ans=-1
    node_list=[]
    root = node(parent=None,child=[],data=target)
    node_list.append(root)
    while(1):
        if(len(node_list)>0):
            currentNode = node_list[-1]
            node_list.pop()
            for item in edge:
                if(item[EdgeIndex.end] == currentNode.data and 
                        item[EdgeIndex.capacity]>item[EdgeIndex.x] and 
                        item[EdgeIndex.delta] == 0):
                    newNode = node(parent=currentNode,data=item[EdgeIndex.start])
                    currentNode.child.append(newNode)
                    node_list.append(newNode)
                    if(newNode.data==s):
                        tmp_result=updatePath(edge,newNode,target_Value,target)
                        if(tmp_result==1):
                            return 1
                        else:
                            ans=2
        else:
            break
    return ans
def calNearestPoint(pos1,pos2,r):
    x1,y1=pos1[0],pos1[1]
    x2,y2=pos2[0],pos2[1]

    vx = x2-x1
    vy = y2-y1

    vr = np.sqrt(vx*vx+vy*vy)

    p1_x = x1+vx/vr*r
    p1_y = y1+vy/vr*r

    p2_x = x2-vx/vr*r
    p2_y = y2-vy/vr*r

    return (p1_x,p1_y),(p2_x,p2_y)

def plt_map(edge,z,point:list,S,E,Available):
    v_pos=[
        (0,1),(1,2),(1,1),(1,0),(2,1),(3,2),(3,1),(3,0),(4,1)
    ]
    r=0.2
    ax=plt.gca()
    # 画点
    for i,item in enumerate(v_pos):
        color='black'
        if(point[i] in S):
            color='red'
        # color='black'
        ax.add_patch(patches.Circle(item,r,edgecolor=color,fill=False))
        plt.text(item[0]-0.15,item[1],"{:2d}[{:2d}]".format(point[i],z[i]))
    # 画箭头
    for i,item in enumerate(edge):
        color='black'
        if(item in E):
            color='green'
        if(item in Available):
            color='red'
        # color='black'
        p1,p2=calNearestPoint(v_pos[point.index(item[EdgeIndex.start])],v_pos[point.index(item[EdgeIndex.end])],r)
        plt.arrow(p1[0],p1[1],p2[0]-p1[0],p2[1]-p1[1],length_includes_head=True,head_width=0.02,head_length=0.03,facecolor=color,edgecolor=color)
        plt.text((p1[0]+p2[0])/2,(p1[1]+p2[1])/2+0.05,"({:2.1f},{:2.1f})".format(item[EdgeIndex.cost],item[EdgeIndex.capacity]))
        plt.text((p1[0]+p2[0])/2,(p1[1]+p2[1])/2-0.1+0.05,"{{{:2.1f},{:2.1f}}}".format(item[EdgeIndex.x],item[EdgeIndex.delta]))

# 9 个点
point=[1,2,3,4,5,6,7,8,9]
# 每个点的邻接矩阵
# 元组的第1个表示起始点
# 第2个表示结束点
# 第3个表示费用
# 第4个表示容量
# 第5个表示当前流量
# 第6个表示简化成本


edge=[
        [1,2,3,4,0,0],[1,3,4,2,0,0],[1,4,4,6,0,0],
        [2,5,2,2,0,0],[2,6,4,3,0,0],
        [3,2,1,2,0,0],[3,5,2,1,0,0],
        [4,3,2,1,0,0],[4,5,2,3,0,0],[4,8,2,2,0,0],
        [5,6,1,1,0,0],[5,7,2,4,0,0],[5,8,9,3,0,0],
        [6,7,3,2,0,0],[6,9,2,5,0,0],
        [7,8,1,2,0,0],[7,9,3,7,0,0],
        [8,9,3,4,0,0]
        ]

# S集合
S=[point[0]]

# 补集
S_bar = []

# 各个点的对偶变量
z=[0,0,0,0,0,0,0,0,0]
print("helo")
target_Value=11
while(1):

    # S集合
    S=[point[0]]
    calCost(point,z,edge)
    # 根据edge 找到S集合
    S=findS(S[0],edge)
    # 补集
    S_bar = []
    # 各个点的对偶变量
    for i in point:
        if(i not in S):
            S_bar.append(i)

    # 增广边的集合
    E = []
    for item in edge:
        # 如果是前向边
        if(item[EdgeIndex.start] in S and item[EdgeIndex.end] in S_bar):
            if(item[EdgeIndex.capacity]>item[EdgeIndex.x]):
                # 如果可以增加
                E.append(item)
            else:
                pass
        # 如果是后向边
        elif(item[EdgeIndex.end] in S_bar and item[EdgeIndex.start] in S):
            if(item[EdgeIndex.x]>0):
                E.append(item)
            else:
                pass
        else:
            pass
    # 可用边的集合
    if(len(E)==0):
        calCost(point,z,edge)
        tmp_result=updateX(edge,point[-1],point[0],target_Value)
        if(tmp_result==2):
            pass
        elif(tmp_result==1):
            print("success")
            break
        else:
            print("fail")
            print(edge)
            break
    else:
        Available = []
        for item in edge:
            if(item[EdgeIndex.start] in S and 
                    item[EdgeIndex.delta] == 0 and
                    item[EdgeIndex.capacity] > item[EdgeIndex.x]):
                Available.append(item)
            else:
                pass
        plt.figure(figsize=(12,8))
        plt_map(edge,z,point,S,E,Available)
        plt.show()

        # 更新参数
        eta = np.Inf
        v_list=[]
        for item in E:
            if(item[EdgeIndex.delta]<eta):
                v_list=[]
                v_list.append(item[EdgeIndex.end])
                eta=item[EdgeIndex.delta]
            elif(item[EdgeIndex.delta]==eta):
                v_list.append(item[EdgeIndex.end])
                eta=item[EdgeIndex.delta]
        # 更新z
        for item in S_bar:
            z[point.index(item)]=eta+z[point.index(item)]
    calCost(point,z,edge)

    Available = []
    for item in edge:
        if(item[EdgeIndex.start] in S and 
                item[EdgeIndex.delta] == 0 and
                item[EdgeIndex.capacity] > item[EdgeIndex.x]):
            Available.append(item)
        else:
            pass
    plt.figure(figsize=(12,8))
    plt_map(edge,z,point,S,E,Available)
    plt.show()

    tmp_result=updateX(edge,point[-1],point[0],target_Value)

    # plt.figure(figsize=(12,8))
    # plt_map(edge,z,point,S,E,Available)
    # plt.show()

    if(tmp_result==1):
        print("success01")
        print(edge)
        plt.figure(figsize=(12,8))
        plt_map(edge,z,point,S,E,Available)
        plt.show()
        break
    elif(tmp_result==2):
        print("update flow")
        print(edge)
        plt.figure(figsize=(12,8))
        plt_map(edge,z,point,S,E,Available)
        plt.show()

