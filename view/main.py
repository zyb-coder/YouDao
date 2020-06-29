import os
import sys
import pygame
from threading import Thread  # 导入线程函数
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog

import dao.game as ga  # 游戏模块
import dao.YouDaofy as yd  # 有道爬虫
import dao.inputWord as iw  # 录入单词模块

from dao.Dao import Dao  # 对数据库的操作
from view.table import Ui_er_boook  # 表格界面
from view.main_window import Ui_MainWindow  # 主界面
from view.word_train import Ui_view_WordTrain  # 答题卡界面


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):  # 初始化类
        super(Main, self).__init__()
        # 首先找到 Main 的父类 再把父类Ui_MainWindow和父类类QMainWindow的对象转换为类Main的对象
        # 转换成  类Main 对象后在调用自己的初始化函数__init__()
        self.setupUi(self)

        # 定义点击按钮次数,奇数打开界面,偶数关闭界面
        self.c = 1  # 翻译界面次数
        # self.b = 1  # 词汇界面次数 bug在页面内退出 下次要点击两次菜可以
        # self.t = 1  # 训练界面次数

        self.view_fan.hide()  # 因翻译界面和主界面是一个窗体,所以先将翻译界面隐藏起来

        # 设置按钮事件  connect调用函数功能时需用 lambda定义(匿名函数)或者调用函数是不加()

        # 退出登录按钮
        self.user_out.triggered.connect(self.close)
        # 检查更新按钮
        self.help_about_check.triggered.connect(self.call)
        # 有道翻译按钮
        self.butt_fanyi.clicked.connect(self.but_fanyi)
        # 清除的按钮
        self.butt_return.clicked.connect(self.cl)
        # 翻译的按钮
        self.butt_range.clicked.connect(self.but_range)
        # 单词训练按钮
        self.butt_wordTrain.clicked.connect(self.but_word_train)
        # 查看词汇按钮
        self.butt_words.clicked.connect(self.add_word)
        # 查看错题本按钮
        # table = self.opten_table()
        self.butt_erbook.clicked.connect(self.opten_table)
        # 娱乐休闲按钮
        self.butt_test.clicked.connect(self.open_game)
        # 官网按钮事件 调用yd模块中的open_html()函数
        self.butt_guanWang.clicked.connect(lambda: yd.open_html())

    def but_fanyi(self):  # 显示翻译界面
        if self.c % 2 != 0:
            self.view_fan.show()  # 显示界面
            self.c += 1  # 次数自增1
        else:
            self.view_fan.hide()  # 隐藏界面
            self.c += 1

    def cl(self):  # 清除文本
        self.input_text.clear()  # setPlainText('')
        self.out_text.clear()  # setPlainText('')

    def but_range(self):  # 翻译按钮事件
        try:
            # z2011 含义真题20年英一第一篇阅读
            # uN'#含义第N单元单词 'sNN' 第十几单元 'hx'易混淆的单词
            beizhu = self.lien_bz.text()  # 获取备注信息
            str = self.input_text.toPlainText()  # 获取多文本行中的内容
            # 判断输入的是否为空或者全是空格,防止程序崩溃
            if len(str) != 0 | str.isspace() == False:
                chinese = yd.fanyi(str)  # 调用yd模块中的fanyi()函数
                if chinese[0] == str:  # 单词拼写错误会返回原字符串,就不将其写入数据库
                    # %s是一个占位符
                    tishi = '%s' + '\n拼写有误' + '\n' + '不写入数据中' + '\n' + '请重新输入'
                    self.out_text.setPlainText(tishi % chinese)
                elif chinese == 'errorCode':
                    self.tishi("网络环境较差或拼写错误")
                else:
                    ch = "\n"
                    for zh in chinese:  # 遍历返回的整个列表
                        ch = ch + zh + "\n"  # 将每一项相加起来并换行
                    self.out_text.setPlainText(ch)  # 将整个字符串输出到多行文本框中

                    # now_time = datetime.datetime.now()# 获取当地时间
                    # time_str = datetime.datetime.strftime(now_time, '%Y-%m-%d %H:%M:%S')# 将时间转换程字符串

                    # 将查询过的单词写入数据库并累计查询的次数
                    dao = Dao()  # 连接数据库
                    id, count, unit = dao.check(str)  # 查询曾经查过的次数
                    if count == 0:  # 如果没有查询过,就添加进去
                        count += 1  # 增加一次
                        sql = "insert into kyword (en,zh,count,time) values (%s,%s,%s,%s);"
                        re = dao.insert(sql, str, ch, count, beizhu)
                        if re == 0:
                            self.tishi("写入数据库失败")
                    elif count > 0:  # 如果曾经查询过
                        count += 1  # 就在次数上加一

                        if beizhu in unit:  # 以前在这个地方出现过,就只增加次数
                            zong = unit
                        else:
                            zong = unit + '-' + beizhu  # 现在录入的单元和以前录入的单元相加

                        i = dao.set(id, count, zong)  # 修改次数和单元
                        if i == 0:
                            self.tishi("修改数据库失败")
                    elif not id:
                        self.tishi("查询数据库失败")
            else:
                pass
        except:
            self.tishi("网络环境较差或拼写错误")

    def but_word_train(self):  # 打开单词训练窗口
        self.MainW = QMainWindow()
        ui = Ui_view_WordTrain()  # 将包中的子页面类实例化
        bz = self.lien_bz.text()  # 获取当前单元信息
        ui.setupUi(self.MainW)  # 初始化页面将信号与槽建立起来
        ui.load_data(bz)  # 加载答题卡信息
        self.MainW.show()  # 让窗口显示出来

    def add_word(self):  # 将txt中的单词添加到数据库中
        try:
            self.tishi("建议夜间录入单词,\n防止ip被限制,录入速率过慢"
                       ",\n进度和异常在data文件夹下查看")
            # 获取文件夹路径
            filsrc = QFileDialog.getExistingDirectory(self, "请选择文件夹路径", "e:\youdao")
            if len(filsrc) == 0:
                self.tishi("取消添加")
            else:
                src = filsrc + '/'
                # 定义线程aW，线程任务为调用iw.start函数,iw.start函数的参数是路径args类型为元组 一个参数也要有逗号
                addWord = Thread(target=iw.start, args=(src,))
                addWord.start()  # 开始执行这个线程
                if not addWord.isAlive():  # 返回线程是否活动的。
                    self.tishi("子线程出错")
        except:
            self.tishi("添加失败")

    def opten_table(self):  # 打开单词库
        self.table = QMainWindow()
        ui = Ui_er_boook()  # 将包中的子页面类实例化
        ui.setupUi(self.table)  # 初始化页面将信号与槽建立起来
        beizhu = self.lien_bz.text()  # 获取备注信息
        ui.lad_table(beizhu)  # 加载table信息
        self.table.show()  # 让窗口显示出来

    def call(self):  # 提示框
        reply = QMessageBox.question(self, '提示', '已是最新版本！！！',
                                     QMessageBox.Yes, QMessageBox.Yes)

    def tishi(self, str):  # 提示框
        reply = QMessageBox.question(self, '提示', str,
                                     QMessageBox.Yes, QMessageBox.Yes)

    def open_game(self):
        # 调用默认程序,播放音乐
        os.system("start explorer data\music.mp3")

        # 打开游戏窗口
        pygame.init()
        pygame.font.init()
        catchball = ga.Main1()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    Main = Main()  # 实例化类
    Main.show()
    sys.exit(app.exec_())  # 类似于一个循环让窗口不一闪而过
