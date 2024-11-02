#导入需要的库
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


#导入主窗口文件
import main_ui


app = QApplication(sys.argv)
MainWindow = QMainWindow()
ui = main_ui.Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
