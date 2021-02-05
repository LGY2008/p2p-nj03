from time import sleep

import pytest
import requests

from api.api import Api
from util import common_assert, read_json, clear_data
from api import log


class TestRegLogin:
    def setup_class(self):
        # 注意：只能放到类方法中
        clear_data()

    # 初始化
    def setup(self):
        # 获取session对象
        self.session = requests.session()
        # 获取ApiRegLogin对象
        self.reg = Api(self.session).api_get_ApiRegLogin()
        self.result = None

    # 结束
    def teardown(self):
        # 关闭Session
        self.session.close()

    # 1、注册图片验证码接口 测试方法
    @pytest.mark.parametrize(("random", "expect_code"), read_json("reg_login.json", "img_code"))
    def test01_img_code(self, random, expect_code):
        # 调用图片验证码接口
        result = self.reg.api_reg_img(random)
        # 断言
        try:
            common_assert(result, expect_code=expect_code)
            log.info("-->注册图片接口断言通过！<--")
        except Exception as e:
            # 打印日志
            log.error("【注册图片接口断言不通过！】")
            log.error(e)
            # 抛异常
            raise

    # 2、注册短信接口 测试方法
    @pytest.mark.parametrize(("phone", "imgVerifyCode", "expect_msg"), read_json("reg_login.json", "phone_code"))
    def test02_phone_code(self, phone, imgVerifyCode, expect_msg):
        # 调用短信验证码接口
        result = self.reg.api_phone_code(phone, imgVerifyCode)
        # 断言
        try:
            common_assert(result, expect_msg=expect_msg, expect_code=200)
            log.info("-->注册短信接口断言通过！<--")
        except Exception as e:
            log.error("【注册短信接口断言不通过！】")
            # 打印日志
            log.error(e)
            # 抛异常
            raise

    # 3、注册接口 测试方法
    @pytest.mark.parametrize(("phone", "password", "verifycode", "phone_code", "invite_phone", "expect_msg"),
                             read_json("reg_login.json", "reg"))
    def test03_reg(self, phone, password, verifycode, phone_code, invite_phone, expect_msg):
        # 调用注册接口
        result = self.reg.api_register(phone=phone, img_code=verifycode, pwd=password, phone_code=phone_code,
                                       invite_phone=invite_phone)
        # 断言
        try:
            common_assert(result, expect_msg=expect_msg)
            log.info("-->注册接口断言通过！<--")
        except Exception as e:
            log.error("【注册接口断言不通过！】")
            # 日志
            log.error(e)
            # 抛异常
            raise

    # 4、登录接口 测试方法
    @pytest.mark.parametrize(("keywords", "password", "expect_msg"), read_json("reg_login.json", "login"))
    def test04_login(self, keywords, password, expect_msg):
        """由于跑脚本需要等待1分钟，所以暂时注释掉"""
        # if password == "error123":
        #     i = 0
        #     while i < 3:
        #         self.reg.api_login(keywords, password)
        #         i += 1
        #     # 暂停60秒
        #     sleep(60)
        #     result = self.reg.api_login("13600001111", "test123")
        #     try:
        #         common_assert(result, expect_msg="登录成功")
        #         log.info("-->登录接口锁定60秒后断言通过！<--")
        #     except Exception as e:
        #         log.error("【登录接口锁定60秒后断言不通过！】")
        #         # 日志
        #         log.error(e)
        #         # 抛异常
        #         raise
        # else:
        #     result = self.reg.api_login(keywords, password)
        #     # 断言
        #     try:
        #         common_assert(result, expect_msg=expect_msg)
        #         log.info("-->登录接口断言通过！<--")
        #     except Exception as e:
        #         log.error("【登录接口断言不通过！】")
        #         # 日志
        #         log.error(e)
        #         # 抛异常
        #         raise

        # 5、查询登录状态接口 测试方法

        # 临时使用不做错误次数验证代码
        result = self.reg.api_login(keywords, password)
        # 断言
        try:
            common_assert(result, expect_msg=expect_msg)
            log.info("-->登录接口断言通过！<--")
        except Exception as e:
            log.error("【登录接口断言不通过！】")
            # 日志
            log.error(e)
            # 抛异常
            raise

    @pytest.mark.parametrize(("status", "expect_msg"), read_json("reg_login.json", "get_login"))
    def test05_get_login(self, status, expect_msg):
        if status == "已登录":
            # 调用登录
            self.reg.api_login("13600001111", "test123")
        # 调用查询登录接口
        result = self.reg.api_get_login()
        # 断言
        try:
            common_assert(result, expect_msg=expect_msg)
            log.info("-->查询登录状态接口断言通过！<--")
        except Exception as e:
            log.error("【查询登录状态接口断言不通过！】")
            # 日志
            log.error(e)
            # 抛异常
            raise
