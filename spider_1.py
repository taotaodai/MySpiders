# -*- coding:utf-8 -*-

'用于爬取http://uc.xinchengjy.cn/ 上的网课。'
'这个文件的功能主要是，获取vid和playsafe，再由polyv_m3u8解密，生成m3u8文件，用于下载视频片段。'
import os
import sys
import time
import requests
import datetime
from Cryptodome.Cipher import AES
import json

#自动化测试库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#代理抓包库
from browsermobproxy import Server
import polyv_m3u8
 
#这个地址需要手工抓包获得
m3u8_url = 'http://hls.videocc.net/b034527feb/3/b034527feb0c7d1f832df6cb628d9553_2.m3u8?pid=1604971237787X1350686&device=desktop'
 

def get_vid_and_playsafe():
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
    
    browser.get("http://uc.xinchengjy.cn/login")
    time.sleep(2)
    username = browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div[2]/form/div[1]/div/input")

    username.send_keys("13318275453")
    password = browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div[2]/form/div[2]/div/input")
    password.send_keys("Xm123456")
    
    #设置cookie自动登录，但是在这个网站无效
    # browser.add_cookie({
    #     'name': 'coksinfo',
    #     'value': 'eG0xMzUyNzIwMTIzMQ%3D%3D'
    # })
    
    print("请在10秒内完成登录")
    time.sleep(10)
    #y[03201]护理学导论 y[34-06230]小学艺术课程与教学 y[00809]市场营销（二）y[00796]商务英语
    #y[42-05151]劳动与社会保障 y[43-11530]护理礼仪与人际沟通 y[00464]中外教育简史 y[00458]中小学教育管理 y[03298]创新思维理论与方法
    #y[51-06088]管理思想史 y[03702]会计制度设计与比较 y[00445]中外教育管理史 y[02864]微生物学与免疫学基础
    #y[42-00806]财务报表分析(二) y[42-00207]高级财务管理 y[42-03364]供应链物流学 y[00469]教育学原理
    #y[00108]工商行政管理学概论 y[00264]中国法律思想史 y[06087]工程项目管理 y[11-00820]汉字学概论
    #y[42-07250]投资学原理 [00227]公司法 y[37-05066]项目论证与评估 y[37-05062]项目质量管理 y[42-06396]国际工程承包与管理
    #y[35-12339]幼儿园教育基础 y[12340]学前儿童发展 y[35-12344]学前教育政策与法规 y[35-30001]学前儿童保育学 y[42-00874]特殊儿童早期干预
    #y[05759]健康教育与健康促进 [34-05963]绩效管理 [34-06090]人员素质测评理论与方法 [33-00923]行政法与行政诉讼法（一）
    #y[42-07817]电子政务 y[11-81761]人力资源管理高级实验 [50-00071]社会保障概论 [43-06093]人力资源开发与管理
    #y[09235]设计原理 y[42-07138]工程造价与管理 y[42-04627]工程管理概论 y[42-06086]工程监理 y[42-06936]建筑法规
    #y[00884]学前教育行政与管理 y[00885]学前教育与诊断 y[42-08118]法律基础 y[00810]人力资源管理（二）
    #y[00803]财务管理 y[50-00098]国际市场营销学 y[03703]国际会计与审计准则 y[03293]现代谈判学 y[03294]公共关系案例
    #y[04531]微观经济学 y[00799]数量方法 [04533]管理与成本会计 [00944]审计 [06069]审计学原理
    #y[11465]现代公司管理 y[07484]社会保障学 y[11466]现代企业人力资源管理概论 y[11467]人力资源统计学 y[00463]现代人员测评
    #y[00324]人事管理学 y[11468]工作岗位研究原理与应用 y[00164]劳动经济学 y[06183]工资管理 y[11365]劳动力市场学
    #y[11366]人口与劳动资源 y[05355]商务英语翻译 y[00096]外刊经贸知识选读 y[00090]国际贸易实务（一）
    #y[05844]国际商务英语 y[05439]商务英语阅读 y[05440]商务英语写作 [00795]综合英语（二） y[07564]唐宋词研究
    #y[11342]民间文学概论 y[00814]中国古代文论选读 y[00821]现代汉语语法研究
    browser.get("http://uc.xinchengjy.cn/topic/course/study/00796")
    
    time.sleep(3)
    #章节                                      //*[@id="app"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div/ul
    parent = browser.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div/ul")
    has_next_section = True
    current_section_index = 4
    total = 0
    while(has_next_section):
        try:
            #第一章是默认展开的，之后的需要点击展开才能使内部的组件可被使用
            if(current_section_index > 1):
                print("点击第"+str(current_section_index)+"章")
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
            except Exception as e:
                print("")
            while(has_next_video):
                try:
                    print("获取第"+str(current_section_index)+"章，第"+str(current_jie_index-1)+"节，第"+str(current_video_index-1)+"课")
                    video = video_parent.find_element_by_xpath("//*[@id=\"app\"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div/ul/li["+str(current_section_index)+"]/ul/li["+str(current_jie_index)+"]/ul/li["+str(current_video_index)+"]/p/a[1]")
                    video_name = "{0}.{1}.{2}-{3}".format(current_section_index,current_jie_index-1,current_video_index-1,video.get_attribute("title"))
                    video_name = video_name.replace("\n", "")
                    video_name = video_name.replace(":", "：")
                    video_name = video_name.replace("?", "？")
                    video_name = video_name.replace("/", "、")
                    video_name = video_name.replace("\\", "、")
                    video_name = video_name.replace("<", "《")
                    video_name = video_name.replace(">", "》")
                    video_name = video_name.replace("*", "&")
                    
                    video_name = video_name
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
                
    print("下载完成，视频数量："+str(total))
    time.sleep(5)
    server.stop()
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
            print("vid",vid)
        if(playsafe_find >= 0):
            playsafe = _url[playsafe_find+6:]
            print("playsafe",playsafe)
    if((len(vid)>0) & (len(playsafe)>0)):
        polyv_m3u8.get_key(vid,playsafe,video_name)
    else:
        print("获取失败，正在重新获取...")
        fetch(proxy,element)


def get_key():
    # return requests.get("http://hls.videocc.net/playsafe/b034527feb/3/b034527feb0c7d1f832df6cb628d9553_2.key?token=b54e88f2-aba4-48c7-aabf-3faa06ab82b0-h126").content
    
    # fp = open("key.key",'rb')
    # content = fp.read().decode('ASCII','ignore')
    return "EDB2555CC399D42A3480292074FADE4EA22BBA105E37E95B589F579DC44AEBB4"
    


def download(url):
    download_path = os.getcwd() + "\download"
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    all_content = requests.get(url).text # 获取M3U8的文件内容
    file_line = all_content.split("\n") # 读取文件里的每一行
    # 通过判断文件头来确定是否是M3U8文件
    if file_line[0] != "#EXTM3U":
        raise BaseException(u"非M3U8的链接")
    else:
        unknow = True   # 用来判断是否找到了下载的地址
        key = get_key()
        iv = ""
        print("key：", key)
        for index, line in enumerate(file_line):
            if "#EXT-X-KEY" in line:  # 找解密Key
                
                uri_pos = line.find("URI")
                quotation_mark_pos = line.rfind('"')
                key_path = line[uri_pos:quotation_mark_pos].split('"')[1]
                
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
                    
                    cryptor = AES.new(key, AES.MODE_CBC, iv)
                    f.write(cryptor.decrypt(res.content))
                    f.flush()
                    return
        if unknow:
            raise BaseException("未找到对应的下载链接")
        else:
            print("下载完成")

def merge_file(path):
    os.chdir(path)
    os.system("copy /b * new.mp4")


get_vid_and_playsafe()