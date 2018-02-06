


import time
import random
import math



people = [('Seymour','BOS'),
          ('Franny','DAL'),
          ('Zooey','CAK'),
          ('Walt','MIA'),
          ('Buddy','ORD'),
          ('Les','OMA')]

destination = 'LGA'
flights = {}
for line in open('schedule.txt'):
    origin,dest,depart,arrive,price=line.strip().split(',')
    #orgin起点，dest终点
    flights.setdefault((origin,dest),[])
    #将航班详情添加到航班列表中
    flights[(origin,dest)].append((depart,arrive,int(price)))

#将时间转化为分钟数
def getminutes(t):
    x = time.strftime(t,'%H:%M')
    return x[3]*60+x[4]


def printschedule(r):
    for d in range(len(r)/2):
        name = people[d][0]
        origin = people[d][1]
        #选初始点到目的地
        out = flights[(origin,destination)][r[2*d]]
        #选从目的地回初始点9o
        ret = flights[(destination,origin)][r[2*d+1]]
        print('%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,out[0],out[1],out[2],ret[0],ret[1],ret[3]))

#将所有方面都考虑成一个值价格进行计算
def schedulecost(sol):
    totalprice = 0
    latestarrival = 0
    earliestdep = 24 * 60
    for d in range(len(sol)/2):
        origin = people[d][1]
        #得到往返程航班价格
        outbound = flights[(origin,destination)][int(sol[2*d])]
        returnf = flights[(destination,origin)][int(sol[2*d+1])]

        #totalprice是总价格往返航班
        totalprice+=outbound+returnf

        #记录最晚到达时间和最早离开时间
        #最晚到达时间，outbound[1]记录飞机到达时间
        if latestarrival<getminutes(outbound[1]):
            latestarrival = getminutes(outbound[1])
        #最早离开时间，returnf[0]记录最早离开的飞机时间
        if earliestdep>getminutes(returnf[0]):
            earliestdep = getminutes(returnf[0])
    #等待全部人到达
    totalwait = 0
    for d in range(len(sol) / 2):
        origin = people[d][1]
        outbound = flights[(origin,destination)][int(sol[2*d])]
        returnf = flights[(destination,origin)][int(sol[2*d+1])]
        #要等待一家人到期的时间
        totalwait+=latestarrival-getminutes(outbound[1])
        #要离开时候每个人要等的时间
        totalwait+=getminutes(returnf[0])-earliestdep

#随机搜索,domain表示每个变量的最小最大值，costf表示成本函数
def randomoptimize(domain,costf):
    best = 999999999
    bestr = None
    for i in range(1000):
        #创建一个随机解
        r = [random.randint(domain[i][0],domain[i][1])]
        for i in range(len(domain)):
            cost = costf(r)
            if cost<best:
                best =cost
                bestr = r
        return r


#爬山方法 从一个随机的时间安排，然后让后某个人乘坐的航班稍早或者稍晚一些的安排，具有最低成本的安排将成为新的题解
def hillclimb(domain,costf):
    #创建一个随机解
    sol=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
    while 1:
        neighbors = []
        for j in range(len(domain)):
            if sol[j]>domain[j][0]:
                neighbors.append(sol[0:j] + [sol[j]-1] + sol[j+1:])
            if sol[j]>domain[j][1]:
                neighbors.append(sol[0:j] + [sol[j] + 1] +sol[j+1:])
        current = costf(sol)
        best = current
        for j in range(len(neighbors)):
            cost  = costf(neighbors[j])
            if cost <best:
                best =cost
                sol =neighbors[j]
            if best == current:
                break
        return sol
