from recommendations import critics
from math import sqrt

#皮尔逊相关系数
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



