# -!- coding: utf-8 -!-
import os
from pathlib import Path
import json
import re
import time
import datetime
import shutil
import requests
from PIL import Image
import sys
import pywintypes
import win32api,win32con
from bs4 import BeautifulSoup

########修改config.json默认配置
def modify_config():
    # 转换后幻灯保存的默认位置
    ###桌面路径
    def get_desktop():
        key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                                  r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 0,
                                  win32con.KEY_READ)
        return win32api.RegQueryValueEx(key, 'Desktop')[0]

    def export_input(config_text):
        export = input("请选择转换后幻灯保存的默认位置：\n回复【1】桌面\n回复【2】软件所在文件夹\n你的选择是：")
        try:
            if int(export) == 1:
                desktop = get_desktop()
                config_text['revealjs_export_dir'] = desktop + "/导出的幻灯"
            elif int(export) == 2:
                config_text['revealjs_export_dir'] = "导出的幻灯"
            else:
                print("\n你的输入错误，请重新输入")
                export_input(config_text)
        except BaseException as e:
            print("\n你的输入错误，请重新输入")
            export_input(config_text)
        return config_text

    # 主题输入
    def theme_input(config_text):
        theme = input(
            "请选择默认使用的主题：\n回复【1】米色背景\n回复【2】黑色背景\n回复【3】黑背景，红色光标\n回复【4】黑色背景，中间微亮\n回复【5】深海蓝\n回复【6】黑色背景，驼色光标\n回复【7】浅灰色背景\n回复【8】白色背景，蓝色光标\n回复【9】浅蓝色背景，中间微亮\n回复【10】浅粉色背景\n回复【11】白色背景，蓝色光标\n回复【12】自定义背景（浅色背景）\n回复【13】自定义背景（深色背景）\n你的选择是：")
        try:
            if int(theme) == 1:
                config_text['revealjs_theme'] = "beige"
            elif int(theme) == 2:
                config_text['revealjs_theme'] = "black"
            elif int(theme) == 3:
                config_text['revealjs_theme'] = "blood"
            elif int(theme) == 4:
                config_text['revealjs_theme'] = "league"
            elif int(theme) == 5:
                config_text['revealjs_theme'] = "moon"
            elif int(theme) == 6:
                config_text['revealjs_theme'] = "night"
            elif int(theme) == 7:
                config_text['revealjs_theme'] = "serif"
            elif int(theme) == 8:
                config_text['revealjs_theme'] = "simple"
            elif int(theme) == 9:
                config_text['revealjs_theme'] = "sky"
            elif int(theme) == 10:
                config_text['revealjs_theme'] = "solarized"
            elif int(theme) == 11:
                config_text['revealjs_theme'] = "white"
            elif int(theme) == 12:
                config_text['revealjs_theme'] = "userset_light"
                img_backgroud_set_light()
            elif int(theme) == 13:
                config_text['revealjs_theme'] = "userset_dark"
                img_backgroud_set_dark()
            else:
                print("\n你的输入错误，请重新输入")
                theme_input(config_text)
        except BaseException as e:
            print("\n你的输入错误，请重新输入")
            theme_input(config_text)
        return config_text

    # 翻页动画输入
    def transition_input(config_text):
        transition = input("请选择默认翻页模式：\n回复【1】无\n回复【2】淡出\n回复【3】滑动\n回复【4】凸\n回复【5】凹\n回复【6】缩放\n你的选择是：")
        try:
            if int(transition) == 1:
                config_text['revealjs_transition'] = "none"
            elif int(transition) == 2:
                config_text['revealjs_transition'] = "fade"
            elif int(transition) == 3:
                config_text['revealjs_transition'] = "slide"
            elif int(transition) == 4:
                config_text['revealjs_transition'] = "convex"
            elif int(transition) == 5:
                config_text['revealjs_transition'] = "concave"
            elif int(transition) == 6:
                config_text['revealjs_transition'] = "zoom"
            else:
                print("\n你的输入错误，请重新输入")
                transition_input(config_text)
        except BaseException as e:
            print("\n你的输入错误，请重新输入")
            transition_input(config_text)
        return config_text

    # 处理转换
    def config_trans(config_text):
        print("----------------------------------------")
        print("----------------------------------------")
        print("默认设置配置部分：")
        print("----------------------------------------")
        export_input(config_text)
        print("----------------------------------------")
        config_text['author_name_english'] = input("请输入你的英文名:")
        print("----------------------------------------")
        config_text['author_name_chinese'] = input("请输入你的中文名:")
        print("----------------------------------------")
        theme_input(config_text)
        print("----------------------------------------")
        transition_input(config_text)
        print("----------------------------------------")
        return config_text

    # 加载
    road = "./config.json"
    with open(road, 'r', encoding='utf-8-sig') as file:
        config_text = file.read()
    config_text = json.loads(config_text)
    config_text = config_trans(config_text)
    print("默认参数修改成功")
    # print(config_text)
    # 写入文件
    with open(road, 'w', encoding='utf-8') as file:
        config_text = json.dumps(config_text)
        file.write(config_text)

########用户自定义背景（浅色）
def img_backgroud_set_light():
    print("----------------------------------------")
    last_set = input("是否沿用上一次背景？\n回复【1】是\n回复【2】否\n你的选择是：")
    if int(last_set) == 1:
        pass
    elif int(last_set) == 2:
        try:
            img_link = input("请拖入背景图片或粘贴图片网络链接：")
            if img_link[:4] != "http":
                with open(img_link, "rb") as file:
                    img = file.read()
                with open("./reveal.js/css/theme/img_userset_light.jpg", "wb") as file:
                    file.write(img)

                with open("./reveal.js/css/theme/userset_light.css", "r", encoding="utf-8-sig") as file:
                    userset = file.readlines()
                userset[19] = "  background-image: url(img_userset_light.jpg);\n "

                with open("./reveal.js/css/theme/userset_light.css", "w", encoding="utf-8") as file:
                    file.writelines(userset)
            else:
                img = requests.get(img_link).content
                with open("./reveal.js/css/theme/img_userset_light.jpg", "wb") as file:
                    file.write(img)

                with open("./reveal.js/css/theme/userset_light.css", "r", encoding="utf-8-sig") as file:
                    userset = file.readlines()
                userset[19] = "  background-image: url(img_userset_light.jpg);\n "

                with open("./reveal.js/css/theme/userset_light.css", "w", encoding="utf-8") as file:
                    file.writelines(userset)
        except:
            input("自定义背景图片出错，请检查图片链接地址！")
            img_backgroud_set_light()
    else:
        print("\n你的输入错误，请重新输入")
        img_backgroud_set_light()

########用户自定义背景（深色）
def img_backgroud_set_dark():
    print("----------------------------------------")
    last_set = input("是否沿用上一次背景？\n回复【1】是\n回复【2】否\n你的选择是：")
    if int(last_set) == 1:
        pass
    elif int(last_set) == 2:
        try:
            img_link = input("请拖入背景图片或粘贴图片网络链接：")
            if img_link[:4] != "http":
                with open(img_link, "rb") as file:
                    img = file.read()
                with open("./reveal.js/css/theme/img_userset_dark.jpg", "wb") as file:
                    file.write(img)

                with open("./reveal.js/css/theme/userset_dark.css", "r", encoding="utf-8-sig") as file:
                    userset = file.readlines()
                userset[19] = "  background-image: url(img_userset_dark.jpg);\n "

                with open("./reveal.js/css/theme/userset_dark.css", "w", encoding="utf-8") as file:
                    file.writelines(userset)
            else:
                img = requests.get(img_link).content
                with open("./reveal.js/css/theme/img_userset_dark.jpg", "wb") as file:
                    file.write(img)

                with open("./reveal.js/css/theme/userset_dark.css", "r", encoding="utf-8-sig") as file:
                    userset = file.readlines()
                userset[21] = "  background-image: url(img_userset_dark.jpg);\n "

                with open("./reveal.js/css/theme/userset_dark.css", "w", encoding="utf-8") as file:
                    file.writelines(userset)
        except:
            input("自定义背景图片出错，请检查图片链接地址！")
            img_backgroud_set_dark()
    else:
        print("\n你的输入错误，请重新输入")
        img_backgroud_set_dark()
########converter
class MarkdownConverter():

    def __init__(self, *args, **kwargs):
        self.source_md_fname = Path(args[0]).expanduser().absolute() 
        if self.source_md_fname.suffix == ".textbundle":
            #text bundle:
            markdown_suffix_list = list(self.source_md_fname.glob("*.markdown"))
            md_suffix_list = list(self.source_md_fname.glob("*.md"))
            self.source_md_fname = (markdown_suffix_list + md_suffix_list)[0]
        self.working_folder = Path(self.source_md_fname).parent
        self.code_dir = Path(__file__).absolute().parent
        config_json_fname = kwargs['path']
        self.config = json.load(open(config_json_fname,encoding='utf-8-sig'))
        self.temp_md_fname = self.working_folder/"temp.md"
        with open(self.source_md_fname,encoding='utf-8-sig') as f:
            self.md_content = f.read()
        self.download_dir = self.working_folder / 'downloaded_images'

    def show_md(self, md_fname = None):
        if not(md_fname):
            md_fname = self.source_md_fname
        cmd = "open {}".format(md_fname)
        os.system(cmd)

    def update_source_md(self):
        with open(self.source_md_fname, 'w',encoding='utf-8') as f:
            f.write(self.md_content)

    def get_absolute_path(self, link):
        # image helper of markdown preview plus for vscode bug:
        if str(link).startswith('/assets/'):
            link = Path(str(link)[1:])
        # convert a arbitary path to absolute ones
        link_path = Path(link).expanduser()
        if not link_path.is_absolute():
            link_path = self.working_folder / link
        return link_path

    def get_file_mtime(self, link):
        try:
            return self.get_absolute_path(link).stat().st_mtime
        except:
            print("图片链接错误，请检查文件中图片位置是否正确！")
            input()
            sys.exit(0)

    def get_formated_mtime_filename(self, link):
            my_mtime = self.get_file_mtime(link)
            d = datetime.datetime.fromtimestamp(my_mtime)
            date_format = '%Y-%m-%d-%H-%M-%S-%f'
            timestr = d.strftime(date_format)
            suffix = self.get_absolute_path(link).suffix
            new_filename = f"assets/{timestr}{suffix}"
            return new_filename

    def get_formatted_current_time_filename(self):
        current_time = datetime.datetime.now()
        date_format = '%Y-%m-%d-%H-%M-%S-%f'
        timestr = current_time.strftime(date_format)
        return timestr


    def download_links(self):
        # prepare for the temp image download dir
        
        if self.download_dir.exists():
            shutil.rmtree(self.download_dir)
        self.download_dir.mkdir()
        new_links = []
        web_link_pattern = re.compile(r'(ht|f)tps?://')

        for link in self.original_image_links:
            if web_link_pattern.search(link): # is a web link
                ext_patt = r"\.(jpg|png|bmp|gif|svg|jpeg)"
                suffix = re.search(ext_patt, link, re.MULTILINE | re.IGNORECASE).group(1)
                download_image_filename = f"{self.get_formatted_current_time_filename()}.{suffix}"
                r = requests.get(link, stream=True)
                new_link = self.download_dir/download_image_filename
                with open(new_link, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                new_links.append(new_link)
            else:
                new_links.append(link)

        self.generated_links = new_links
        self.replace_links()
        self.original_image_links = self.generated_links

    def clean_up_download_images(self):
        # remove the temp image download dir
        if self.download_dir.exists():
            shutil.rmtree(self.download_dir)
                

    def get_image_links(self, md_content):
        return re.findall(r'\!\[.*\]\((.*)\)', md_content)

    def generate_links(self):
        self.generated_links = []
        for link in self.original_image_links:
            new_link = self.get_formated_mtime_filename(link)
            self.generated_links.append(new_link)

    def copy_image_files(self):
        for link, new_link in zip(self.original_image_links, self.generated_links):
             if link != new_link:
                # need to move
                source = self.get_absolute_path(link)
                target = self.get_absolute_path(new_link)
                shutil.copy2(source, target)


    def replace_links(self):
        content = self.md_content
        for link, new_link in zip(self.original_image_links, self.generated_links):
            content = content.replace(str(link), str(new_link))
        self.md_content = content

    def generate_temp_md(self):
        with open(self.temp_md_fname, 'w',encoding='utf-8') as f:
            f.write(self.md_content)
        self.show_md(self.temp_md_fname)
        

    def convert(self):
               
        self.original_image_links = self.get_image_links(self.md_content)
        self.download_links()
        self.generate_links()
        self.replace_links()
        self.copy_image_files()
        self.clean_up_download_images()

##################revealjs_converter.py

class MarkdownRevealjsConverter(MarkdownConverter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_folder = self.config["revealjs_export_dir"]
        self.output_folder = Path(self.output_folder).expanduser()
        self.output_html = self.output_folder/"slide.html"
        self.temp_html = self.working_folder/"temp.html"
        self.revealjs_folder = self.code_dir/"reveal.js"


    def convert(self):
        # first, convert the self.md_content links to local
        super().convert()
        # convert markdown to slide markdown
        self.change_md_to_slide_md()
        # convert slide markdown to html with pandoc
        self.pandoc_slide_md_to_revealjs()
        # adjust several things in the html
        self.html_adjust()
        # output the html, along with revealjs and assets files
        self.make_output()
        # adjust several things in the html
        self.preview_slide()

    def preview_slide(self):
        # cmd = f"open {self.output_html}"
        try:
            # os.system(cmd)
            os.popen(self.output_html)
        except:
            # system other than unix-like ones
            try:
                cmd = f"start {self.output_html}"
                os.system(cmd)
            except:
                pass # do nothing if cannot open slide correctly


    def pandoc_slide_md_to_revealjs(self):
        # generate the temp md to run pandoc
        with open(self.temp_md_fname, 'w',encoding='utf-8') as f:
            f.write(self.md_content)
        cmd = f"""
        pandoc  -t revealjs\
        --standalone -i\
    --variable theme={self.config["revealjs_theme"]} \
    --variable transition={self.config["revealjs_transition"]} \
    {self.temp_md_fname} \
    -o {self.temp_html}
        """
        os.system(cmd)
        with open(self.temp_html,encoding='utf-8-sig') as f:
            self.html_content = f.read()

    def make_output(self):
        # prepare output dir
        # if folder exists, delete it.
        if self.output_folder.exists():
            shutil.rmtree(self.output_folder)
        # create output folder
        self.output_folder.mkdir()
        # create assets folder inside output folder
        (self.output_folder/"assets").mkdir()
        # sync reveal.js runtime
        shutil.copytree(self.revealjs_folder, self.output_folder/"reveal.js")
        # sync media
        for link in self.media_links:
            try:
                shutil.copy2(self.working_folder/link, self.output_folder/"assets")
            except:
                print(link+"  该视频链接错误，请检查文件中视频链接是否正确！")
                input()
                sys.exit(0)
        # write output html slide file
        with open(self.output_html, 'w',encoding='utf-8') as f:
            f.write(self.html_content)


    def html_adjust(self):
        data = self.html_content
        # print(data)
        # make pointer works

        keyboard_string = """
        keyboard: {
            39: 'next',
            37: 'prev',
            67: function() { RevealChalkboard.toggleNotesCanvas() },	// toggle notes canvas when 'c' is pressed
			66: function() { RevealChalkboard.toggleChalkboard() },	// toggle chalkboard when 'b' is pressed
			46: function() { RevealChalkboard.clear() },	// clear chalkboard when 'DEL' is pressed
			 8: function() { RevealChalkboard.reset() },	// reset chalkboard data on current slide when 'BACKSPACE' is presse
			88: function() { RevealChalkboard.colorNext() },	// cycle colors forward when 'x' is pressed
			89: function() { RevealChalkboard.colorPrev() },	// cycle colors backward when 'y' is pressed
        },
            
        chalkboard: {
            // optionally load pre-recorded chalkboard drawing from file
            src: "chalkboard.json",
            toggleChalkboardButton: { left: "80px" },
            toggleNotesButton: { left: "130px" },
        },
        """
        regex = r"(Reveal\.initialize\({)"
        subst = "\\1" + keyboard_string
        data = re.sub(regex, subst, data, 0, re.MULTILINE)

        #增加第三方脚本插件
        dependencies_string = """,
          { src: 'reveal.js/plugin/chalkboard/chalkboard.js' },
		  { src: 'reveal.js/plugin/menu/menu.js' },
        """
        regex = r"({ src: 'reveal.js/plugin/notes/notes.js', async: true })"
        subst = "\\1" + dependencies_string
        data = re.sub(regex, subst, data, 0, re.MULTILINE)

        # change background video to lazy loading controls stretch video element

        # regex = r"<section id=\"(.*?)\".*?class=\"(.*?)\".*?data-background-video=\"(.*?)\"(.*\n)*?</section>"
        # subst = "<section id=\"\\1\" class=\"\\2\"><video class=\"stretch\" data- controls>  <source data-src=\"\\3\" type=\"video/mp4\" /></video></section>"
        # data = re.sub(regex, subst, data, 0)
        #修改上面代码,设置视频为控制播放
        regex = r"<video class=\"stretch\" src=\"(.*?)\" data-autoplay controls>"
        subst = "<video class=\"stretch\" src=\"\\1\" data- controls>"
        data = re.sub(regex, subst, data, 0)

        # convert media links to export assets

        regex = r"img src=\"(.*?)\""
        inline_image_links = re.findall(regex, data)
        regex = r"data-background-image=\"(.*?)\""
        background_image_links = re.findall(regex ,data)
        regex = r"<video\s.*src=\"(.*)\""
        background_video_links = re.findall(regex, data)

        self.media_links = inline_image_links + background_image_links + background_video_links #下一步保存媒体文件

        # inline image path convert:
        regex = r"(img src=\")(.*)/(.*?)\""
        subst = "\\1assets/\\3\""
        data = re.sub(regex, subst, data, 0, re.MULTILINE)
        # background image path convert:
        regex = r"(data-background-image=\")(.*)/(.*?)\""
        subst = "\\1assets/\\3\""
        data = re.sub(regex, subst, data, 0, re.MULTILINE)
        # background video path convert:
        regex = r"<video\s.*src=\"(.*)\""  #修复导出视频链接位置错误
        old_video_list = re.findall(regex, data)
        # print(old_video_list[0].split("\\")[-1])
        new_video_list = old_video_list
        temp = list(old_video_list) #创建临时变量，复制列表
        for item in range(100):
            try:
                new_video_list[item] = "assets\\" + old_video_list[item].split("\\")[-1]
                data = data.replace(temp[item], new_video_list[item])
            except:
                break


        # regex = '<video".*"src="(.*)"' #测试
        # subst = "\\1assets/\\3\""
        # subst = "assets\\"+regex.split('\\')[-1]
        # data = re.sub(regex, subst, data, 0, re.MULTILINE)

        # remove all the section id in Chinese slides:
        # if self.is_chinese_slide:
        #     regex = r"(<section\s+)id=\".*\"\s"
        #     subst = "\\1"
        #     data = re.sub(regex, subst, data, 0, re.MULTILINE)


        self.html_content = data

    def check_contain_chinese(self, check_str):
        # for ch in check_str.decode('utf-8'):
        for ch in check_str:
            if '\u4e00' <= ch <= '\u9fff':
                return True
        return False

    def change_md_to_slide_md(self):



        data = self.md_content

        # handle blank lines between list items

        regex = r"^$\n(^\s*[-\*])"
        subst = "\\1"
        data = re.sub(regex, subst, data, 0, re.MULTILINE)

        # change title line from h1 to title
        regex = r"^# (.*)"
        title = re.match(regex, data, flags=re.MULTILINE).group(1)

        now = datetime.datetime.now()

        self.is_chinese_slide = self.check_contain_chinese(title)

        if self.is_chinese_slide: #contains chinese characters in title:
            author = self.config["author_name_chinese"]
            date = "{}年{}月".format(now.year, now.month)
            end_string = "\n\n## {}\n\n{}".format("放映结束", "谢谢观赏！")

        else: # English title
            author = self.config["author_name_english"]
            date = now.strftime("%b %Y")
            end_string = "\n\n## {}\n\n{}".format("The End", "Thanks for your time!")

        subst = "% \\1\\n% {}\\n% {}".format(author, date)
        data = re.sub(regex, subst, data, 0, re.MULTILINE)


        # change h2 title to h1 title
        regex = r"^## (.*)"
        subst = "# \\1"
        data = re.sub(regex, subst, data, 0, re.MULTILINE)

        # change h3 title to h2 title
        regex = r"^### (.*)"
        subst = "## \\1"
        data = re.sub(regex, subst, data, 0, re.MULTILINE)

        # change separated inline image to one line
        regex = r"^\s*[-\*]\s+\n+!\["
        subst = "* !["
        data = re.sub(regex, subst, data, 0, re.MULTILINE)


        # make background images to separate slide
        regex = r"^ *!\[.*\]\((.*)\)"
        subst = "\n\n##  {data-background-image=\"\\1\" data-background-size=\"contain\"}"
        data = re.sub(regex, subst, data, 0, re.MULTILINE)


        # # make video links to separate video slide （老师）
        regex = r"^ *\[video\]\((.*)\)"
        subst = "\n\n## {} \n\n<video class=\"stretch\" src=\"\\1\" data-autoplay controls></video>"
        data = re.sub(regex, subst, data, 0, re.MULTILINE)

        # change inline images to html link
        regex = r"^ *([-\*])\s+!\[(.*)\]\((.*)\)"
        subst = "\\1 <img src=\"\\3\" style=\"border-style: none\" alt=\"\\2\">"
        data = re.sub(regex, subst, data, 0, re.MULTILINE)

        # resize inline images
        regex = r"^[\*-] +<img src=\"(.*?)\".*"
        links = re.findall(regex, data, re.MULTILINE)

        for link in links:
            # print(link)
            with Image.open(self.working_folder / link) as im:
                width, height = im.size
            if height>width and height>400:
                regex = r"^(.*" + link + r".*?alt=\".*?\").*?>"
                subst = "\\1 height=\"400\">"
                data = re.sub(regex, subst, data, 0, re.MULTILINE)

        data = data + end_string

        self.md_content = data

##################幕布html2md
# 写入md文件
def write_file(new_html):
    # 如果路径不存在就创建，如果不存在就不创建
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    with open("./temp/html2md_temp.md","w",encoding='utf-8') as file:
        file.writelines(new_html)

# 转换函数
def html2md(md_fname):
    html = BeautifulSoup(open(md_fname,encoding='utf-8'),features='html.parser')
    # print(html)

    new_html = []

    title = html.find_all('head')[0].title.text
    title_md = "# "+title+"\n\n" #拿到标题
    new_html.append(title_md)

    body = html.find_all('body')[0]

    # 进行编码排序
    for item_1 in range(10000):
        try:#找文字
            one_list = body.find_all('li')
            one_content = one_list[item_1].find_all('div',attrs={"class":"content"})[0]
            one_word_append =[]
            for item_2 in range(50):
                try:
                    onespan = one_content.find_all('span')[item_2]
                    onetext = onespan.text #导图中一级标题内容
                    try: #文字加粗、斜体、下划线、颜色、超链接
                        tag = onespan.attrs["class"]
                        herf = 0
                        try:#获取超链接的地址
                            herf = onespan.parent.attrs["href"]
                        except:
                            pass
                        onetext = DealWord(tag,onetext,herf) #转接文字处理
                    except:
                        pass
                    one_word_append.append(onetext)
                except:
                    break

            # 将content内容转换成一个字符串
            one_text = "".join(one_word_append)

            # 通过[视频]制作视频
            if one_text[:4] == "[视频]" or one_text[:4] == "【视频】" or one_text[:4] == "(视频)" or one_text[:4] == "（视频）":
                # print(one_text[:4])
                one_text = one_text.replace("\\", "\\")
                one_text = "[video](" + one_text[4:] +")\n\n"
                new_html.append(one_text)
            elif one_text[:1] == "|":  #通过|制作表格
                if new_html[len(new_html) - 1][:3] == "## ":
                    one_text = "###   \n" + one_text
                if new_html[len(new_html) - 1][:4] == "### ":
                    one_text = "###   \n" + one_text
                if new_html[len(new_html) - 1][:2] == "- ":
                    new_html[len(new_html) - 1] = "###   \n"+new_html[len(new_html) - 1][2:]
                one_text = one_text+"\n"
                new_html.append(one_text)
            else:#制作前标识符
                one_text = "- "+one_text+"\n\n"
                try:
                    two_list = one_list[item_1].find_all('ul',attrs={"class":"node-list"})[0]
                    one_text = "### " + one_text[2:]
                    if new_html[len(new_html) - 1][:3] == "![]" and new_html[len(new_html) - 1][-8:-5] == "###":
                        new_html[len(new_html) - 1] = new_html[len(new_html) - 1][:-8] 
                    else:
                        pass
                except BaseException as e:
                    pass
                try:
                    three_list = one_list[item_1].find_all('ul',attrs={"class":"node-list"})[0].find_all('ul',attrs={"class":"node-list"})[0]
                    one_text = "## " + one_text[4:]
                except BaseException as e:
                    pass
                try:
                    new_html_last = str(new_html[len(new_html) - 1])
                    # print(new_html_last)
                    if new_html_last[:3] == "## ":
                        if one_text[:2] == "- ":
                            one_text = "### " + one_text[2:]
                except BaseException as e:
                    pass
                new_html.append(one_text) #录入
        except:
            try:#找图片
                one_list = body.find_all('li')
                img = one_list[item_1].find_all("img")[0].attrs["src"]  # 找图片链接
                img_text = "![](" + img + ")\n\n"
                # print(img_text)
                if new_html[len(new_html) - 1][:3] == "![]":
                    new_html[len(new_html) - 1] = new_html[len(new_html) - 1][:-8]
                    img_text = img_text + "###   \n\n"
                    new_html.append(img_text)
                elif new_html[len(new_html) - 1][-6:-2] =="【背景】" or new_html[len(new_html) - 1][-6:-2] =="[背景]" or new_html[len(new_html) - 1][-6:-2] =="（背景）" or new_html[len(new_html) - 1][-6:-2] =="(背景)":
                    new_html[len(new_html) - 1] = img_text
                else:
                    img_text = img_text + "###   \n\n"
                    new_html[len(new_html) - 1] = img_text
            except:
                break
    # print(new_html)
    write_file(new_html)

def DealWord(tag,onetext,herf): #文字效果处理
    if tag[0] == "bold": #加粗
        onetext = "**" + onetext + "**"
    elif tag[0] == "italic": #斜体
        onetext = "*" + onetext + "*"
    elif tag[0] == "underline": #下划线
        onetext ="<u>" + onetext + "</u>"
    elif tag[0] == "text-color-red": #颜色-红
        onetext ="<font color=#dc2d1e>" + onetext + "</font>"
    elif tag[0] == "text-color-yellow": #颜色-黄
        onetext ="<font color=#ffaf38>" + onetext + "</font>"
    elif tag[0] == "text-color-green": #颜色-绿
        onetext ="<font color=#75c940>" + onetext + "</font>"
    elif tag[0] == "text-color-blue": #颜色-蓝
        onetext ="<font color=#3da8f5>" + onetext + "</font>"
    elif tag[0] == "text-color-purple": #颜色-紫
        onetext ="<font color=#797ec9>" + onetext + "</font>"
    elif tag[0] == "content-link-text": #超链接
        onetext ="<a class=\"content-link\" target=\"_blank\" href=\"" + herf + "\">" + onetext + "</a>"
    else:
        pass
    return onetext

##################读入md文件转为utf-8编码
def md_to_utf8(md_fname):
    with open(md_fname, 'r', encoding='utf-8-sig') as file:
        text = file.readlines()
    with open(md_fname, 'w', encoding='utf-8') as file:
        file.writelines(text)
        # print("转换完成")

##################桌面路径
def get_desktop_desktop():
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER,
                              r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 0,
                              win32con.KEY_READ)
    return win32api.RegQueryValueEx(key, 'Desktop')[0]
    
    
##################md2slide.py
print("----------------------------------------------------------------")
print("欢迎使用md2slide，关注微信公众号：一陈Stone，查看软件教程与更新。")
print("*感谢王树义老师提供的支持!       交流QQ群：811635560")
print("----------------------------------------------------------------\n")

#设置config.json文件
# 如果路径不存在就设置config
if os.path.exists('./导出的幻灯') or os.path.exists(get_desktop_desktop()+'/导出的幻灯'):
    pass
else:
    modify_config()

# get the dir of current python file
code_dir = Path(__file__).absolute().parent

try:
    md_fname = sys.argv[1]
except:
    md_fname = input("请拖入md文件或html文件到此窗口，然后回车")

if md_fname[-2:] == "ml":
    print("正在转换，请稍候……(html文件需从网络下载图片，等待时间稍长)")
    md_fname = md_fname.replace("\\", "\\\\")
    html2md(md_fname)
    md_fname = "temp/html2md_temp.md"
else:
    print("正在转换，请稍候……")
    md_to_utf8(md_fname)

# 如果路径不存在就创建，如果存在就不创建
road = os.path.dirname(os.path.realpath(md_fname))
if not os.path.exists(road + '/assets/'):
    os.mkdir(road + '/assets/')

config = dict()
config["path"] = code_dir/"config.json"

converter = MarkdownRevealjsConverter(md_fname, **config)
converter.convert()
print("转换完成\n")
print("----------------------------------------------------------------")
do_reset = input("\n你想重新设置默认参数么？(默认不修改)\n回复【1】是，\n回复【2】否\n你的选择是：")
try:
    if int(do_reset) == 1:
        modify_config()
    elif int(do_reset) == 2:
        pass
except BaseException as e:
    pass
input()
