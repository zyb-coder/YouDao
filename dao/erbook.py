import util.DbUtil as db
#导入util文件夹下的DbUtil文件

class erbook:

    '''对erbook表的增删改查'''

    def add_erbook(self):#向erbook表插入数据

        con = db.dbutil(self) #连接数据库
        cursor = con.cursor()  # 使用cursor()方法创建一个游标对象

        try:
            #执行sql语句，插入单条数据   若多个数据建立data列表用executmany()函数
            cursor.execute('insert into erbook values (6,"4","4","4","略");')
            con.commit()  # 提交事务
            return 1  #成功插入返回1
        except:
            con.rollback()  # 发生错误时回滚

        cursor.close()  # 关闭游标
        con.close()#关闭数据库连接
        return 0  #插入失败返回0


    def check_erbook(self):#查询表中的数据

        con = db.dbutil(self)  # 连接数据库
        cursor = con.cursor()  # 使用cursor()方法创建一个游标对象
        sql = "select * from erbook"#mysql 查询语句

        try:
            cursor.execute(sql)#执行sql语句，查询erbook表
            request1 = cursor.fetchall()
            return request1  # 返回查询到的结果
        except:
            con.rollback()  # 发生错误时回滚

        cursor.close()# 关闭游标
        con.close()  # 关闭数据库连接
        return 0  # 查询失败返回0


    def up_erbook(self):#修改erbook表中的数据
        con = db.dbutil(self)  # 连接数据库
        cursor = con.cursor()  # 使用cursor()方法创建一个游标对象
        # mysql 修改语句  占位符用%s
        sql = 'update erbook set wrid = %s where id = %s'

        try:
            cursor.execute(sql,(9,1))  # 执行sql语句，查询erbook表
            con.commit()  # 提交事务
            return 1  # 修改成功返回1
        except:
            con.rollback()  # 发生错误时回滚

        cursor.close()  # 关闭游标
        con.close()  # 关闭数据库连接
        return 0  # 修改失败返回0


    def del_erbook(self):#删除erbook表中的数据
        con = db.dbutil(self)  # 连接数据库
        cursor = con.cursor()  # 使用cursor()方法创建一个游标对象
        # mysql 删除语句  占位符用%s
        sql = 'delete from erbook where id = %s'

        try:
            cursor.execute(sql,(6))  # 执行sql语句
            con.commit()  # 提交事务
            return 1  # 删除成功返回1
        except:
            con.rollback()  # 发生错误时回滚

        cursor.close()  # 关闭游标
        con.close()  # 关闭数据库连接
        return 0  # 删除失败返回0


if __name__ =='__main__':
    eb = erbook()#实例化类
    a = eb.del_erbook()#调用类中的方法
    print(a)

