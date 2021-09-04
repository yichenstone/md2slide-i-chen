import requests


# img_link = input("自定义背景图片\n请拖入背景图片或粘贴图片网络链接：")
# img_link = "http://www.51pptmoban.com/d/file/2017/05/22/4f4267b7ec2f610f17453d0a8b63dd38.jpg"

def img_backgroud_set():
    try:
        img_link = input("自定义背景图片\n请拖入背景图片或粘贴图片网络链接：")
        if img_link[:4] != "http":
            with open(img_link ,"rb") as file:
                img = file.read()
            with open("./reveal.js/css/theme/img_userset.jpg","wb") as file:
                file.write(img)

            with open("./reveal.js/css/theme/userset.css","r",encoding="utf-8-sig") as file:
                userset = file.readlines()
            userset[19] = "  background-image: url(img_userset.jpg);\n "

            with open("./reveal.js/css/theme/userset.css","w",encoding="utf-8") as file:
                file.writelines(userset)
        else:
            img = requests.get(img_link).content
            with open("./reveal.js/css/theme/img_userset.jpg","wb") as file:
                file.write(img)

            with open("./reveal.js/css/theme/userset.css","r",encoding="utf-8-sig") as file:
                userset = file.readlines()
            userset[19] = "  background-image: url(img_userset.jpg);\n "

            with open("./reveal.js/css/theme/userset.css","w",encoding="utf-8") as file:
                file.writelines(userset)
    except:
        input("自定义背景图片出错，请检查图片链接地址！")

img_backgroud_set()






















