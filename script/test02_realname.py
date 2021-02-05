import pytest
import requests

from api import log
from api.api import Api
from util import common_assert, parser_html, read_json


class TestRealName:
    # 初始化
    def setup(self):
        # 获取session对象
        self.session = requests.session()
        # 获取Api对象
        self.api = Api(self.session)
        # 获取ApiRealName对象
        self.realname = self.api.api_get_ApiRealName()

    # 结束
    def teardown(self):
        # 关闭session对象
        self.session.close()

    # 1、认证接口测试方法
    @pytest.mark.parametrize(("realname","card_id","expect_msg"),read_json("realname.json","realname"))
    def test01_realname(self, realname,card_id,expect_msg):
        # 调用登录
        self.api.api_get_ApiRegLogin().api_login("13600001111", "test123")
        # 调用认证接口
        result = self.realname.api_realname(realname,card_id)
        try:
            print("响应结果为：",result.json())
            # 断言
            common_assert(result,expect_msg=expect_msg)
        except Exception as e:
            # 日志
            log.error(e)
            # 抛异常
            raise

    # 2、开户接口测试方法
    @pytest.mark.parametrize(("status","expect_msg"),read_json("realname.json","trust"))
    def test02_trust(self, status, expect_msg):
        if status == "登录":
            # 调用登录
            self.api.api_get_ApiRegLogin().api_login("13600001111", "test123")
            # 调用开户接口
            result = self.realname.api_trust()
            # 如果开户成功 则需要三方开户
            r = parser_html(result)
            # 三方开户
            result = self.session.post(url=r[0], data=r[1])
            try:
                print("开户响应结果为：", result.text)
                # 断言
                common_assert(result, expect_text=expect_msg)
            except Exception as e:
                # 日志
                log.error(e)
                # 抛异常
                raise
        else:
            # 调用开户接口
            result = self.realname.api_trust()
            # 如果开户成功 则需要三方开户
            # 三方开户
            try:
                print("开户响应结果为：", result.text)
                # 断言
                common_assert(result, expect_text=expect_msg)
            except Exception as e:
                # 日志
                log.error(e)
                # 抛异常
                raise

    # 3、充值验证码接口测试方法
    @pytest.mark.parametrize(("random","expect_code"),read_json("realname.json","vericy_code"))
    def test03_verify_code(self, random,expect_code):
        # 调用充值验证码接口
        result = self.realname.api_verify_code(random)
        try:
            # 断言
            common_assert(result, expect_code=expect_code)
        except Exception as e:
            # 日志
            log.error(e)
            # 抛异常
            raise

    # 4、充值接口 测试方法
    @pytest.mark.parametrize(("amount","valicode","expect_text"),read_json("realname.json","recharge"))
    def test04_recharge(self, amount, valicode, expect_text):
        # 登录
        self.api.api_get_ApiRegLogin().api_login("13600001111", "test123")
        # 充值验证码
        self.realname.api_verify_code(123123)
        # 充值
        result = self.realname.api_recharge(amount=amount,img_code=valicode)
        if expect_text == "OK":
            # 三方充值
            r = parser_html(result)
            result = self.session.post(r[0],data=r[1])
            print("充值结果为：", result.text)
            try:
                common_assert(result,expect_text=expect_text)
            except Exception as e:
                # 日志
                log.error(e)
                # 抛异常
                raise
        else:
            try:
                common_assert(result, expect_text=expect_text)
            except Exception as e:
                # 日志
                log.error(e)
                # 抛异常
                raise