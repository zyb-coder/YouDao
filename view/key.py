from  PyQt5.Qt import *
import sys
class My(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ddd')
        self.setFixedSize(300,60)
        self.setup_ui()

    def setup_ui(self):
        pass

    def keyPressEvent(self, evt):#重写这个函数
        if evt.key() == Qt.Key_Return:
            print('enter')
        elif evt.key() == Qt.Key_Escape:
            print('ESC')

app = QApplication(sys.argv)
Main = My()#实例化类
Main.show()
sys.exit(app.exec_())#类似于一个循环让窗口不一闪而过