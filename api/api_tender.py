from config import HOST


class ApiTender:
    # 初始化
    def __init__(self, session):
        # 获取session
        self.session = session
        # 投资请求url
        self.__url_tender = HOST + "/trust/trust/tender"

    # 请求投资接口 封装
    def api_tender(self, tender_id, amount, depositCertificate):
        # data 数据
        data = {
            "id": tender_id,
            "depositCertificate": depositCertificate,
            "amount": amount
        }
        # 请求post方法
        return self.session.post(url=self.__url_tender, data=data)
