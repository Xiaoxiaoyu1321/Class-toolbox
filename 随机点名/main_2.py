#导入必须的库
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QFont ,QIcon
from PyQt5.QtCore import  Qt
import sys
import os
import random
import time
import _thread
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


        # 连接信号与槽
        self.Start_button.clicked.connect(self.Start_button_do)
        self.Open_File_button.clicked.connect(self.Open_File_button_do)


        #初始化要做的
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setText('未选定')

        font = self.name_label.font()  # 获取当前字体
        font.setPointSize(72)  # 设置新的字体大小
        self.name_label.setFont(font)  # 应用新的字体

        font = self.name_label.font()  # 获取当前字体
        font.setPointSize(24)
        self.Start_button.setFont(font)

    def choose_student(self):
        count = len(name_list)
        if count == 0 :
            self.name_set('文件为空')
        r_i = random.randint(0,count - 1)
        student = name_list[r_i]
        return student
    def a_student(self):

        self.Start_button.setEnabled(False)
        self.Start_button.setText('正在抽取...')
        num = 0
        while num <= 15:
            num = num + 1
            self.name_set(self.choose_student())
            time.sleep(0.08)
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

def TrueStart():
    checkfile()
    load_file()


if __name__ == '__main__':

    TrueStart()


    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())