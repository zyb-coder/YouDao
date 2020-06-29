
import sys
from PyQt5.QtWidgets import QApplication
from view.main import Main

app = QApplication(sys.argv)
Main = Main()  # 实例化类
Main.show()
sys.exit(app.exec_())  # 类似于一个循环让窗口不一闪而过
