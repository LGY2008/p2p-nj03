import pytest
import requests

from api import log
from api.api import Api
from util import parser_html, common_assert, read_json, clear_data


class TestTender:
    # 初始化
    def setup(self):
        # 获取session
        self.session = requests.session()
        # 获取ApiRegLogin对象
        self.login = Api(self.session).api_get_ApiRegLogin()
        # 获取ApiTender对象
        self.tender = Api(self.session).api_get_ApiTender()

    # 结束
    def teardown(self):
        self.session.close()

    def teardown_class(self):
        # 注意：只能放到类方法中
        clear_data()

    # 投资接口测试方法
    @pytest.mark.parametrize(("tender_id", "amount", "depositCertificate", "expect_msg"),
                             read_json("tender.json", "tender"))
    def test01_tender(self, tender_id, amount, depositCertificate, expect_msg):
        # 1、登录
        self.login.api_login("13600001111", "test123")
        # 2、调用投资接口
        result = self.tender.api_tender(tender_id, amount, depositCertificate)
        if expect_msg == "OK":
            # 3、三方投资
            # 提取三方投资所需数据
            r = parser_html(result)
            # 请求方法投资
            result = self.session.post(url=r[0], data=r[1])
            print(result.text)
            try:
                common_assert(result, expect_text=expect_msg)
            except Exception as e:
                # 日志
                log.error(e)
                # 抛异常
                raise
        else:
            try:
                common_assert(result, expect_msg=expect_msg)
            except Exception as e:
                # 日志
                log.error(e)
                # 抛异常
                raise

    # 投资业务方法
    def test02_mock(self):
        self.api = Api(self.session)
        # 1、注册接口
        self.api.api_get_ApiRegLogin().api_register("13600001115", 8888, "test123", 666666)
        # 2、登录
        self.api.api_get_ApiRegLogin().api_login("13600001115", "test123")
        # 3、认证
        self.api.api_get_ApiRealName().api_realname("张三", "110101199008075399")
        # 4、开户
        result = self.api.api_get_ApiRealName().api_trust()
        # 5、三方开户
        r = parser_html(result)
        result = self.session.post(url=r[0], data=r[1])
        print("开户结果为：", result.text)
        common_assert(result, expect_text="OK")

        # 6、充值验证码
        self.api.api_get_ApiRealName().api_verify_code(123123)
        # 7、充值
        result = self.api.api_get_ApiRealName().api_recharge(1000, 8888)
        # 8、三方充值
        r = parser_html(result)
        result = self.session.post(url=r[0], data=r[1])
        print("充值结果为：", result.text)
        common_assert(result, expect_text="OK")

        # 9、投资
        result = self.api.api_get_ApiTender().api_tender(642, 100, -1)
        # 10、三方投资
        r = parser_html(result)
        result = self.session.post(url=r[0], data=r[1])
        print("投资结果为：", result.text)
        common_assert(result, expect_text="OK")
