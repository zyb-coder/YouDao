import time
import random
import hashlib
import requests
import webbrowser
from os import system


def make_md5(string):  # md5码加密
    string = string.encode('utf-8')
    md5 = hashlib.md5(string).hexdigest()
    return md5


def fanyi(word):
    url = "http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule"

    # 模仿js文件生成提单中的变量
    ts = str(int((time.time() * 1000)))  # 获取本地时间取整部
    salt = ts + str(random.randint(0, 9))  # 在ts后加一位0-9的数值 闭区间
    sign = make_md5("fanyideskweb" + word + salt + "n%A-rKaT5fb[Gy?;N5@Tj")
    bv = make_md5(
        "5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36")
    # 设备信息MD5加密

    # 头部字典
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'OUTFOX_SEARCH_USER_ID_NCOO=5049841.05502916; OUTFOX_SEARCH_USER_ID="-1399227025@10.169.0.83"; _ntes_nnid=8b6e61524064f1eacda98b567a179fe5,1571322761992; JSESSIONID=aaasjfXZVTWw18y8X2I3w; ___rl__test__cookies=1571474782735',
        'Host': 'fanyi.youdao.com',
        'Origin': 'http://fanyi.youdao.com',
        'Referer': 'http://fanyi.youdao.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }

    # 要提交的表单字典
    data = {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": salt,
        "sign": sign,
        "ts": ts,
        "bv": bv,
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_CLICKBUTTION"
    }

    dip = {
        'http': '120.83.102.246:9999'
    }

    # 用post方式向服务器发送请求 没有data参数用get方式 json()将js格式转换python格式
    request = requests.post(url=url, headers=headers, data=data).json()

    if request['errorCode'] != 0:  # 如果查询不出来 返回字符串
        return 'errorCode'

    chinese = []  # 盛放所有翻译结果的列表

    zh = request['translateResult'][0][0]['tgt']  # 提取想要的信息 通过键查找值 内容为最直接的翻译

    chinese.append(zh)  # 将最直接的翻译放到列表当中

    if 'smartResult' in request:  # 判断 smartResult 是否存在 request字典中 如果存在则有更多的含义
        # 遍历更多含义的个数依次输出
        for i in range(0, len(request['smartResult']['entries'])):
            # 将更多的含义放到列表当中  将结果中的换行符 “\r\n”去除掉
            chinese.append(request['smartResult']['entries'][i].strip('\r\n'))

    return chinese  # 返回一个盛放一个或多个的翻译结果列表


def open_html():  # 调用默认浏览器打开指定网址
    system("start explorer data\index.html")


if __name__ == "__main__":
    word = "love"
    chinese = fanyi(word)
    print(chinese)
