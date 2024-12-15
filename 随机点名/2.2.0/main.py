from pystray import Icon,Menu,MenuItem
from PIL import Image
#导入必须的库
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QFont ,QIcon, QPainter, QColor, QBrush, QPen,QPixmap
from PyQt5.QtCore import  Qt, QRect, QPoint, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
import sys
import os
import random
import time
import _thread
import pygetwindow as gw
class StatusStorage:
    total_student = []
    backup_list = []
    currentStudent = ''


class BackgroundSignals():
    open_window_request = pyqtSignal()
    close_window_request = pyqtSignal()


class FloatingWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 设置窗口属性
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # 设置悬浮球的大小和圆角半径
        self.setFixedSize(50, 50)
        self.corner_radius = 10  # 圆角半径

        # 设置悬浮球的位置
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry.left() + 20, screen_geometry.bottom() - self.height() - 20, self.width(),
                         self.height())

        # 加载图标
        self.icon_pixmap = QPixmap('bin/icon.ico').scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # 设置悬浮球的样式（背景色通过paintEvent设置）
        self.setStyleSheet("border-radius: {0}px;".format(self.corner_radius))

        # 使整个悬浮球可点击
        self.setMouseTracking(True)
        self.pressed = False

    def paintEvent(self, event):
        """自定义绘制事件，用于绘制圆角方形背景和图标"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 设置背景色画笔和画刷
        bg_brush = QBrush(QColor(255, 255, 255, 180))  # 白色背景，带透明度
        painter.setBrush(bg_brush)

        # 绘制圆角方形背景
        rect = QRect(0, 0, self.width(), self.height())
        painter.drawRoundedRect(rect, self.corner_radius, self.corner_radius)

        # 绘制图标，保持图标中心对齐
        icon_rect = QRect(QPoint(0, 0), self.icon_pixmap.size())
        icon_rect.moveCenter(self.rect().center())
        painter.drawPixmap(icon_rect, self.icon_pixmap)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pressed = True

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.pressed:
            self.pressed = False
            self.execute_function()

    def execute_function(self):
        """要执行的函数"""
        print("悬浮球被点击了！")
        window.hide()
        window.show()

class SEEWO_Tools():
    def __init__(self):
        self.FLOAT_KEEPOPEN = False
    def showIcon(self):
        self.icon = Icon("my_icon",title="随机点名")

        menu = Menu(
            MenuItem('显示主界面',lambda:FuckingShowWindows()),
        MenuItem('退出程序',lambda:self.exitProgram())
        )

        self.icon.icon = Image.open('icon.ico')

        self.icon.menu = menu
        self.icon.run()
    def showMessage(self,messages,titles='随机点名'):
        self.icon.notify(title=titles,message=messages)
    def exitProgram(self):

        app.quit()

        self.icon.stop()
        global EXITSTATUS
        EXITSTATUS = True

    def ScanProgramTitle(self):
        global 幻灯片放映状态
        幻灯片放映状态 = False
        while EXITSTATUS == False:
            time.sleep(0.5)
            windows = gw.getAllTitles()
            #print('[Windows 监听服务]已启动',windows)
            try:
                已经找到 = False
                for i in windows:
                    if i.startswith('PowerPoint 幻灯片放映'):

                        已经找到 = True
                        if 幻灯片放映状态 == False:
                            幻灯片放映状态 = True
                            print('检测到幻灯片放映开始')
                            self.FLOAT_KEEPOPEN = True

                            floatball.show()
                            self.showMessage('幻灯片放映插件已启用')
                if 已经找到 == False:
                    if 幻灯片放映状态 == True:
                        print('幻灯片放映结束')
                        幻灯片放映状态 = False
                        floatball.hide()
            except:
                print('[Windows 监听服务]遇到错误')
                pass
            #if windows['title'] == "PowerPiont 幻灯片放映":
                #print('检测到幻灯片播放')
    def PowerPointStart(self):
        pass
#调试用
print(os.listdir('.'))
print(os.getcwd())
print(os.listdir(os.path.join(os.path.dirname(__file__),'bin')))
bin_path = os.path.join(os.path.dirname(__file__),'bin')
#定义各种需要的变量
name_list = [] #定义名字列表
name_file_path = r'name.txt' #定义点名文件
mode = 'w+' #创建打开文件模式变量
def checkfile(): #检查文件是否存在，若存在，则返回真，否则返回否，并设置mode变量
    global mode

    if os.path.exists(name_file_path):
        mode  = 'r'
        return(True)
    else:
        mode = 'w+'
        return(False)


#打开并读入文件
def read_file():
    with open(name_file_path,mode,encoding='utf-8') as f:
        if mode == "r":
            file_content = f.readlines()
            return(file_content)
        if mode == 'w+':
            default_text = '#这是一个点名文件，它采用txt文件形式保存。  \n#像这样子，以“#” 开头的文本不会被当做姓名处理，如果您希望添加注释，也可以在注释的文本前添加“#” \n#请直接将姓名每行一个粘贴到下面的空白区域，请确保没有多余的空行'

            f.write(default_text)
            return(False)

        else:
            return(False)

def load_file():
    global name_list
    result = read_file()
    print(result)
    if result != False:
        for i in result:
            if i.startswith('#') == False:
                name_list.append(i.strip())
            else:
                print('检测到注释',i)
    print(name_list)
    return name_list


class MyWindow(QtWidgets.QMainWindow):
    def refresh_status(self):

        global name_list
        print('refresh_status')
        shengyu_name = len(name_list)
        renji_name = len(self.backup_list)
        self.status_label.setText(self.sb_1 + str(self.total_student) + self.sb_2 + str(shengyu_name) + self.sb_3 + str(
            renji_name))

        random.shuffle(name_list)

    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi(bin_path + '/main.ui', self)  # 加载 .ui 文件
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint) #禁用最大化按钮
        self.setFixedSize(self.width(), self.height()) #固定宽度和高度
        self.setWindowIcon(QIcon(bin_path + '/icon.ico'))
        # 查找按钮控件（假设按钮的对象名称是 'pushButton'）

        self.Start_button = self.findChild(QtWidgets.QPushButton, 'Start_button') #开始点名按钮
        self.Open_File_button = self.findChild(QtWidgets.QPushButton, 'OpenFile_button') #打开文件按钮
        self.name_label = self.findChild(QtWidgets.QLabel,'Name_label')
        self.status_label = self.findChild(QtWidgets.QLabel,'status_label')

        # 连接信号与槽
        self.Start_button.clicked.connect(self.Start_button_do)
        self.Open_File_button.clicked.connect(self.Open_File_button_do)

        global First_boot
        #初始化要做的
        if First_boot == False:
            self.backup_list = StatusStorage.backup_list
            self.total_student = StatusStorage.total_student
            self.name_set(StatusStorage.currentStudent)
        elif First_boot == True:
            self.name_label.setText('未选定')

            #初始化列表
            self.backup_list = []
            self.total_student = len(name_list)



            First_boot  = False

        ######   设置按钮字体
        self.name_label.setAlignment(Qt.AlignCenter)
        font = self.name_label.font()  # 获取当前字体
        font.setPointSize(72)  # 设置新的字体大小
        self.name_label.setFont(font)  # 应用新的字体

        font = self.name_label.font()  # 获取当前字体
        font.setPointSize(24)
        self.Start_button.setFont(font)
        #######



        self.sb_1 = '总学生：'
        self.sb_2 = '，剩余学生：'
        self.sb_3 = '，点过学生：'
        self.refresh_status()
    def choose_student(self):
        count = len(name_list)
        if count == 0 :
            self.name_set('文件为空')
        r_i = random.randint(0,count - 1)
        self.end_student = r_i
        student = name_list[r_i]
        return student
    def del_studnet(self,num):
        global name_list
        print('will delete',name_list[int(num)])
        self.backup_list.append(name_list[int(num)])

        del name_list[num]
        self.refresh_status()

    def a_student(self):

        self.Start_button.setEnabled(False)
        self.Start_button.setText('正在抽取...')
        num = 0
        while num <= 15:
            num = num + 1
            current_student = self.choose_student()
            self.name_set(current_student)
            time.sleep(0.08)
            #end_student = current_student


        self.del_studnet(self.end_student)
        self.Start_button.setEnabled(True)
        self.Start_button.setText('开始')

    def Start_button_do(self):
        # 这里是按钮点击时要执行的代码
        print("开始按钮被点击了！")
        _thread.start_new_thread(self.a_student,())

    def Open_File_button_do(self):
        print('打开文件按钮被点击')
        os.startfile(name_file_path)
    def name_set(self,current_name):
        self.name_label.setText(str(current_name))
    def closeEvent(self, a0):
        print('退出按钮被按下')
        #保存信息
        StatusStorage.total_student = self.total_student
        StatusStorage.backup_list = self.backup_list
        StatusStorage.currentStudent = self.name_label.text()

        window.hide()
        SEEWO_Tool.showMessage('窗口已最小化到托盘')
        a0.ignore()





def TrueStart():
    checkfile()
    load_file()
def FuckingShowWindows():
    global app
    global window
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    global floatball
    floatball = FloatingWidget()

    #floatball.show()
    floatball.show()
    window.show()

    floatball.hide()
    sys.exit(app.exec_())



if __name__ == '__main__':
    First_boot = True
    EXITSTATUS = False
    TrueStart()
    SEEWO_Tool=SEEWO_Tools()

    #_thread.start_new_thread(showIconService,())
    _thread.start_new_thread(FuckingShowWindows,())
    _thread.start_new_thread(SEEWO_Tool.ScanProgramTitle,())
    SEEWO_Tool.showIcon()


