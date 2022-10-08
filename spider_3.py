# -*- coding:utf-8 -*-

'用于爬取https://www.zikao365.com/ 上的网课。'

import os
import time
import re
import requests

# 自动化测试库
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
# 代理抓包库
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

    browser.get("https://www.zikao365.com/")
    #                                                  /html/body/div[2]/div[1]/div/div[1]/ul[1]/li[3]
    #/html/body/div/div[4]/div[1]/div[1]/div[1]/div[2]/a[1]
    login_1 = browser.find_element(by=By.XPATH, value="/html/body/div/div[4]/div[1]/div[1]/div[1]/div[2]/a[1]")
    login_1.click()
    time.sleep(2)

    browser.switch_to.frame("frameTencent")

    login_2 = browser.find_element(by=By.XPATH, value="/html/body/div[1]/div/div[1]/ul/li[3]")
    login_2.click()
    time.sleep(1)

    #abcd123520
    username = browser.find_element(by=By.XPATH, value="//*[@id=\"username\"]")
    username.send_keys("13450494254")
    password = browser.find_element(by=By.XPATH, value="//*[@id=\"password\"]")
    password.send_keys("Zk123456")

    login_3 = browser.find_element(by=By.XPATH, value="//*[@id=\"submit_log_btn\"]")
    login_3.click()
    time.sleep(5)

    #配置1.是否为前言。
    is_introduction = False

    url = "http://elearning.zikao365.com/xcware/video/h5video/videoPlay.shtm?cwareID=513993&videoID="
    browser.get(url + ("1" if is_introduction else "101"))

    # 章节                                      //*[@id="app"]/div/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div/div/div[1]/div/ul
    # parent = browser.find_element_by_xpath("//*[@id=\"catalog\"]/div[2]/div/div[1]")
    has_next_section = True
    current_section_index = 1

    total = 0
    while has_next_section:
        #配置2。videoID。

        try:
            browser.get(url + str(current_section_index) + ("" if is_introduction else "01"))
            time.sleep(2)
            print("点击第" + str(current_section_index) + "章")
            # //*[@id="catalog"]/div[2]/div/div[1]/a[1]
            # //*[@id="catalog"]/div[2]/div/div[1]/a[1]
            # //*[@id="catalog"]/div[2]/div/div[1]/a[2]
            section = browser.find_element(by=By.XPATH,
                                           value="//*[@id=\"catalog\"]/div[2]/div/div[1]/a[" + str(
                                               current_section_index) + "]")
            section.click()
            time.sleep(1)
            has_next_jie = True
            current_jie_index = 1

        except Exception as e:
            print("一层报错：" + str(e))
            break
        while has_next_jie:
            # //*[@id="101"]/span[2]
            # //*[@id="301"]/span[2]
            # //*[@id="801"]/span[2]
            video_index = "00"

            if current_jie_index >= 10:
                video_index = str(current_jie_index)
            else:
                video_index = "0"+str(current_jie_index)
            if is_introduction:
                video_index = ""
            browser.get(url + str(current_section_index) + video_index)
            time.sleep(2)
            try:
                jie = browser.find_element(by=By.XPATH, value="//*[@id=\"" + str(current_section_index) + video_index + "\"]/span[2]")
                jie_name = jie.get_attribute("title")

                print("获取第" + str(current_section_index) + "章，第" + str(current_jie_index) + "讲")
                fetch(proxy, jie, "第" + str(current_section_index) + "章" + jie_name)
                current_jie_index += 1
                total += 1

            except Exception as e:
                print("二层报错：" + str(e))
                has_next_jie = False
                current_section_index += 1

    print("下载完成，视频数量：" + str(total))
    time.sleep(5)
    server.stop()
    browser.quit()


def fetch(proxy, element, video_name):
    # element.click()
    # time.sleep(2)
    result = proxy.har

    m3u8content = ""
    for entry in result['log']['entries']:
        _url = entry['request']['url']
        if _url.find("m3u8") >= 0:
            # print(_url)
            # 取最后
            m3u8content = requests.get(_url).content.decode('utf-8')
            # print(m3u8content)
            # break

    key_url = re.search(r'URI="([^"]+)"', m3u8content)
    key_url = key_url.group().replace("URI=", "")
    key_url = key_url.replace("\"", "")
    key = requests.get(key_url).content.decode('utf-8')

    m3u8content = re.sub(r'URI="([^"]+)"', 'URI="Base64:%s"' % (key), m3u8content, 1, re.M | re.I)
    m3u8content = m3u8content.replace("/ssec", "https://ssec")

    with open(os.getcwd() + "\m3u8File\\" + video_name + ".m3u8", "wb") as f:
        f.write(m3u8content.encode('utf-8'))


get_m3u8_file()

# m3u8content = "#EXTM3U\n#EXT-X-TARGETDURATION:15\n#EXT-X-ALLOW-CACHE:YES\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXT-X-KEY:METHOD=AES-128,URI=\"https://elearning.cdeledu.com/hls/service/getKeyForHls?cwareID=513759&videoID=101&userID=82122702&time=1619077384672&code=16dd183536a386a37645f01917e398b5&host=inner.zikao365.com&sid=&th=pc&path=K1jILY5n6QYbAlMZ97NAw4fA.z0geCIGy3qaLRzTUlgFTZ-Ak2cXMlg0MLEHjzv9tTnOvamtPb.d.DpJXy.NeQ__.mp4&h1=1619077388376&token=f42bdf5c2fd11d7c15be0e985b073e42\"\n#EXT-X-VERSION:3\n#EXT-X-MEDIA-SEQUENCE:1\n#EXTINF:15.000,\n/ssec.chinaacc.com/K1jILY5n6QYbAlMZ97NAw4fA.z0geCIGy3qaLRzTUlgFTZ-Ak2cXMlg0MLEHjzv9tTnOvamtPb.d.DpJXy.NeQ__.mp4/seg-1-v1-a1.ts?cwareID=513759&videoID=101&userID=82122702&time=1619077384672&code=16dd183536a386a37645f01917e398b5&host=inner.zikao365.com&sid=&th=pc\n#EXTINF:15.000,\n/ssec.chinaacc.com/K1jILY5n6QYbAlMZ97NAw4fA.z0geCIGy3qaLRzTUlgFTZ-Ak2cXMlg0MLEHjzv9tTnOvamtPb.d.DpJXy.NeQ__.mp4/seg-2-v1-a1.ts?cwareID=513759&videoID=101&userID=82122702&time=1619077384672&code=16dd183536a386a37645f01917e398b5&host=inner.zikao365.com&sid=&th=pc\n#EXTINF:15.000,\n/ssec.chinaacc.com/K1jILY5n6QYbAlMZ97NAw4fA.z0geCIGy3qaLRzTUlgFTZ-Ak2cXMlg0MLEHjzv9tTnOvamtPb.d.DpJXy.NeQ__.mp4/seg-3-v1-a1.ts?cwareID=513759&videoID=101&userID=82122702&time=1619077384672&code=16dd183536a386a37645f01917e398b5&host=inner.zikao365.com&sid=&th=pc\n#EXTINF:15.000,\n/ssec.chinaacc.com/K1jILY5n6QYbAlMZ97NAw4fA.z0geCIGy3qaLRzTUlgFTZ-Ak2cXMlg0MLEHjzv9tTnOvamtPb.d.DpJXy.NeQ__.mp4/seg-4-v1-a1.ts?cwareID=513759&videoID=101&userID=82122702&time=1619077384672&code=16dd183536a386a37645f01917e398b5&host=inner.zikao365.com&sid=&th=pc\n"
# m3u8content = m3u8content.replace("/ssec", "https://ssec")
# # print(m3u8content)

# # m3u8content = re.sub(r'URI="([^"]+)"', 'URI="Base64:%s"' %(""), m3u8content, 1, re.M | re.I)
# key_url = re.search(r'URI="([^"]+)"', m3u8content)
# # print(m3u8content)
# key_url = key_url.group().replace("URI=", "")
# key_url = key_url.replace("\"", "")

# print(key_url)
