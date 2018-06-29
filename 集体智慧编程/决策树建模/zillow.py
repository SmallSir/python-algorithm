import urllib.request
import requests
import xml.dom.minidom
zwskey = "X1-ZWzlchwxis15aj_9skq6"

#以地址和城市作为输入参数，并构造URL进行咨询房产信息
def getadderssdata(address,city):
    escad = address.replace(' ','+')
    #构造url
    url = 'http://www.zillow.com/webservice/GetDeepSearchResults.htm?zws-id=%s&address=%s&citystatezip=%s' %(zwskey,escad,city)
    #解析XML形式的返回结果
    doc = xml.dom.minidom.parseString(urllib.request.urlopen(url).read())
    code = doc.getElementsByTagName('code')[0].firstChild.data
    #状态码为0代表操作成功，否则代表有错误发生
    if code != '0':
        return None
    try:
        zipcode = doc.getElementsByTagName('zipcode')[0].firstChild.data
        use = doc.getElementsByTagName('useCode')[0].firstChild.data
        year = doc.getElementsByTagName('yearBuilt')[0].firstChild.data
        bath = doc.getElementsByTagName('bathrooms')[0].firstChild.data
        bed = doc.getElementsByTagName('bedrooms')[0].firstChild.data
        rooms = doc.getElementsByTagName('totalRooms')[0].firstChild.data
        price = doc.getElementsByTagName('amount')[0].firstChild.data
    except:
        return None
    return (zipcode,use,int(year),float(bath),int(bed),int(rooms),price)

def getpricelist():
    l1 = []
    with open('addresslist.txt','r') as fp:
        lines = fp.readlines()
        line = lines.pop()
        data = getadderssdata(line.strip(),'Cambridge,MA')
        l1.append(data)
    return l1
#利用方差进行计算
def variance(rows):
    if len(rows)==0:
        return 0
    data = [float(row[len(row)-1]) for row in rows]
    mean = sum(data)/len(data)
    variance = sum([(d-mean)**2 for d in data])/len(data)
    return variance
#递归方式建决策树
def buildtree(rows,scoref = variance):
    if len(rows) == 0:
        return decisionnode()
    current_score = scoref(rows)
    #定义一些变量以记录最佳拆分条件
    best_gain = 0.0
    best_criteria = None
    best_sets = None

    column_count = len(rows[0]) - 1
    for col in range(0,column_count):
        #在当前列中生成一个由不同值构成的序列
        column_value = {}
        for row in rows:
            column_value[row[col]] = 1
        #接下来根据这一列中的每个值，尝试对数据集进行拆分
        for value in column_value.keys():
            (set1,set2) = divideset(rows,col,value)
            #信息增益
            p =float(len(set1))/len(rows)
            gain = current_score-p*scoref(set1) - (1-p) * scoref(set2)
            if gain>best_gain and len(set1) >0 and len(set2)>0:
                best_gain = gain
                best_criteria = (col,value)
                best_sets = (set1,set2)
    #创建子分支
    if best_gain > 0:
        trueBranch = buildtree(best_sets[0])
        falseBranch = buildtree(best_sets[1])
        return decisionnode(col = best_criteria[0],value=best_criteria[1],tb = trueBranch,fb = falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))
#计算分支宽度
def getwidth(tree):
    if tree.tb  == tree.fb and tree.fb == None:
        return 1
    return getwidth(tree.tb) + getwidth(tree.fb)
#计算分支深度
def getdepth(tree):
    if tree.tb == tree.fb and tree.tb == None:
        return 0
    return max(getdepth(tree.tb),getdepth(tree.fb))+1
#为绘制的树确定一个合理尺寸
def drawtree(tree,jpeg='tree.jpg'):
    w = getwidth(tree) * 100
    h = getdepth(tree) * 100 +120

    img = Image.new('RGB',(w,h),(255,255,255))
    draw = ImageDraw.Draw(img)

    drawnode(draw,tree,w/2,20)
    img.save(jpeg,'JPEG')
#绘制决策树的节点
def drawnode(draw,tree,x,y):
    if tree.results == None:
        #得到每个分支的宽度
        w1 = getwidth(tree.fb) * 100
        w2 = getwidth(tree.tb) * 100

        #确定此节点所需要占据的总空间
        left = x - (w1+w2)/2
        right = x+(w1+w2)/2

        #绘制判断条件的字符串
        draw.text((x-20,y-20),str(tree.col)+':'+str(tree.value),(0,0,0))

        #绘制到分支的连线
        draw.line((x,y,left+w1/2,y+100),fill=(255,0,0))
        draw.line((x,y,right-w2/2,y+100),fill=(255,0,0))

        #绘制分支的节点
        drawnode(draw,tree.fb,left+w1/2,y+100)
        drawnode(draw,tree.tb,right-w2/2,y+100)
    else:
        txt = ' \n'.join(['%s:%d'%v for v in tree.results.items()])
        draw.text((x-20,y),txt,(0,0,0))
housedata = getpricelist()
housetree = buildtree(housedata,scoref=variance)
drawtree(housetree,'housetree.jpg')


