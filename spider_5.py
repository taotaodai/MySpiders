# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 15:37:53 2021

@author: Administrator
"""
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

    username.send_keys("17820020047")
    password = browser.find_element_by_xpath("/html/body/div[3]/div/div/div[2]/div[1]/div/div[2]/div[2]/div[2]/input")

    password.send_keys("Abcd123520")
    
    print("请在10秒内完成登录")
    time.sleep(10)

    browser.get("https://www.educity.cn/wangxiao/spjx10109777.html#a_14011510")
    
    time.sleep(3)
    jie_index = 1
    total = 0
    while(True):
        try:
            #/html/body/div[4]/div[1]/div[2]/div[3]/div/ul/a[1]/li
            #/html/body/div[4]/div[1]/div[2]/div[3]/div/ul/a[2]/li/span[1]
            #/html/body/div[4]/div[1]/div[2]/div[3]/div/ul/a[3]/li/span[1]
            jie_parent = browser.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/div[3]/div/ul/a["+str(jie_index)+"]/li")
            jie = browser.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/div[3]/div/ul/a["+str(jie_index)+"]/li/span[1]")
            c = jie_parent.get_attribute("class")
            zhang = int(c.replace("collapseTr", "")[0:1]) + 1
            video_name = "第{0}章-{1}".format(str(zhang),jie.text)
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
            
            fetch(proxy, jie,video_name)
            time.sleep(2)
            jie_index += 1
            total += 1
        except Exception as e:
            print("一层报错："+str(e))
            break
    
            
                
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
            # print("url",_url)
            # print("vid",vid)
        if(playsafe_find >= 0):
            playsafe = _url[playsafe_find+6:]
            # print("playsafe",playsafe)
    if((len(vid)>0) & (len(playsafe)>0)):
        polyv_m3u8.get_key(vid,playsafe,video_name)
    else:
        print("获取失败，正在重新获取...")
        fetch(proxy,element,video_name)

get_vid_and_playsafe()
