from bangumi_spider import get_link
import time
import random
import pickle
import os

yiyan_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"), "yiyan")
url='https://v1.hitokoto.cn/?c=a&c=b&c=c&c=d&c=i&c=j&c=k'

yiyan_list = []
for i in range(1000):
    yiyan=get_link(url)
    print(yiyan)

    if yiyan:
        yiyan.encoding='utf-8'
        yiyan=yiyan.json()
        if yiyan["from_who"]!=None:
            saying=yiyan["hitokoto"]+'\n'+'{0:>{length}}'.format(r"———"+yiyan["from_who"], length=2*len(yiyan["hitokoto"]))
        elif yiyan["from"]!=None:
            saying=yiyan["hitokoto"]+'\n'+'{0:>{length}}'.format(r"———"+yiyan["from"], length=2*len(yiyan["hitokoto"]))
        else:
            saying=yiyan["hitokoto"]
        yiyan_list.append(saying)

    else:
        print('一言爬取失败')

    time.sleep(random.randint(0,3)+float(float(random.randint(1,10)/10)))

with open(yiyan_path,'wb') as f:
    pickle.dump(yiyan_list,f)