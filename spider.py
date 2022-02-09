
import requests
import re
import os
import urllib.request as r
import time

    
#爬取网页
def get_link(url):
    # url = 'https://bgm.tv/calendar'
    #headers
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
    proxy=r.getproxies() #获取代理
    proxies = {
        "http": proxy['http'],
        "https": proxy['http']
    }
    # bangumi_content = requests.get(url, proxies=proxies, headers=headers)
    status = count = 0
    max_count = 5 #最大重试次数

    while status != 200 and count < max_count:
        try:
            bangumi_content = requests.get(url, proxies=proxies, headers=headers)
            status = bangumi_content.status_code
        except:
            count += 1
        
    #访问失败
    if count == max_count:
        print('访问失败！')
        return False
    
    #访问成功
    else:
        print('访问成功！')
        return bangumi_content

## 解析番剧日历信息，返回图片直链列表
def parse_bangumi_calendar(bangumi_content):
    if bangumi_content !=False:
        week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        bangumi_content.encoding='utf-8'
        txt=repr(bangumi_content.text)
        date_list = []
        #包含图片直链的日期标签爬取
        for i in range(0,7):
            date_list.append(re.findall(r'<dd class="%s">.*?</dd>' % week[i], txt))

        #番剧名称和图片直链爬取，存进列表
        bangumi_name_list_cn = []
        # bangumi_name_list_jp = []
        img_url_list = []
        for i in range(0,7):
            temp=[]

            #中文名称列表解析
            name_list_cn = re.findall(r'class="nav">[^(<small><em>.*?</em></small>)]*?</a>', date_list[i][0])
            for j in range(0,len(name_list_cn)):
                temp.append(name_list_cn[j][12:-4])
            bangumi_name_list_cn.append(temp)

            temp=[]

            #图片直链列表解析
            img_link_list = re.findall(r'background:url.*?\)', date_list[i][0])
            for j in range(0,len(img_link_list)):
                temp.append('https:'+img_link_list[j][17:-3])
            img_url_list.append(temp)
        
        total_list = []
        total_list.append(bangumi_name_list_cn)
        total_list.append(img_url_list)
        

        return total_list

    else:
        return False

## 保存图片
def downloader(total_list):
    if total_list != False:
        week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

        for i in range(0,7):
        #获取图片直链列表
            img_url_list = total_list[1][i]

        #获取番剧名称列表
            # bangumi_name_list_cn = total_list[0][i]

        #获取图片保存路径
            img_save_path = os.getcwd()+'\\'+'img'+'\\'+week[i]

        #创建图片保存路径
            if not os.path.exists(img_save_path):
                os.makedirs(img_save_path)

        #保存图片
            for j in range(0,len(img_url_list)):
                img = get_link(img_url_list[j])
                if img != False:
                    with open(img_save_path+'\\'+str(j)+'.jpg', 'wb') as f:
                        f.write(img.content)
                        print('%s.jpg 下载完成！' % str(j))
    else:
        print('获取图片失败！')




if __name__ == '__main__':
    downloader(parse_bangumi_calendar(get_link('https://bgm.tv/calendar')))