from api.api_realname import ApiRealName
from api.api_reg_login import ApiRegLogin
from api.api_tender import ApiTender


class Api:
    def __init__(self, session):
        self.session = session

    # 获取ApiRegLogin对象
    def api_get_ApiRegLogin(self):
        return ApiRegLogin(self.session)

    # 获取ApiRealName对象
    def api_get_ApiRealName(self):
        return ApiRealName(self.session)

    # 获取ApiTender对象
    def api_get_ApiTender(self):
        return ApiTender(self.session)
