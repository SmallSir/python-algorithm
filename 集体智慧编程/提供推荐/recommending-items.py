
from recommendations import critics
from math import sqrt
#皮尔逊相关度评价
def sim_person(p1,p2):
    si={}
    for item in critics[p1]:
        if item in critics[p2]:
            si[item] = 1
    if len(si) == 0:
        return 0

    #对共同的偏好计算之和
    sum1 = sum([critics[p1][it] for it in si])
    sum2 = sum([critics[p2][item] for item in si])
    #对共同的偏好计算之和求平方之和
    sq1 = sum([pow(critics[p1][item],2) for item in si])
    sq2 = sum([pow(critics[p2][item],2) for item in si])
    #对共同的偏好计算乘积之和
    summ = sum([critics[p1][item]*critics[p2][item] for item in si])
    #计算皮尔逊系数
    num = summ-(sum1 * sum2/ len(si))
    den = sqrt((sq1 - pow(sum1,2)/len(si))*(sq2-pow(sum2,2)/len(si)))
    if den == 0:
        return 0
    r = num / den
    return r

#推荐物品
def getRecommendations(person):
    totals = {}
    simSunms = {}
    for other in critics:
        #不与自己进行比较
        if other == person:
            continue
        #获得与其他人的皮尔逊相关系数
        sim = sim_person(person,other)
        if sim <= 0:
            continue
        for item in critics[other]:
            #只对自己还未曾看到过的影片进行评价
            if item not in critics[person] or critics[person][item] == 0:
                #将该电影不存在则初始化为0，存在则返回这个值
                totals.setdefault(item,0)
                #相似度*这个人对这个电影的打分
                totals[item] += critics[other][item] * sim
                simSunms.setdefault(item,0)
                #所有人对这个电影相似度和
                simSunms[item] += sim
        #用这部电影的相似度*打分之和/相似度之和得到每部电影的得分
        rankings = [(total/simSunms[item],item) for item,total in totals.items()]
        rankings.sort()
        rankings.reverse()
        return rankings
print(getRecommendations('Toby'))