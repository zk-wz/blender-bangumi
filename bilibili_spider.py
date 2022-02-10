
from bangumi_spider import get_link
from bangumi_spider import muti_process_get_pic
import time
import os

def pre_handle_bilibili_calendar(bilibili_content):
    if bilibili_content:

        if bilibili_content['message'] == 'success':
            week_bangumi_list=[]#每周番剧列表
            all_bangumi_list=bilibili_content['result']#所有番剧列表
            now = str(time.localtime()[1])+'-'+str(time.localtime()[2])
            for i in range(len(all_bangumi_list)):
                #计算差值，获取当前周的番剧
                if all_bangumi_list[i]['date'] == now:
                    day_of_week = all_bangumi_list[i]['day_of_week']
                    if day_of_week == 7:
                        delta_minus=0
                        delta_plus=6
                    else:
                        delta_minus=day_of_week
                        delta_plus=6-day_of_week
                    for j in range(delta_minus,-1,-1):
                        week_bangumi_list.append(all_bangumi_list[i-j])
                    for j in range(1,delta_plus+1):
                        week_bangumi_list.append(all_bangumi_list[i+j])
                    break
            return week_bangumi_list
                    
        else:
            print('获取番剧信息失败！')
            return False

    else:
        print('网络连接失败！')
        return False

#获取总列表
def parse_bilibili_calendar(week_bangumi_list):
    if week_bangumi_list:
        total_list=[]
        bangumi_name_list=[]
        bangumi_cover_list=[]
        bangumi_url_list=[]
        for i in range(0,7):
            bangumi_list=week_bangumi_list[i]['seasons']
            day_bangumi_name_list=[]
            day_bangumi_cover_list=[]
            day_bangumi_link_list=[]
            for each_bangumi in bangumi_list:
                day_bangumi_name_list.append(each_bangumi['title'])
                day_bangumi_cover_list.append(each_bangumi['square_cover'])
                day_bangumi_link_list.append(each_bangumi['url'])
            bangumi_name_list.append(day_bangumi_name_list)
            bangumi_cover_list.append(day_bangumi_cover_list)
            bangumi_url_list.append(day_bangumi_link_list)
        total_list.append(bangumi_name_list)
        total_list.append(bangumi_cover_list)
        total_list.append(bangumi_url_list)
        return total_list
    else:
        return False


## 保存图片
def downloader(total_list,i):
    if total_list:
        week = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        #获取图片直链列表
        img_url_list = total_list[1][i]

        #获取番剧名称列表
        bangumi_name_list_cn = total_list[0][i]
        # bangumi_name_list_jp = total_list[1][i]

        #获取图片保存路径
        img_save_path = os.getcwd()+'\\'+'img'+'\\'+week[i]

        #创建图片保存路径
        if not os.path.exists(img_save_path):
            os.makedirs(img_save_path)

        #保存图片
        for j in range(len(img_url_list)):
            #获取图片链接
            img = get_link(img_url_list[j])

            if img:
                #获取图片名称
                bangumi_name=bangumi_name_list_cn[j]

                with open(img_save_path+'\\'+str(j)+'.jpg', 'wb') as f:
                # with open(img_save_path+'\\'+bangumi_name+'.jpg', 'wb') as f:
                    f.write(img.content)
                    print('番剧：“%s” 的封面下载完成！' % bangumi_name)

def main():
    bilibili_content=get_link('https://bangumi.bilibili.com/web_api/timeline_global').json()
    week_bangumi_list=pre_handle_bilibili_calendar(bilibili_content)
    total_list=parse_bilibili_calendar(week_bangumi_list)
    # print(total_list)
    muti_process_get_pic(total_list,7,downloader)

if __name__ == '__main__':
    t=time.time()
    main()
    print('爬取完成！耗时：%s' % (time.time()-t))