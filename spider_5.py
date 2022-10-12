# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 15:37:53 2021

@author: Administrator
"""

import time

# 自动化测试库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# 代理抓包库
from browsermobproxy import Server
import polyv_m3u8

# 希赛网
BASE_URL = "https://www.educity.cn/"


def get_vid_and_playsafe():
    server = Server(r'D:\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
    server.start()
    proxy = server.create_proxy()

    chrome_options = Options()
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
    proxy.new_har(options={'captureHeaders': True, 'captureContent': True})

    browser = webdriver.Chrome(chrome_options=chrome_options)

    login_url = BASE_URL + "login.html"
    browser.get(login_url)
    time.sleep(2)
    login_switch = browser.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div[1]/div/div[1]/ul/li[2]")
    login_switch.click()
    time.sleep(1)
    username = browser.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[1]/input")

    username.send_keys("15527938793")
    password = browser.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/input")

    password.send_keys("Ws123456z")

    print("请在10秒内完成登录")
    time.sleep(10)

    browser.get("https://wangxiao.xisaiwang.com/wangxiao2/c20417540/sp20188879.html")

    time.sleep(3)
    zhang_index = 1

    total = 0
    while True:
        try:
            # //*[@id="vidtree"]/div[1]/a/span    //*[@id="vidtree"]/div[4]/a/span
            # //*[@id="vidtree"]/div[8]/div[1]/div/a/span[1]
            zhang = browser.find_element_by_xpath("//*[@id=\"vidtree\"]/div[" + str(zhang_index) + "]/a/span")
            if zhang_index > 1:
                zhang.click()
            time.sleep(2)
            jie_index = 1
            while True:
                try:
                    jie = browser.find_element_by_xpath(
                        "//*[@id=\"vidtree\"]/div[" + str(zhang_index) + "]/div[" + str(jie_index) + "]/div/a/span[1]")
                    video_name = jie.text
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

                    print("正在下载第{0}章第{1}节".format(str(zhang_index), str(jie_index)))
                    print(video_name)
                    jie.click()
                    fetch(proxy, jie, video_name)
                    time.sleep(2)
                    jie_index += 1
                    total += 1
                except Exception as e:
                    print("一层报错：" + str(e))
                    break

            time.sleep(2)
            zhang_index += 1
        except Exception as e:
            print("一层报错：" + str(e))
            break

    print("下载完成，视频数量：" + str(total))
    time.sleep(5)
    server.stop()
    browser.quit()


def fetch(proxy, element, video_name):
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
        if vid_find >= 0:
            vid = _url[vid_find + 4:vid_find + 38]
            # print("url",_url)
            # print("vid",vid)
        if playsafe_find >= 0:
            playsafe = _url[playsafe_find + 6:]
            # print("playsafe",playsafe)
    if (len(vid) > 0) & (len(playsafe) > 0):
        polyv_m3u8.get_key(vid, playsafe, video_name)
    else:
        print("获取失败，正在重新获取...")
        fetch(proxy, element, video_name)


get_vid_and_playsafe()
