
# coding:utf-8

import re
import dao.YouDaofy as yd  # 有道爬虫
from dao.Dao import Dao
import time
import random
import os
import logging


def CountNum(filepath):
    wlist = []  # 单词
    clist = []  # 次数
    myfile = open(filepath, 'r', encoding='utf-8')
    content = myfile.read()
    CountDict = {}
    pattern = '[,.\s]\s*'  # [\s\S]*?表示匹配任意字符，且只匹配一次，即懒惰匹配；去掉?为贪婪匹配
    words = re.split(pattern, content)  # 按指定字符进行切割
    for word in words:
        if word not in CountDict and word.isalpha():  # isalpha() 方法检测字符串是否只由字母组成
            CountDict[word.lower()] = 1  # lower() 方法转换字符串中所有大写字符为小写。
        elif word in CountDict:
            CountDict[word.lower()] += 1  # 次数加一
    # 将字典中每个键值打包成一小元组,后按从小到大排序.
    result = sorted(zip(CountDict.keys(), CountDict.values()))
    for i, j in result:  # 一次性遍历一个元组
        wlist.append(i)
        clist.append(j)
    return wlist, clist  # 返回单词数组和次数数组


def write(file, beizhu):
    w, c = CountNum(file)
    try:
        for i in range(len(w)):
            less = len(w) - i  # 剩余单词个数
            print(beizhu, "文件剩余单词数：", less)
            log('进度', 'info', '%s-文件剩余单词数：%d' % (beizhu, less))
            en = w[i]
            if i > 0 and i % 50 == 0:
                time.sleep(30)
            time.sleep(random.uniform(5, 10))  # 沉睡0.5秒
            chinese = yd.fanyi(en)  # 调用yd模块中的fanyi()函数
            if chinese[0] == en:  # 单词拼写错误会返回原字符串,就不将其写入数据库
                log('异常', 'warning', '%s-查询失败,来自文件-%s' % (en, beizhu))  # 查询失败写入日志中
            elif chinese == 'errorCode':
                log('异常', 'warning', '%s-查询失败,来自文件-%s' % (en, beizhu))  # 查询失败写入日志中
            else:
                ch = "\n"
                for zh in chinese:  # 遍历返回的整个列表
                    ch = ch + zh + "\n"  # 将每一项相加起来并换行
                # 将查询过的单词写入数据库并累计查询的次数

                dao = Dao()  # 连接数据库
                id, count, unit = dao.check(en)  # 查询曾经查过的次数
                if count == 0:  # 如果没有查询过,就添加进去
                    count += c[i]  # 增加一次
                    sql = "insert into kyword (en,zh,count,time) values (%s,%s,%s,%s);"
                    re = dao.insert(sql, en, ch, count, beizhu)
                    if re == 0:
                        log('异常', 'error', '%s-写入数据库失败,来自文件-%s' % (en, beizhu))  # 写入日志中
                elif count > 0:  # 如果曾经查询过
                    count += c[i]  # 就在次数上加一

                    if beizhu in unit:  # 以前在这个地方出现过,就只增加次数
                        zong = unit
                    else:
                        zong = unit + '-' + beizhu  # 现在录入的单元和以前录入的单元相加

                    i = dao.set(id, count, zong)  # 修改次数和单元
                    if i == 0:
                        log('异常', 'error', '%s-修改数据库失败,来自文件-%s' % (en, beizhu))  # 写入日志中
                elif not id:
                            log('异常', 'error', '%s-数据库查询失败,来自文件-%s' % (en, beizhu))  # 写入日志中
        else:
            pass
        print(beizhu, "文件录入完成")
        log('进度', 'info', '%s-文件录入完成' % (beizhu))
    except Exception as e:
        print(e)
        log('异常', 'error', '代码出错:%s' % (str(e)))


def log(name, kind, message):
    # 第一步，创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Log等级总开关
    # 第二步，创建一个handler，用于写入日志文件
    rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))[:-4]
    log_name = 'data/' + rq + name + '.log'  # 输出到指定路径
    logfile = log_name
    fh = logging.FileHandler(logfile, mode='a')  # 追加输出
    fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh.setFormatter(formatter)
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)
    if kind == 'warning':
        logger.warning(message)
    elif kind == 'error':
        logger.error(message)
    elif kind == 'info':
        logger.info(message)
    elif kind == 'debug':
        logger.debug(message)
    else:
        logger.critical(message+'log方法,第二个参数错误')
    # 最后在记录日志之后移除句柄,防止重复录入
    logger.removeHandler(fh)


def start(path):
    try:
        j = 1
        filename_list = os.listdir(path)  # 获取文件夹下的文件
        for i in filename_list:  # 遍历文件名
            info = '共有%d个文件第,正在录入第%d个文件' % (len(filename_list), j)
            print(info)
            log('进度', 'info', info)
            a = i.index(".")  # 获取.的位置
            beizhu = i[0:a]  # 获取名字不带txt格式
            src = path + i
            write(src, beizhu)
            j += 1
        print("全部文件录入完成")
        log('进度', 'info', "全部文件录入完成")
        log('进度', 'info', "---------------------------------------------------------")
        return 1
    except Exception as e:
        log('异常', 'error', '代码出错:%s' % (str(e)))


if __name__ == '__main__':
    start('E:/youdao')
    # write('E:/youdao/2021.txt')
    # w,c= CountNum('E:/youdao/ti/z1823.txt')
    # print(len(w))
