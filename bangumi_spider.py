
import requests
import re
import os
import urllib.request as r
import time
from threading import Thread
import pickle

#获取代理
def get_proxy_():
    proxy=r.getproxies() #获取代理
    if len(proxy) != 0:
        proxies = {
            "http": proxy['http'],
            "https": proxy['https'].replace('https','http')
        }
        return proxies

    else:
        proxies = {
            "http": None,
            "https": None
        }
        return proxies



#爬取网页
def get_link(url):

    # url = 'https://bgm.tv/calendar'
    #headers
    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"}
    #获取代理
    proxies=get_proxy_()

    # bangumi_content = requests.get(url, proxies=proxies, headers=headers)
    status = count = 0
    max_count = 3 #最大重试次数

    while status != 200 and count < max_count:
        try:
            bangumi_content = requests.get(url, proxies=proxies, headers=headers)
            status = bangumi_content.status_code
            count += 1
        except:
            count += 1
        
    #访问失败
    if count == max_count:
        print('访问失败！')
        return False
    
    #访问成功
    else:
        # print('访问成功！')
        return bangumi_content




## 解析番剧日历信息，返回图片直链列表
def parse_bangumi_calendar(bangumi_content):

    if bangumi_content:
        week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        bangumi_content.encoding='utf-8'
        txt=repr(bangumi_content.text)
        date_list = []
        #包含图片直链的日期标签爬取
        for i in range(0,7):
            date_list.append(re.findall(r'<dd class="%s">.*?</dd>' % week[i], txt))

        #番剧名称和图片直链爬取，存进列表
        bangumi_name_list_cn = []
        bangumi_name_list_jp = []
        img_url_list = []
        bangumi_link_list = []
        for i in range(0,7):

            temp=[]

            #图片直链列表解析
            img_link_list = re.findall(r'background:url.*?\)', date_list[i][0])
            for j in range(len(img_link_list)):
                temp.append('https:'+img_link_list[j][17:-3])
            img_url_list.append(temp)


            #单独分离出每部番剧的部分，方便分离出名称
            each_bangumi=re.findall(r'<li.*?</li>', date_list[i][0])

            
            name_list_cn=[]
            name_list_jp=[]
            day_link_list=[]
            #若是有中文部分，则将中文名称添加到列表name_list_cn，否则添加空字符串，方便之后分离，日文同理
            #需要同时抓取日文和中文是因为有些番剧名称只有日文，没有中文
            for j in range(len(each_bangumi)):
                #中文部分
                name = re.findall(r'class="nav">[^(<small>.*?</small>)]*?</a>', each_bangumi[j])

                if len(name)!=0:
                    name_list_cn.append(name[0][12:-4])
                else:
                    name_list_cn.append('')

                #日文部分
                name = re.findall(r'class="nav"><small><em>.*?</em></small>', each_bangumi[j])

                if len(name)!=0:
                    name_list_jp.append(name[0][23:-13])
                else:
                    name_list_jp.append('')

                #番剧链接
                link = re.findall(r'<a href=".*?" class="nav">', each_bangumi[j])
                day_link_list.append(r"https://bgm.tv"+link[0][9:-14])

            # temp=[]

            #中文名称列表解析
            # for j in range(len(name_list_cn)):
            #     temp.append(name_list_cn[j])

            bangumi_name_list_cn.append(name_list_cn)


            # temp=[]

            #日文名称列表解析
            # for j in range(len(name_list_jp)):
            #     temp.append(name_list_jp[j])

            bangumi_name_list_jp.append(name_list_jp)

            # temp=[]
            
            #番剧链接列表解析
            bangumi_link_list.append(day_link_list)


        name_fix(bangumi_name_list_cn)
        name_fix(bangumi_name_list_jp)

        bangumi_name_list = []
        #获取图片名称
        for i in range(7):
            temp=[]
            for j in range(len(bangumi_name_list_cn[i])):
                if bangumi_name_list_cn[i][j]!='':
                    temp.append(bangumi_name_list_cn[i][j])
                else:
                    temp.append(bangumi_name_list_jp[i][j])
            bangumi_name_list.append(temp)

        #拼接以上列表
        #中文名称下标为0，日文名称下标为1，图片直链下标为2
        total_list = []
        total_list.append(bangumi_name_list)
        # total_list.append(bangumi_name_list_jp)
        total_list.append(img_url_list)
        total_list.append(bangumi_link_list)
        
        

        return total_list


    else:
        return False



#去除名称中的反斜杠
def name_fix(name_list):
    for i in range(len(name_list)):
        for j in range(len(name_list[i])):
            name_list[i][j] = name_list[i][j].replace('\\','')
    return name_list
    


## 保存图片
def downloader(total_list,i):
    if total_list:
        week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


        #获取图片直链列表
        img_url_list = total_list[1][i]

        #获取番剧名称列表
        bangumi_name_list = total_list[0][i]

        #获取图片保存路径
        # img_save_path = os.getcwd()+'\\'+'img'+'\\'+week[i]
        img_save_path = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)),'img'),"bangumi"),week[i])

        #创建图片保存路径
        if not os.path.exists(img_save_path):
            os.makedirs(img_save_path)

        #保存图片
        for j in range(len(img_url_list)):
            #获取图片链接
            img = get_link(img_url_list[j])

            if img:

                bangumi_name = bangumi_name_list[j]

                with open(os.path.join(img_save_path,str(j)+'.jpg'), 'wb') as f:
                # with open(img_save_path+'\\'+bangumi_name+'.jpg', 'wb') as f:
                    f.write(img.content)
                    print('番剧：“%s” 的封面下载完成！' % bangumi_name)

        # for i in range(0,7):
        # #获取图片直链列表
        #     img_url_list = total_list[1][i]

        # #获取番剧名称列表
        #     # bangumi_name_list_cn = total_list[0][i]

        # #获取图片保存路径
        #     img_save_path = os.getcwd()+'\\'+'img'+'\\'+week[i]

        # #创建图片保存路径
        #     if not os.path.exists(img_save_path):
        #         os.makedirs(img_save_path)

        # #保存图片
        #     for j in range(0,len(img_url_list)):
        #         img = get_link(img_url_list[j])
        #         if img != False:
        #             with open(img_save_path+'\\'+str(j)+'.jpg', 'wb') as f:
        #                 f.write(img.content)
        #                 print('%s.jpg 下载完成！' % str(j))

    else:
        print('获取图片失败！')


#多线程下载图片
def multi_process_get_pic(total_list,tread_num,target):

    treads = []
    for i in range(tread_num):
        treads.append(Thread(target=target, args=(total_list,i)))
    for i in treads:
        i.start()
    for i in treads:
        i.join()

# def test(total_list):
#     for i in range(0,7):
#         print(total_list[0][i])
#         # print(total_list[1][i])
#         # print(total_list[2][i])
#         print('\n')

#爬虫主函数
def bangumi_main():
    t=time.time()
    bangumi_content = get_link('https://bgm.tv/calendar')
    total_list = parse_bangumi_calendar(bangumi_content)

    #保存番剧信息，优化读取效率
    path=os.path.join(os.path.dirname(os.path.abspath(__file__)),'src')
    if not os.path.exists(path):
        os.makedirs(path)
    with open(os.path.join(path,'bangumi_info'),"wb") as f:
        pickle.dump(total_list,f)


    # downloader(total_list)
    multi_process_get_pic(total_list,7,downloader)
    # test(total_list)
    print('爬取完成！耗时：'+str(time.time()-t)+'秒')


# if __name__ == '__main__':
    # print(os.path.dirname(os.path.abspath(__file__)))
#     t=time.time()
#     spider()
#     print('爬取完成！共使用'+str(time.time()-t)+'秒')
    





