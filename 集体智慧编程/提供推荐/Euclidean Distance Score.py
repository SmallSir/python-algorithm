from recommendations import critics
from math import sqrt


#欧几里得距离
def sim_distance(person1,person2):
    si={}
    for item in person1:
        if item in person2:
            si[item] = 1
    if len(si) == 0:#判断是否有共同之处，没有就返回0
        return 0
    sum = 0
    for item in critics[person1]:
        if item in critics[person2]:
            sum = sum + pow((critics[person2][item]-critics[person1][item]),2)#计算所有差值的平方和
    return 1/(1+sqrt(sum))
print(sim_distance('Lisa Rose','Gene Seymour'))