
#匹配商品


#from recommendations import critics

def transformPrefs():
    result={}
    for person in critics:
        for item in critics[person]:
            result.setdefault(item,{})
            result[item][person] = critics[person][item]
    return result