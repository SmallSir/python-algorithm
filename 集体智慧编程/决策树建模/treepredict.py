my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]


class decisionnode:
        def __init__(self,col = -1,value = None,results =None,tb = None,fb = None):
                self.col = col#待检验的判断条件所对应的列索引值
                self.value = value#对应为了使结果为true，当前列必须匹配的值
                self.results = results#保存的事针对于当前分支的结果
                self.tb = tb
                self.fb = fb
                #树上相对于当前节点的字数上的节点
#根据列表中某一栏的数据将列表拆分成两个数据集合,rows指的是列表，column表示进行划分的依据列所在位置，value表示划分的参考值
def divideset(rows,column,value):
        split_function =None
        if isinstance(value,int) or isinstance(value,float):
                split_function = lambda  row:row[column] >=value
        else:
                split_function = lambda row:row[column] == value
        set1 = [row for row in rows if split_function(row)]
        set2 = [row for row in rows if not split_function(row)]
        return (set1,set2)
#找出所有不同的可能结果，返回一个字典，rows表示的是列表
def uniquecounts(rows):
        results = {}
        for row in rows:
                r = row[len(row) - 1]
                if r not in results:
                        results[r] = 0
                results[r]+=1
        return results
#基尼不纯度 随机放置的数据项出现于错误分类中的概率
def giniimpurity(rows):
        total = len(rows)
        counts = uniquecounts(rows)
        imp = 0
        for k1 in counts:
                p1 = float(counts[k1])/total
                for k2 in counts:
                        if k1 == k2:
                                continue
                        p2 = float(counts[k2])/total
                        imp+=p1*p2
        return imp
#熵
def entropy(rows):
        from math import log
        log2 = lambda x:log(x)/log(2)
        results = uniquecounts(rows)
        #此处开始计算熵
        ent = 0.0
        for r in results.keys():
                p = float(results[r])/len(rows)
                ent =ent-p*log2(p)
        return ent
