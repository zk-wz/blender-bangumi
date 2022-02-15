from .bangumi_spider import get_link
import os

def imgapi_dl(imgapi_style,imgapi_category):
    if imgapi_category != "cosplay":
        url = "https://imgapi.cn/api.php" + "?zd=" + imgapi_style + "&fl=" + imgapi_category
    else:
        url = "https://imgapi.cn/cos.php"
    img = get_link(url)
    if img:
        pic_path=os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "img"), "rand_img")
        if not os.path.exists(pic_path):
            os.makedirs(pic_path)

        pic_path = os.path.join(pic_path, "rand_img.jpg")

        with open(pic_path, 'wb') as f:
            f.write(img.content)
    else:
        print("获取图片失败！")

