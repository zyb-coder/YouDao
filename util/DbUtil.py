import pymysql



def dbutil(self): #连接数据库

    # 主机名，用户名，密码，数据库名，编码格式
    db = pymysql.connect("localhost","root","123456","insist",charset="utf8")

    return db
