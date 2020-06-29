import util.DbUtil as db


# 导入util文件夹下的DbUtil文件

class Dao:

    def check(self, english):  # 对数据表的查询操作
        con = db.dbutil(self)  # 连接数据库
        cursor = con.cursor()  # 使用cursor()方法创建一个游标对象
        sql = 'select id,count,time from kyword WHERE en = "%s"'%(english)
        try:
            cursor.execute(sql)  # 执行sql语句，查询表
            tup = cursor.fetchall()  # 获取查询到的结果
            cursor.close()  # 关闭游标
            con.close()  # 关闭数据库连接
            if not tup:  # 查询为空次数和id都放回0
                id = 0
                count = 0
                time = ''
            else:
                id = tup[0][0]  # 提取id
                count = tup[0][1]  # 提取次数
                time = tup[0][2]
            return id, count, time  # 返回id 次数 备注
        except:
            con.rollback()  # 发生错误时回滚
            cursor.close()  # 关闭游标
            con.close()  # 关闭数据库连接
            return False, False  # 查询失败返回False

    def insert(self, sql, en, zh, count, time):  # 对数据表插入操作
        con = db.dbutil(self)  # 连接数据库
        cursor = con.cursor()  # 使用cursor()方法创建一个游标对象
        try:
            # 执行sql语句，插入单条数据   若多个数据建立data列表用executmany()函数
            cursor.execute(sql, (en, zh, count, time))  # mysql 语句和 插入的值
            con.commit()  # 提交事务
            cursor.close()  # 关闭游标
            con.close()  # 关闭数据库连接
            return 1  # 成功插入返回1
        except:
            con.rollback()  # 发生错误时回滚
            cursor.close()  # 关闭游标
            con.close()  # 关闭数据库连接
            return 0  # 插入失败返回0

    def delete(self, sql):  # 删除erbook表中的数据
        con = db.dbutil(self)  # 连接数据库
        cursor = con.cursor()  # 使用cursor()方法创建一个游标对象

        try:
            cursor.execute(sql)  # 执行sql语句
            con.commit()  # 提交事务
            cursor.close()  # 关闭游标
            con.close()  # 关闭数据库连接
            return 1  # 删除成功返回1
        except:
            con.rollback()  # 发生错误时回滚
        cursor.close()  # 关闭游标
        con.close()  # 关闭数据库连接
        return 0  # 删除失败返回0

    def set(self, id, count, time):  # 修改数据库
        con = db.dbutil(self)  # 连接数据库
        cursor = con.cursor()  # 使用cursor()方法创建一个游标对象
        sql = 'UPDATE kyword set count=%d,time="%s" where id =%d;'%(count, time, id)
        try:
            cursor.execute(sql)  # 执行sql语句
            con.commit()  # 提交事务
            cursor.close()  # 关闭游标
            con.close()  # 关闭数据库连接
            return 1  # 修改返回1
        except:
            con.rollback()  # 发生错误时回滚
        cursor.close()  # 关闭游标
        con.close()  # 关闭数据库连接
        return 0  # 修改失败返回0

    def call(self, sql):  # 对数据表的查询操作
        con = db.dbutil(self)  # 连接数据库
        cursor = con.cursor()  # 使用cursor()方法创建一个游标对象
        try:
            cursor.execute(sql)  # 执行sql语句，查询表
            tup = cursor.fetchall()  # 获取查询到的结果
            cursor.close()  # 关闭游标
            con.close()  # 关闭数据库连接
            return tup  # 返回元组类型包含多种类型
        except:
            con.rollback()  # 发生错误时回滚
            cursor.close()  # 关闭游标
            con.close()  # 关闭数据库连接
            return False  # 查询失败返回False


if __name__ == '__main__':
    import os
    import sys

    curPath = os.path.abspath(os.path.dirname(__file__))

    rootPath = os.path.split(curPath)[0]

    PathProject = os.path.split(rootPath)[0]

    sys.path.append(rootPath)

    sys.path.append(PathProject)

    print(sys.path)
