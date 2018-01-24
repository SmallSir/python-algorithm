
from recommendations import critics

#构造物品比较数据集

def calcuateSunukarItems(n=10):
    result = {}
    #将之前以人为中心转换为以物品为中心对偏好矩阵实施倒置处理
    itemPrefs = transformPrefs(critics)
    c = 0
    for item in itemPrefs:
        #针对大数据集更新状态变量
        c+=1
        if c%100 == 0:
            print("%d / %d "%(c,len(itemPrefs)))
        #寻找最相近的物品
        scores = topMatches(item,n=n)
        result[item]=scores
    return result

