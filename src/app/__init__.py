from flask import Flask, request
from urllib import parse
from . import frontTradeDemo, frontRcvResponse, backRcvResponse, backTradeDemo, fileDownload, batTrans, \
    batTransQuery, multiCertDemo, multiKeyDemo, frontTradeDemo2, encryptCerUpdateQuery


def create_app():
    app = Flask(__name__)

    @app.route("/", methods=['GET'])
    def index():
        return "<a href='frontTradeDemo'>前台交易示例</a><br>\n" \
               "<a href='frontTradeDemo2'>前台交易示例</a><br>\n" \
               "<a href='backTradeDemo'>后台交易示例</a><br>\n" \
               "<br>\n" \
               "<a href='fileDownload'>对账文件下载示例</a><br>\n" \
               "<a href='batTrans'>批量交易示例</a><br>\n" \
               "<a href='batTransQuery'>批量查询示例</a><br>\n" \
               "<a href='multiCertDemo'>多证书示例</a><br>\n" \
               "<a href='multiKeyDemo'>多密钥示例</a><br>\n" \
               "<a href='encryptCerUpdateQuery'>加密证书更新示例</a><br>\n"

    @app.route("/frontTradeDemo", methods=['GET'])
    def front_trade():
        return frontTradeDemo.getDemoHtml()

    @app.route("/frontTradeDemo2", methods=['GET'])
    def front_trade2():
        return frontTradeDemo2.getDemoHtml()

    @app.route("/backTradeDemo", methods=['GET'])
    def back_trade():
        return backTradeDemo.demoTrade()

    @app.route("/fileDownload", methods=['GET'])
    def file_download():
        return fileDownload.trade()

    @app.route("/batTrans", methods=['GET'])
    def bat_trans():
        return batTrans.trade()

    @app.route("/batTransQuery", methods=['GET'])
    def bat_query():
        return batTransQuery.trade()

    @app.route("/multiCertDemo", methods=['GET'])
    def multi_cert():
        return multiCertDemo.trade()

    @app.route("/multiKeyDemo", methods=['GET'])
    def multi_key():
        return multiKeyDemo.trade()

    @app.route("/frontRcvResponse", methods=['POST'])
    def front_notify():
        request_dict = parse_response_data(request.get_data())
        return frontRcvResponse.notify(request_dict)

    @app.route("/backRcvResponse", methods=['POST'])
    def back_notify():
        request_dict = parse_response_data(request.get_data())
        return backRcvResponse.notify(request_dict)

    @app.route("/encryptCerUpdateQuery", methods=['GET'])
    def encCertUpdate():
        return encryptCerUpdateQuery.demoTrade()

    def parse_response_data(req_data):
        req_data = req_data.decode('utf-8')
        req_dict = parse.parse_qs(req_data)
        res_dict = {}

        for el in req_dict:
            res_dict[el] = req_dict[el][0]

        return res_dict

    return app
