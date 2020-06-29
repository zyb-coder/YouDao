import random
from dao.Dao import Dao


class Train:
    '''完成单词训练的方法'''

    def read_file(self):  # 读取文件
        idlist = []
        with open('data/id.txt', 'r') as f:
            idtxt = f.readlines()  # 一行为单位读取所有内容
        for i in range(len(idtxt)):  # 删除换行符
            id = idtxt[i].replace('\n', '')
            idlist.append(int(id))
        return idlist

    def ran_word(self, bz):  # 随机抽取一个单词和翻译不重复
        try:
            idtxt = self.read_file()  # 获取文件中id的列表
            dao = Dao()
            if bz == 'None' or len(bz) == 0:
                sql = 'select * from kyword;'  # 默认查询全部
            else:
                bz = '%' + bz + '%'  # 加上% 表示模糊搜索
                sql = 'select * from kyword where time like "%s";' % (bz)  # 模糊搜索

            tup = dao.call(sql)  # 获取所有数据的大元组
            idmysql = []  # 存放数据库id的列表
            for i in range(len(tup)):
                idmysql.append(tup[i][0])  # 提取所有的id

            # 取差集 idmysql中有而idtxt中没有的
            idlist = list(set(idmysql).difference(set(idtxt)))  # 未学习过的id

            if len(idlist) != 0:  # 判断词汇是否都学完
                count = len(idlist) - 1  # 返回未训练单词的个数
                random.shuffle(idlist)  # 随机打乱列表
                id = random.choice(idlist)  # 随机抽取一个id
                idlist.remove(id)  # 在列表中删除这个id

                s1 = 'select * from kyword where id = '
                sid = s1 + str(id) + ';'
                tup = dao.call(sid)  # 查询这个id的信息

                return tup[0], count  # 返回一维元组元组的列表和剩余个数 return直接结束循环
            else:
                return 'ok', 0  # 表示词汇都学完了
        except Exception as e:
            print(e)
            return 0, 0  # 表示获取单词信息失败


if __name__ == '__main__':
    tr = Train()  # 实例化类
    w, c = tr.ran_word()  # 调用类中的方法
