from config import HOST


class ApiRealName:
    # 初始化
    def __init__(self, session):
        # 获取session
        self.session = session
        # 1、认证url
        self.__url_realname = HOST + "/member/realname/approverealname"
        # 2、开户url
        self.__url_trust = HOST + "/trust/trust/register "
        # 3、充值验证码url
        self.__url_verify_code = HOST + "/common/public/verifycode/{}"
        # 4、充值url
        self.__url_recharge = HOST + "/trust/trust/recharge"

    # 1、认证接口 封装
    def api_realname(self, realname, card_id):
        # 定义data
        data = {
            "realname": realname,
            "card_id": card_id
        }
        """
            multipart/form-data:多中参数类型
            解决：参数类型传多种 如：data + files
        """
        # 调用post方法 注意：认证的请求头multipart
        return self.session.post(url=self.__url_realname, data=data, files={"x": "y"})

    # 2、开户接口 封装
    def api_trust(self):
        # 调用post方法
        return self.session.post(url=self.__url_trust)

    # 3、充值验证码接口 封装
    def api_verify_code(self,random):
        # 调用get方法
        return self.session.get(url=self.__url_verify_code.format(random))

    # 4、充值接口封装
    def api_recharge(self, amount, img_code):
        # 定义data
        data = {
            "paymentType":"chinapnrTrust",
            "amount":amount,
            "formStr":"reForm",
            "valicode":img_code

        }
        # 请求post方法
        return self.session.post(url=self.__url_recharge, data=data)
