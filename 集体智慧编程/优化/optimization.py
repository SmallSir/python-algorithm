


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
for line in file('schedule.txt'):
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
