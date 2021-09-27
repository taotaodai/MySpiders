# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 17:48:58 2021

@author: Administrator
"""

import sys
import time
from enum import Enum
 
#这里我们提供必要的引用。基本控件位于pyqt5.qtwidgets模块中。
from PyQt5.QtWidgets import QApplication, QWidget,QLabel,QComboBox,QLineEdit,QPushButton
from PyQt5.QtGui import QIntValidator,QPalette
from PyQt5.QtCore import Qt,QThread,pyqtSignal
import spider_1

ORIGIN_X = 20
ORIGIN_Y = 20
H_LABEL = 35
H_EDIT = 30

executing = False
class Website(Enum):
    XIN_CHENG = {"url":"http://uc.xinchengjy.cn/","password":"Xm123456"}
    ZIKAO_35 = {"url":"http://kc.zikao35.com/","password":"Zg123456"}
    ZIKAO_HUI = {"url":"http://yzkjh.beegoedu.com/","password":"Zk123456"}
    
class Example(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.combo = QComboBox(self)
        self.lbHint = QLabel("",self)
        
        lbUsername = QLabel("用户名:", self)
        self.leUsername = QLineEdit(self)
        lbPassword = QLabel("密码:", self)
        self.lePassword = QLineEdit(self)
        
        lbCode = QLabel("课程编号:", self)
        self.leCode = QLineEdit(self)
        lbZhang = QLabel("章:", self)
        self.leZhang = QLineEdit(self)
        self.leZhang.setValidator(QIntValidator(0,100))
        # lbJie = QLabel("节:", self)
        # self.leJie = QLineEdit(self)
            
        self.start = QPushButton("开始",self)
        
        for name,member in Website.__members__.items():
            self.combo.addItem(member.value["url"])

        self.combo.move(ORIGIN_X, ORIGIN_Y)
        self.lbHint.setGeometry(220,ORIGIN_Y,150,20)
        palette = QPalette()
        palette.setColor(QPalette.WindowText,Qt.red)
        self.lbHint.setPalette(palette)
        self.lbHint.setWordWrap(True)
        
        lbUsername.move(ORIGIN_X,ORIGIN_Y + H_LABEL*1)
        self.leUsername.setGeometry(ORIGIN_X + 60,ORIGIN_Y + H_LABEL*1,80,20)
        lbPassword.move(ORIGIN_X + 150,ORIGIN_Y + H_LABEL*1)
        self.lePassword.setGeometry(ORIGIN_X + 210,ORIGIN_Y + H_LABEL*1,80,20)
        
        lbCode.move(ORIGIN_X,ORIGIN_Y + H_LABEL*2)
        self.leCode.setGeometry(ORIGIN_X + 60, ORIGIN_Y + H_LABEL*2,80,20)
        
        lbZhang.move(ORIGIN_X + 150, ORIGIN_Y + H_LABEL*2)
        self.leZhang.setGeometry(ORIGIN_X + 170, ORIGIN_Y + H_LABEL * 2, 30, 20)
        
        # lbJie.move(ORIGIN_X + 220,ORIGIN_Y + H_LABEL*2)
        # self.leJie.setGeometry(ORIGIN_X + 240, ORIGIN_Y + H_LABEL * 2, 30, 20)

        self.combo.activated[str].connect(self.onActivated)
        
        self.start.move(140,140)
        self.start.clicked[bool].connect(self.onStart)

        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('QComboBox')
        self.show()
        self.showTestData()

    def onActivated(self, text):
        print(text)
    
    def showTestData(self):
        self.leUsername.setText("17820020047")
        self.lePassword.setText("Zk123456")
        self.leCode.setText("51-01850")
        
    def onStart(self):
        global executing
        if executing:
            self.thread.terminate()
            spider_1.cancel()
            executing = False
            self.start.setText("开始")
        else:            
            username = self.leUsername.text()
            if username:    
                print("用户名",username)
            else:
                self.lbHint.setText("请输入用户名")
                return
            password = self.lePassword.text()
            if password:    
                print("密码",password)
            else:
                self.lbHint.setText("请输入密码")
                return
            courseCode = self.leCode.text()
            if courseCode:
                print("课程编号",courseCode)
            else:
                self.lbHint.setText("请输入课程编号")
                return
            
            zhang = self.leZhang.text()
            if zhang:
                zhang = int(zhang)
            else:
                zhang = 1
            self.start.setText("取消")
            executing = True
            self.thread = DownloadTheard(self.combo.currentText(),username,password,courseCode,zhang)
            self.thread.hint_text.connect(self.showHint)
            self.thread.start()
            
    def showHint(self,text):
        self.lbHint.setText(text)
        
    
class DownloadTheard(QThread):
    
    hint_text = pyqtSignal(str)  # 信号类型 str
    
    def __init__(self,url,username,password,courseCode,zhang,parent=None):
    # def __init__(self,parent=None):
        super(DownloadTheard, self).__init__(parent)
        self.url = url
        self.username = username
        self.password = password
        self.courseCode = courseCode
        self.zhang = zhang

    def run(self):
        # while True:
        #     self.count = self.count + 1
        #     self.hint_text.emit(str(self.count))
        #     time.sleep(1)

        spider_1.start(self.username,self.password,self.courseCode,url=self.url,zhang=self.zhang,hintCallback=self.hintCallback)
    
    def hintCallback(self,text):
        self.hint_text.emit(text)
            
if __name__ == '__main__':
    #每一pyqt5应用程序必须创建一个应用程序对象。sys.argv参数是一个列表，从命令行输入参数。
    app = QApplication(sys.argv)
    ex = Example()
    
    # thread = DownloadTheard("","","","")
    # thread.start()

    sys.exit(app.exec_())