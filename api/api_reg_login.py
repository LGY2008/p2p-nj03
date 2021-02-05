from config import HOST
from api import log


class ApiRegLogin:
    # 初始化
    def __init__(self, session):
        # 获取 session
        self.session = session
        # 获取图片验证url
        self.__url_img_code = HOST + "/common/public/verifycode1/{}"
        # 获取短信验证码url
        self.__url_phone_code = HOST + "/member/public/sendSms"
        # 注册url
        self.__url_reg = HOST + "/member/public/reg"
        # 登录url
        self.__url_login = HOST + "/member/public/login"
        # 查询登录url
        self.__url_get_login = HOST + "/member/public/islogin"

    # 1、获取注册图片验证码接口 封装
    def api_reg_img(self, random=1232112334):
        # 调用get方法 并返回响应结果
        r = self.session.get(self.__url_img_code.format(random))
        # 日志
        log.info("正在调用注册图片验证接口，请求url: {} 响应状态码:{}".format(self.__url_img_code.format(random),r.status_code))
        return r

    # 2、获取短信验证码接口 封装
    def api_phone_code(self, phone, img_code, random=12312312):
        # 1、调用图片验证
        self.api_reg_img(random)
        # 2、定义请求参数
        data = {
            "phone": phone,
            "imgVerifyCode": img_code,
            "type": "reg"
        }
        log.info("正在调用注册手机验证接口，请求url: {} 请求数据：{}".format(self.__url_phone_code,data))
        # 3、调用post方法
        return self.session.post(url=self.__url_phone_code, data=data)

    # 3、注册接口 封装
    def api_register(self, phone, img_code, pwd, phone_code, invite_phone=None,random=12334523234):
        # 1、图片验证码接口
        self.api_reg_img(random)
        # 2、短信验证码接口
        self.api_phone_code(phone, img_code, random)
        # 3、请求data数据
        data = {
            "phone": phone,
            "password": pwd,
            "verifycode": img_code,
            "phone_code": phone_code,
            "dy_server": "on",
            "invite_phone": invite_phone

        }
        log.info("正在调用注册接口，请求url: {} 请求数据：{}".format(self.__url_reg,data))
        # 4、调用post方法
        return self.session.post(url=self.__url_reg, data=data)

    # 4、登录接口 封装
    def api_login(self, keywords, password):
        # 1、定义data数据
        data = {
            "keywords": keywords,
            "password": password
        }
        log.info("正在调用登录接口，请求url: {} 请求数据：{}".format(self.__url_login,data))
        # 2、调用post方法
        return self.session.post(url=self.__url_login, data=data)

    # 5、查询登录状态接口 封装
    def api_get_login(self):
        log.info("正在调用查询登录状态接口，请求url: {}".format(self.__url_get_login))
        # 调用post方法
        return self.session.post(url=self.__url_get_login)
