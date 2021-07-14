# -*- coding: utf-8 -*-
'爬取 https://www.tmooc.cn/ 上的网课'

import os
import time
import requests

#自动化测试库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#代理抓包库
from browsermobproxy import Server

def get_m3u8_file():
    server = Server(r'D:\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
    server.start()
    proxy = server.create_proxy()
    
    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    proxy.new_har(options={'captureHeaders': True, 'captureContent': True})
    
    
    browser = webdriver.Chrome(chrome_options=chrome_options)
    
    browser.get("https://www.tmooc.cn/")
    
    login_1 = browser.find_element_by_xpath("//*[@id=\"login_xxw\"]")
    login_1.click()
    time.sleep(2)
    
    username = browser.find_element_by_xpath("//*[@id=\"js_account_pm\"]")
    username.send_keys("653253826@qq.com")
    password = browser.find_element_by_xpath("//*[@id=\"js_password\"]")
    password.send_keys("64509852")
    
    login_2 = browser.find_element_by_xpath("//*[@id=\"js_submit_login\"]")
    login_2.click()
    time.sleep(2)
    
    browser.get("https://uc.tmooc.cn/userCenter/toUserSingUpCoursePage")
    time.sleep(2)
    
    to_learn = browser.find_element_by_xpath("//*[@id=\"tts_class\"]/div[2]/div/p[1]/a")
    to_learn.click()
    
    menuId = 698615
    # 729586
    has_next_zhang = True
    zhang_index = 0
    total = 0
    while(has_next_zhang):
        try:
            url = "https://tts.tmooc.cn/video/showVideo?menuId=" + str(menuId) + "&version=UIDVN201909"
            print(url)
            browser.get(url)
            time.sleep(2)
        except Exception as e:
            print("一层报错："+str(e))
            has_next_zhang = False
            break
        
        has_next_video = True
        video_index = 1
        while(has_next_video):
            try:
                print("获取第"+str(zhang_index)+"章，第"+str(video_index)+"课")
                                                      #/html/body/div[2]/div/div[3]/div[2]/div/div/div[1]/div[2]/div/p[1]/a
                                                     # /html/body/div[2]/div/div[3]/div[2]/div/div/div[1]/div[2]/div/p[1]/a'
                video = browser.find_element_by_xpath("/html/body/div[2]/div/div[3]/div[2]/div/div/div[1]/div[2]/div/p["+str(video_index)+"]/a")
                video.click();
                time.sleep(2)
                fetch(proxy, video,"第"+str(zhang_index)+"章"+video.get_attribute("title"))
                video_index += 1
                total += 1
            except Exception as e:
                print("二层报错："+str(e))
                has_next_vedio = False
                zhang_index += 1
                menuId -= 1
                video_index = 1
                break
        
    
    print("下载完成，视频数量："+str(total))
    time.sleep(5)
    server.stop()
    browser.quit()

def fetch(proxy,element,video_name):
    # element.click()
    # time.sleep(2)
    result = proxy.har

    m3u8content = ""
    baseUrl = "";
    replace_str = ""
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        if _url.find("m3u8?") >= 0:
            # print(_url)
            #取最后
            m3u8content = requests.get(_url).content.decode('utf-8')
            baseUrl = _url[0:_url.find("m3u8")]
            split_list = baseUrl.split("/")
            replace_str = str(split_list[len(split_list) - 1])

    print(baseUrl)
    # key_url = re.search(r'URI="([^"]+)"', m3u8content)
    # key_url = key_url.group().replace("URI=", "")
    # key_url = key_url.replace("\"", "")
    # key = requests.get(key_url).content.decode('utf-8')
    
    # m3u8content = re.sub(r'URI="([^"]+)"', 'URI="Base64:%s"' %(key), m3u8content, 1, re.M | re.I)
    m3u8content = m3u8content.replace(replace_str, baseUrl)
    
    with open(os.getcwd() + "\m3u8File\\" + video_name + ".m3u8", "wb") as f:
        f.write(m3u8content.encode('utf-8'))
    
    
get_m3u8_file()



