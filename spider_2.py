# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 16:07:47 2020

@author: Administrator
"""
import os, sys
import json
import time
import requests
import datetime
import urllib.parse
import cv2
import numpy as np
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont

url_get_token = 'https://video.sunlands.com/video/thirdLogin'
url_get_ppt = 'https://video.sunlands.com/video/getincrmsg'

url_room = 'http://player.sunlands.com/room/#/vod?partnerId=1&roomId=81047&ts=1607159931&userAvatar=https%3A%2F%2Fsfs-public.shangdejigou.cn%2Fuser_center%2FnewUserImagePath%2F3868830%2F3868830_51934214.jpg&userId=3868830&userName=%E9%92%9F%E9%BB%8E&userRole=1&sign=fab1c1900d59f32e9984d545d3d96567&teachUnitId=5185274&encryptStr=ZS_d_c6SMcpkYW0yhWu7Xg__'
def getParamDict(url):
    url = urllib.parse.unquote(url)
    paramList = url.strip().split('?')[1].split('&')
    paramDict = {}
    for item in paramList:
        paramDict[item.split('=')[0]] = item.split('=')[1]
    
    return paramDict
#15157583442      aA1179237370    
#账号：18222409930       密码：zlzlzlzl121522
def get_token():
    param_dict = getParamDict(url_room)
    payloadData = {
        'partnerId': 1,
        'roomId':int(param_dict.get('roomId')),
        'userId':param_dict.get('userId'),
        'userName':param_dict.get('userName'),
        'userRole':1,
        'ts':int(param_dict.get('ts')),
        'userAvatar':param_dict.get('userAvatar'),
        'sign':param_dict.get('sign'),
        'terminalType':3
    }
    
    # print(payloadData)
    # 请求头设置
    payloadHeader = {
    'Host': 'video.sunlands.com',
    'Content-Type': 'application/json',
    }

    # # 下载超时
    # timeOut = 25
    # # 代理
    # proxy = "183.12.50.118:8080"
    # proxies = {
    #     "http": proxy,
    #     "https": proxy,
    # }
    res = requests.get(url_get_token, data=json.dumps(payloadData), headers=payloadHeader)
    
   # {
   #    "roomInfo": {
   #      "sName": "【英语翻译】英语本<精讲9>",
   #      "sTeacher": "王杜",
   #      "lBeginTime": 1605353400,
   #      "lEndTime": 1605360600,
   #      "iUserCount": 5,
   #      "page": {
   #        "iPageId": 0,
   #        "iType": 2,
   #        "iColor": 4280455559,
   #        "iWidth": 1024,
   #        "iHeight": 576,
   #        "lSequence": 0,
   #        "iCoursewareId": 10000,
   #        "iTabulaWidth": 0,
   #        "iTabulaHeight": 0,
   #        "iScrollPosition": 0
   #      },
   #      "iRoomId": 115200,
   #      "iImId": 115200
   #    },
   #    "sUserName": "张贯球",
   #    "videoPlayUrls": [
   #      {
   #        "sUrl": "http://1257236654.vod2.myqcloud.com/cc26eeabvodcq1257236654/1cc8a0de5285890809597395166/f0.mp4?t=5fcb4498&us=57202985&sign=d1a93d066615b7e39d1aa597afe32f71",
   #        "eCdnType": 1,
   #        "lSequence": 0,
   #        "sFormat": "mp4",
   #        "iDuration": 9888.8,
   #        "bIsConcat": false,
   #        "sFileName": "5285890809597395166",
   #        "sequenceInfos": [
   #          {
   #            "iStart": 0,
   #            "iDuration": 7201.485,
   #            "lSequence": 1605352474054
   #          },
   #          {
   #            "iStart": 7201.485,
   #            "iDuration": 2687.152,
   #            "lSequence": 1605359675996
   #          }
   #        ],
   #        "sharedPlaybackUrlInfos": [],
   #        "lFileSize": 340613254,
   #        "eMediaType": 1,
   #        "dTotalDuration": 9888.8,
   #        "sHlsUrl": "http://1257236654.vod2.myqcloud.com/a310dc53vodtranscq1257236654/1cc8a0de5285890809597395166/playlist.f6.m3u8?t=5fcb4498&us=f823eb6b&sign=80dc910139378fcc226949bbb16de4a9",
   #        "sHttpsUrl": "https://1257236654.vod2.myqcloud.com/cc26eeabvodcq1257236654/1cc8a0de5285890809597395166/f0.mp4?t=5fcb4498&us=57202985&sign=d1a93d066615b7e39d1aa597afe32f71",
   #        "sHttpsHlsUrl": "https://1257236654.vod2.myqcloud.com/a310dc53vodtranscq1257236654/1cc8a0de5285890809597395166/playlist.f6.m3u8?t=5fcb4498&us=f823eb6b&sign=80dc910139378fcc226949bbb16de4a9"
   #      }
   #    ],
   #    "iUserId": 222356,
   #    "token": "12fa0a4b2d402bb441e641444d6a13c0",
   #    "ended": false,
   #    "promotes": []
   #  }
    print(res.text)
    return res.json()

#获取PPT信息，这里会有三种情况：
# 1.PPT有更新时
# {
#   "sequenceMap": {
#     "1605353245450": [
#       {
#         "eType": 10008,
#         "bytes": "{\"iPageId\":10,\"sUrl\":\"//sfs-private.shangdejigou.cn/SunliveDocument/20201114/115200_159792_10_543974540ddc8f4922bbb93b480d0eae.jpg?sign=8e9f4f687be22478921f048e6e3e5200&t=1607267894\",\"iType\":1,\"iWidth\":1200,\"iHeight\":675,\"lSequence\":1605353245450,\"iCoursewareId\":159792,\"iTabulaWidth\":16,\"iTabulaHeight\":9,\"iScrollPosition\":50}"
#       }
#     ]
#   }
# }    
# 2.涂鸦有更新时
# {
#     "sequenceMap": {
#         "1605355372428": [
#             {
#                 "eType": 10006,
#                 "bytes": "{\"version\":1,\"iType\":5,\"iCoursewareId\":159703,\"iPageId\":80,\"iId\":72,\"lSequence\":1605355372428,\"points\":[{\"x\":1834,\"y\":3330},{\"x\":4147,\"y\":3376}],\"penWidth\":6,\"iColor\":4294901760}"
#             }
#         ]
#     }
# }
# 3.都没有更新时
# {}
#获取PPT包的时间大小（秒）
P_Interval = 120
def get_ppt(lSequence,token,roomId):
    payloadData = {
        'lSequence': lSequence,
        'iInterval':P_Interval,
        'token':{
            'roomId':roomId,
            'token':token
            }
    }
    # 请求头设置
    payloadHeader = {
    'Host': 'video.sunlands.com',
    'Content-Type': 'application/json',
    }
    
    res = requests.get(url_get_ppt, data=json.dumps(payloadData), headers=payloadHeader)
    print(res.text)
    return res.json()

def download_img(img_url, img_name):
    # print (img_url)
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        open(os.getcwd() + '\download\\'+ img_name + '.png', 'wb').write(r.content) # 将内容写入图片
        print("done")

def download_audio(url):
    print('开始下载音频...')
    r = requests.get(url, stream=True)
    print(r.status_code)
    if r.status_code == 200:
        open(os.getcwd() + '\output\\'+  'audio.mp4', 'wb').write(r.content) # 将内容写入图片
        print("done")
        
#图片转视频
'每秒帧数'
FPS = 5
PFS_ADD = 1000/FPS
def convert_to_video():
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')        # 设置输出视频为mp4格式

    size = (video_width, video_height)
    video = cv2.VideoWriter('output/result.mp4',fourcc, FPS, size)

    images = os.listdir('download')
    # print(images)
    time_stamp_count = int(images[0].split('.')[0])
    current_img = 'download/'+images[0]
    for i, img in enumerate(images[1:]):
        timestamp = int(img.split('.')[0])

        old_img = True
        img_E = cv2.imread(current_img)
        img_E = cv2.resize(img_E,dsize=(video_width,video_height),fx=1,fy=1,interpolation=cv2.INTER_LINEAR)
        print(current_img)
        while(old_img):
            video.write(img_E)
            time_stamp_count += PFS_ADD
            # print(str(time_stamp_count)+'~~~'+str(timestamp))
            # print(current_img)
            if(time_stamp_count >= timestamp):
                old_img = False
                
                current_img = 'download/'+img
    video.release()

#从直播视频中提取音频，合并到PPT视频中
def combin_audio_to_video():
    # 读取2个视频文件 
    videoclip_1 = VideoFileClip("output/audio.mp4")
    videoclip_2 = VideoFileClip("output/result.mp4")
    
    # 提取第一个视频文件的音频部分
    audio_1 = videoclip_1.audio
    
    # 将提取的音频和第二个视频文件进行合成
    videoclip_3 = videoclip_2.set_audio(audio_1)
    
    # 输出新的视频文件
    videoclip_3.write_videofile("output/c.mp4")

def draw(obj,image,key_draw):
    # image = cv2.imread('download/'+ key_img +'.png')
    # image = cv2.resize(image,dsize=(video_width,video_height),fx=1,fy=1,interpolation=cv2.INTER_LINEAR)
    
    iType = obj.get('iType')
    
    #点连线
    if iType == 1:
        #画线
        # pts = np.array([[1200*0.8087,675*0.4387],[1200*0.81,675*0.4387],[1200*0.81,675*0.4341],[1200*0.8113,675*0.4341],
        #                 [1200*0.8139,675*0.4318],[1200*0.8139,675*0.4295],[1200*0.8152,675*0.4272],[1200*0.8152,675*0.4249],
        #                 [1200*0.8165,675*0.4226],[1200*0.8191,675*0.4226],[1200*0.8204,675*0.4180],[1200*0.8217,675*0.4180],
        #                 [1200*0.8268,675*0.4088],[1200*0.8281,675*0.4042],[1200*0.8307,675*0.4019],[1200*0.8333,675*0.4019],
        #                 [1200*0.8410,675*0.3858],[1200*0.8423,675*0.3858],[1200*0.8436,675*0.3812],[1200*0.8462,675*0.3789],
        #                 [1200*0.8462,675*0.3766],[1200*0.8540,675*0.3674],[1200*0.8604,675*0.3583],[1200*0.8643,675*0.3537],
        #                 [1200*0.8643,675*0.3514],[1200*0.8656,675*0.3491],[1200*0.8695,675*0.3445],[1200*0.8695,675*0.3422],
        #                 [1200*0.8720,675*0.3422],[1200*0.8720,675*0.3399],[1200*0.8720,675*0.3376]], np.int32)
        
        # pts2 = np.array([[1200*0.7971,675*0.4042],[1200*0.7997,675*0.4111],[1200*0.7997,675*0.418],[1200*0.801,675*0.4203]
        #                 ,[1200*0.8023,675*0.4203],[1200*0.8036,675*0.4226],[1200*0.8036,675*0.4249],[1200*0.8062,675*0.4318]
        #                 ,[1200*0.8062,675*0.4341],[1200*0.8074,675*0.4341],[1200*0.8087,675*0.4364]], np.int32)
        
        # pts3 = np.array([[1200*0.8087,675*0.4364],[1200*0.8087,675*0.4387]], np.int32)
        # cv2.polylines(image,[pts],True,(0,0,255),6)
        # cv2.polylines(image,[pts2],True,(0,0,255),6)
        # cv2.polylines(image,[pts3],True,(0,0,255),6)
        
        #画点
        # points_list = [(int(1200*0.7971),int(675*0.4042)),(int(1200*0.7997),int(675*0.4111)),(int(1200*0.7997),int(675*0.418)),(int(1200*0.801),int(675*0.4203))
        #                 ,(int(1200*0.8023),int(675*0.4203)),(int(1200*0.8036),int(675*0.4226)),(int(1200*0.8036),int(675*0.4249)),(int(1200*0.8062),int(675*0.4318))
        #                 ,(int(1200*0.8062),int(675*0.4341)),(int(1200*0.8074),int(675*0.4341)),(int(1200*0.8087),int(675*0.4364))
        #     ,(int(1200*0.8087),int(675*0.4364)),(int(1200*0.8087),int(675*0.4387))
        #     ,(int(1200*0.8087),int(675*0.4387)),(int(1200*0.81),int(675*0.4387)),(int(1200*0.81),int(675*0.4341)),(int(1200*0.8113),int(675*0.4341))
        #                 ,(int(1200*0.8139),int(675*0.4318)),(int(1200*0.8139),int(675*0.4295)),(int(1200*0.8152),int(675*0.4272)),(int(1200*0.8152),int(675*0.4249))
        #                 ,(int(1200*0.8165),int(675*0.4226)),(int(1200*0.8191),int(675*0.4226)),(int(1200*0.8204),int(675*0.4180)),(int(1200*0.8217),int(675*0.4180))
        #                 ,(int(1200*0.8268),int(675*0.4088)),(int(1200*0.8281),int(675*0.4042)),(int(1200*0.8307),int(675*0.4019)),(int(1200*0.8333),int(675*0.4019))
        #                 ,(int(1200*0.8410),int(675*0.3858)),(int(1200*0.8423),int(675*0.3858)),(int(1200*0.8436),int(675*0.3812)),(int(1200*0.8462),int(675*0.3789))
        #                 ,(int(1200*0.8462),int(675*0.3766)),(int(1200*0.8540),int(675*0.3674)),(int(1200*0.8604),int(675*0.3583)),(int(1200*0.8643),int(675*0.3537))
        #                 ,(int(1200*0.8643),int(675*0.3514)),(int(1200*0.8656),int(675*0.3491)),(int(1200*0.8695),int(675*0.3445)),(int(1200*0.8695),int(675*0.3422))
        #                 ,(int(1200*0.8720),int(675*0.3422)),(int(1200*0.8720),int(675*0.3399)),(int(1200*0.8720),int(675*0.3376))
        #                 ]
    
        # point_color = (0, 0, 255) # BGR
        # thickness = 8 # 可以为 0 、4、8
        # point_size = 2
        
        # for point in points_list:
        #     cv2.circle(image, point, point_size, point_color, thickness)
        points = obj.get('points')
        pts = []
        for p in points:
            sp = [video_width*p.get('x')/10000,video_height*p.get('y')/10000]
            pts.append(sp)
        
        pts = np.array(pts,np.int32)
        cv2.polylines(image,[pts],False,hex2bgr(obj.get('iColor')),obj.get('penWidth'))
        cv2.imwrite('download/'+ key_draw +'.png', image)
        
    #矩形
    elif iType == 5:
        points = obj.get('points')
        p1 = points[0]
        p2 = points[1]
        cv2.rectangle(image, (int(video_width*p1.get('x')/10000),int(video_height*p1.get('y')/10000)), (int(video_width*p2.get('x')/10000),int(video_height*p2.get('y')/10000)), hex2bgr(obj.get('iColor')), obj.get('penWidth'),cv2.LINE_4)
        cv2.imwrite('download/'+ key_draw +'.png', image)
    elif iType == 7:
        points = obj.get('points')
        # font = cv2.FONT_HERSHEY_SIMPLEX
        p1 = points[0]
        #为了解决中文乱码问题，这里用PIL库转换一下
        image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image)
        # 字体的格式
        fontStyle = ImageFont.truetype("font/simsun.ttc", obj.get('fontSize'), encoding="gbk")
        draw.text((int(video_width*p1.get('x')/10000),int(video_height*p1.get('y')/10000)),obj.get('sText'), hex2bgr(obj.get('iColor')), font=fontStyle)
        # cv2.putText(image,obj.get('sText'),(int(video_width*p1.get('x')/10000),int(video_height*p1.get('y')/10000)), font, 1,hex2bgr(obj.get('iColor')),2,cv2.LINE_AA)
        image = np.array(image)
        cv2.imwrite('download/'+ key_draw +'.png', image)
        # print('文字涂鸦：'+bytes_info.get('sText'))

def hex2bgr(hexcolor):
  bgr = (hexcolor & 0xff,
      (hexcolor >> 8) & 0xff,
      (hexcolor >> 16) & 0xff
     )
  return bgr

token_obj = get_token()
#老师直播视频文件地址
audio_url = token_obj.get('videoPlayUrls')[0].get('sUrl')
#开播时间
start_time = token_obj.get('videoPlayUrls')[0].get('sequenceInfos')[0].get('lSequence')
#直播时长
duration = int(token_obj.get('videoPlayUrls')[0].get('iDuration')) * 1000
#结束时间
end_time = start_time + duration
video_width = token_obj.get('roomInfo').get('page').get('iWidth')
video_height = token_obj.get('roomInfo').get('page').get('iHeight')

# #下载PPT
# ppt_obj = get_ppt(token_obj.get('videoPlayUrls')[0].get('sequenceInfos')[0].get('lSequence'),token_obj.get('token'),token_obj.get('roomInfo').get('iRoomId'))
# last_img_sequence = 0
# last_img = ''
# while('sequenceMap' in ppt_obj):    
#     ppt_obj = ppt_obj.get('sequenceMap')
    
#     index = 0
#     last_sequence = 0
    
#     for key in ppt_obj:
#         index += 1
#         # print(key)
#         bytes_info = ppt_obj.get(key)[0].get('bytes')
#         bytes_info = bytes_info.replace('\\','')
#         bytes_info = json.loads(bytes_info)
#         if 'sUrl' in bytes_info:
#             ppt_source_url = 'https:'+bytes_info.get('sUrl')
#             download_img(ppt_source_url,key)
#             print('第'+str(index)+ppt_source_url)
#             last_img_sequence = int(key)
#             last_img = cv2.imread('download/'+ str(last_img_sequence) +'.png')
#             last_img = cv2.resize(last_img,dsize=(video_width,video_height),fx=1,fy=1,interpolation=cv2.INTER_LINEAR)
#         elif 'points' in bytes_info:
#             print('绘制：'+str(last_sequence))
#             draw(bytes_info,last_img,key)
                
#         last_sequence = int(key)
#     time.sleep(1)
#     ppt_obj = get_ppt(last_sequence,token_obj.get('token'),token_obj.get('roomInfo').get('iRoomId'))
#     while(('sequenceMap' not in ppt_obj) & (last_sequence + 300000 <= end_time)):
#         last_sequence += 3000
#         ppt_obj = get_ppt(last_sequence,token_obj.get('token'),token_obj.get('roomInfo').get('iRoomId'))
#         time.sleep(1)

convert_to_video()

download_audio(audio_url)  

combin_audio_to_video()


'----------------------------------测试代码1------------------------------------'
# fourcc = cv2.VideoWriter_fourcc('m','p','4','v')        # 设置输出视频为mp4格式
# cap_fps = 30
# size = (video_width, video_height)

# video = cv2.VideoWriter('output/result.mp4',fourcc, cap_fps, size)
  
# img_E = cv2.imread('download/1596462217438.png')
# img_E = cv2.resize(img_E,dsize=(video_width,video_height),fx=1,fy=1,interpolation=cv2.INTER_LINEAR)
# video.write(img_E)
# video.release()


# images = os.listdir('download')
# for i, img in enumerate(images[1:]):
#     timestamp = int(img.split('.')[0])
#     print(str(timestamp))
'----------------------------------测试代码2（涂鸦绘制）------------------------------------'
#点连线
# def dot_json2array(json):
#     pList = []
#     for p in json:
#         p1 = [(1200*p.get('x')/10000),(675*p.get('y')/10000)]
#         pList.append(p1)
#     return np.array(pList,np.int32)

# image = cv2.imread('download/1596453638267.png')

# json1 = json.loads('[{"x":426,"y":7487},{"x":426,"y":7533},{"x":439,"y":7579},{"x":439,"y":7625},\
#                    {"x":452,"y":7625},{"x":452,"y":7648},{"x":465,"y":7671},{"x":465,"y":7694},\
#                        {"x":490,"y":7717},{"x":503,"y":7763},{"x":516,"y":7786},{"x":529,"y":7786},\
#                            {"x":529,"y":7809},{"x":710,"y":7809},{"x":801,"y":7786},{"x":826,"y":7786}]')
# cv2.polylines(image,[dot_json2array(json1)],False,(0,0,255),6)
# cv2.imwrite('test.png', image)
#矩形
# image = cv2.imread('download/1596453638267.png')
# tangle=cv2.rectangle(image, (84, 45), (210, 228), (0, 0, 255), 3,cv2.LINE_4)
# cv2.imwrite('test.png', image)

#文字
# image = cv2.imread('download/1596453638267.png')
# image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
# draw = ImageDraw.Draw(image)
# # 字体的格式
# fontStyle = ImageFont.truetype(
#     "font/simsun.ttc", 20, encoding="gbk")
# # 绘制文本
# draw.text((10,500), '中文乱码', (0,0,255), font=fontStyle)

# cv2.imwrite('test.png', np.array(image))