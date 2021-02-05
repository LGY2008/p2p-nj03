import logging.handlers
import os
import json

import pymysql
from bs4 import BeautifulSoup
from config import dir_path


# 公共断言封装
def common_assert(result, expect_msg=None, expect_code=None, expect_text=None):
    try:
        if expect_code:
            assert result.status_code == expect_code, "预期结果：{} 实际结果：{}".format(expect_code, result.status_code)
        if expect_msg:
            assert expect_msg in result.json().get("description"), "预期结果：{} 实际结果：{}".format(expect_msg,
                                                                                            result.json().get(
                                                                                                "description"))
        if expect_text:
            assert expect_text in result.text, "预期结果：{} 属于 实际结果：{}".format(expect_text, result.text)
    except Exception as e:
        # 抛异常
        raise
        # 打印日志


# 日志封装
class GetLog:
    logger = None

    @classmethod
    def get_logger(cls):
        if cls.logger == None:
            # 1、获取日志器
            cls.logger = logging.getLogger()
            # 2、设置日志器级别
            cls.logger.setLevel(logging.INFO)
            # 3、获取处理器 根据时间切割
            filename = dir_path + os.sep + "log" + os.sep + "p2p.log"
            tf = logging.handlers.TimedRotatingFileHandler(filename=filename,
                                                           when="midnight",
                                                           interval=1,
                                                           backupCount=3,
                                                           encoding="utf-8")
            # 4、获取格式器
            fm = "%(asctime)s %(levelname)s [%(name)s] [%(filename)s (%(funcName)s:%(lineno)d] - %(message)s"
            fmt = logging.Formatter(fm)
            # 5、将格式器添加到处理器中
            tf.setFormatter(fmt)
            # 6、将处理器添加到日志器中
            cls.logger.addHandler(tf)
        # 返回日志器
        return cls.logger


# 读取json工具
def read_json(filename, data_name):
    # 组装数据文件绝对路径
    filepath = dir_path + os.sep + "data" + os.sep + filename
    # 新建空列表 ->将读取数据添加到列表中
    arrs = []
    # 打开文件
    with open(filepath, "r", encoding="utf-8") as f:
        # 遍历所有文件
        for data in json.load(f).get(data_name):
            # 将值追加到空列表中
            arrs.append(tuple(data.values())[1:])
        # 返回列表
        return arrs


# 提取html->三方接口
def parser_html(result):
    # 1、提取html
    file = result.json().get("description").get("form")
    # 2、获取soup对象
    soup = BeautifulSoup(file, "html.parser")
    # 3、提取url
    url = soup.form.get("action")
    data = {}
    # 4、提取所有input中name和value属性
    for el in soup.find_all("input"):
        data[el.get("name")] = el.get("value")
    # 5、返回提取所有值
    return url, data


# 数据库工具类
class DButil:

    # 1、执行sql
    @classmethod
    def execute_sql(cls, sql):
        # 获取连接对象
        conn = pymysql.Connect(host="52.83.144.39",
                               user="root",
                               password="Itcast_p2p_20191228",
                               database="czbk_member",
                               charset="utf8",
                               autocommit=True)
        # 获取游标对象
        cursor = conn.cursor()
        # 执行sql
        cursor.execute(sql)
        # 返回结果
        result = cursor.fetchall()
        # 关闭对象（游标、连接）
        DButil.__close_sql(cursor, conn)
        return result

    # 2、关闭对象
    @classmethod
    def __close_sql(cls, cursor=None, conn=None):
        if cursor:
            cursor.close()
        if conn:
            conn.close()


# 清除测试数据方法
def clear_data():
    sql1 = """delete i.* from mb_member_info i inner join mb_member m on m.id = i.member_id where m.phone in ("13600001111","13600001112","13600001113","13600001114","13600001115")"""
    DButil.execute_sql(sql1)
    sql2 = """delete l.* from mb_member_login_log l inner join mb_member m on m.id=l.member_id where  m.phone in ("13600001111","13600001112","13600001113","13600001114","13600001115")"""
    DButil.execute_sql(sql2)
    sql3 = """delete from mb_member where phone in ("13600001111","13600001112","13600001113","13600001114","13600001115")"""
    DButil.execute_sql(sql3)
    sql4 = """delete from mb_member_register_log where phone in ("13600001111","13600001112","13600001113","13600001114","13600001115")"""
    DButil.execute_sql(sql4)


if __name__ == '__main__':
    # GetLog.get_logger().info("info测试")
    # GetLog.get_logger().error("error测试")
    """
        格式1、：[(),()]
        列表2、：[[],[]]
    """
    clear_data()