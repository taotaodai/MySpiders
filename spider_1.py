# -*- coding:utf-8 -*-

'用于爬取http://uc.xinchengjy.cn/ 上的网课。'
'这个文件的功能主要是，获取vid和playsafe，再由polyv_m3u8解密，生成m3u8文件，用于下载视频片段。'
import os
import time
import requests
from Cryptodome.Cipher import AES
import hashlib

#自动化测试库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#代理抓包库
from browsermobproxy import Server
import polyv_m3u8

#http://yzkjh.beegoedu.com/
BASE_URL = "http://uc.xinchengjy.cn/"
# BASE_URL = "http://kc.zikao35.com/"

server = None
browser = None
def start(userName,passWord,courseCode,url = BASE_URL,zhang = 1,jie = 2,hintCallback = None):
    server = Server(r'D:\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
    server.start()
    proxy = server.create_proxy()
    
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    proxy.new_har(options={'captureHeaders': True, 'captureContent': True})
    
    # prefs= {
    # "profile.managed_default_content_settings.images":1,
    # "profile.content_settings.plugin_whitelist.adobe-flash-player":1,
    # "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player":1,
    # 'profile.default_content_setting_values':{'images': 1,'javascript':1,'stylesheet': 1}
    # }

    # chrome_options.add_experimental_option('prefs',prefs)
    
    browser = webdriver.Chrome(chrome_options=chrome_options)
    
    login_url = url + "login"
    browser.get(login_url)
    time.sleep(2)
    username = browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div[2]/form/div[1]/div/input")

    username.send_keys(userName)
    password = browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div[2]/form/div[2]/div/input")
    
    password.send_keys(passWord)
    
    #设置cookie自动登录，但是在这个网站无效
    # browser.add_cookie({
    #     'name': 'coksinfo',
    #     'value': 'eG0xMzUyNzIwMTIzMQ%3D%3D'
    # })
    
    wait_time = 15
    hint_login = "请在"+str(wait_time)+"秒内完成登录"
    print(hint_login)
    if hintCallback:
        hintCallback(hint_login)
    time.sleep(wait_time)
    #y「51-02139」计算机信息检索 y「51-02134」信息系统设计与分析 y「51-02136」Windows及应用 y「51-02129」信息资源建设
    #y「51-02133」信息政策与法规 y「51-02140」信息咨询 y「04741」计算机网络原理 y「04735」数据库系统原理 y「02323」操作系统概论
    #y「00537」中国现代文学史 y「51-02867」卫生统计学 y「51-04489」室内装饰材料 y「51-06918」工程图学基础 y「50-00185」商品流通概论
    #「00186」国际商务谈判
    browser.get(url + "topic/course/study/" + courseCode)
    
    time.sleep(5)
    #章节                                      //*[@id="app"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div/ul
    parent = browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div/ul")
    has_next_section = True
    current_section_index = zhang
    total = 0
    while(has_next_section):
        try:
            #第一章是默认展开的，之后的需要点击展开才能使内部的组件可被使用
            if(current_section_index > 1):
                hint_zhang = "请点击第"+str(current_section_index)+"章"
                print(hint_zhang)
                if hintCallback:
                    hintCallback(hint_zhang)
                time.sleep(10)
                # parent.click()
                
                #但是这里点击失败了，第二级不会展开。只能手动点击
                # parent_2 = browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/ul/li["+str(current_section_index)+"]/ul")
                # parent_2.click()
                
            section = parent.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div/ul/li["+str(current_section_index)+"]")
            has_next_jie = True
            current_jie_index = 2

            video_parent = section.find_element_by_tag_name("ul")
        except Exception as e:
            print("一层报错："+str(e))
            break
        while(has_next_jie):
            has_next_video = True
            current_video_index = 2
            #//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/ul/li[5]/ul/li[2]/p/a
            try:
                jie = parent.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div/ul/li["+str(current_section_index)+"]/ul/li["+str(current_jie_index)+"]/p/a")               
                jie_name = jie.get_attribute("title")
                if(jie_name.find("内容略") >= 0):
                    #换下一节
                    current_jie_index += 1
                    continue
            except Exception:
                print("")
            while(has_next_video):
                try:
                    hint_ke = "获取第"+str(current_section_index)+"章，第"+str(current_jie_index-1)+"节，第"+str(current_video_index-1)+"课"
                    print(hint_ke)
                    if hintCallback:
                        hintCallback(hint_ke)
                    video = video_parent.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div/ul/li["+str(current_section_index)+"]/ul/li["+str(current_jie_index)+"]/ul/li["+str(current_video_index)+"]/p/a[1]")
                    video_name = "{0}.{1}.{2}-{3}".format(current_section_index,current_jie_index-1,current_video_index-1,video.get_attribute("title"))
                    video_name = video_name.replace("\n", "")
                    video_name = video_name.replace("\r", "")
                    video_name = video_name.replace(" ", "")
                    video_name = video_name.replace(":", "：")
                    video_name = video_name.replace("?", "？")
                    video_name = video_name.replace("/", "、")
                    video_name = video_name.replace("\\", "、")
                    video_name = video_name.replace("<", "《")
                    video_name = video_name.replace(">", "》")
                    video_name = video_name.replace("*", "&")
                    video_name = video_name.replace("\"", "“")
                    video_name = video_name.replace("|", " ")
                    
                    fetch(proxy, video,video_name)                         #//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/ul/li[1]/ul/li[2]/ul/li[2]/p/a[1]
                                                                #//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/ul/li[2]/ul/li[2]/ul/li[3]/p/a[1]
                                                                #//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/ul/li[1]/ul/li[2]/ul/li[2]/p/a[1]
                                                                #//*[@id="app"]/div/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/div[1]/div/ul/li[1]/ul/li[3]/ul/li[2]/p/a[1]
                    current_video_index += 1
                    total += 1
                    # break
                except Exception as e:
                    print("二层报错："+str(e))

                    #没有下一节，换章
                    if(current_video_index == 2):
                        has_next_jie = False
                        current_section_index += 1
                    else:
                        #换下一节
                        current_jie_index += 1                    
                    has_next_video = False                    
                    # total -= 1
        # break
    hint_finish = "下载完成，视频数量："+str(total)
    print(hint_finish)
    if hintCallback:
        hintCallback(hint_finish)
    time.sleep(5)
    server.stop()
    browser.quit()

def cancel():
    if server:
        server.close()
    if browser:
        browser.quit()
        
def fetch(proxy,element,video_name):
    element.click()
    time.sleep(2)
    result = proxy.har
    # print(result)
    vid = ""
    playsafe = ""
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        vid_find = _url.find("vid=")
        playsafe_find = _url.find("token=")
        if(vid_find >= 0):
            vid = _url[vid_find+4:vid_find+38]
            # print("url",_url)
            # print("vid",vid)
        if(playsafe_find >= 0):
            playsafe = _url[playsafe_find+6:]
            # print("playsafe",playsafe)
    if((len(vid)>0) & (len(playsafe)>0)):
        polyv_m3u8.get_key(vid,playsafe,video_name)
    else:
        print("获取失败，正在重新获取...")
        fetch(proxy,element)


def get_key(m3u8_content):
    target = "Base64:"
    if m3u8_content.find(target) >= 0:
        return m3u8_content[len(target):len(target)+24]
    else:
        return ""
    


def download(url):
    download_path = os.getcwd() + "\download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    
    all_content = ""
    if url.startswith("http"):    
        all_content = requests.get(url).text # 获取M3U8的文件内容
    else:
        f = open(url,"r")
        all_content = f.read()
    file_line = all_content.split("\n") # 读取文件里的每一行
    # 通过判断文件头来确定是否是M3U8文件
    if file_line[0] != "#EXTM3U":
        raise BaseException(u"非M3U8的链接")
    else:
        unknow = True   # 用来判断是否找到了下载的地址
        key = get_key(all_content)
        iv = ""
        print("key：", key)
        for index, line in enumerate(file_line):
            if "#EXT-X-KEY" in line:  # 找解密Key
                
                
                iv_pos = line.find("IV")
                iv = line[iv_pos+3:]
                
                print ("IV",iv)

            if "EXTINF" in line:
                unknow = False
                # 拼出ts片段的URL
                pd_url = file_line[index + 1]
                res = requests.get(pd_url)
                # c_fule_name = str(index)+ '.ts'
                c_fule_name = "%(index)02d" % {'index': index} + '.ts'
                
                with open(download_path + "\\" + c_fule_name, 'ab') as f:
                    
                    cryptor = AES.new("9c861f057dcbe368".encode("utf-8"), AES.MODE_CBC, "a2a173a99896112c".encode("utf-8"))
                    f.write(cryptor.decrypt(res.content))
                    f.flush()
                    
        if unknow:
            raise BaseException("未找到对应的下载链接")
        else:
            print("下载完成")

def merge_file(path):
    os.chdir(path)
    os.system("copy /b * new.mp4")

def hash_md5(_str) :
    _hash = hashlib.md5()
    _hash.update(_str.encode('utf-8'))
    return _hash.hexdigest()

#「00018」计算机应用基础 「02324」离散数学 「31-00197」旅游资源规划与开发 「31-00198」旅游企业投资与管理 「31-00199」中外民俗 
#「51-01850」建筑施工技术
# start("17820020047","Zk123456","51-01850",url= "http://yzkjh.beegoedu.com/",zhang=1)


# path = "E:\wangtao\PythonWorkSpace\MySpiders\m3u8File\[34-04579]中学语文教学法\\"
# download(path + "1.1.1-语言与文化：“背景”与“领域”.m3u8")
# print("2.3.1- 认知心理学与语文课程".replace(" ", ""))
