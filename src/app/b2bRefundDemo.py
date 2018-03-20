from flask import jsonify
from datetime import datetime
from unionpay.SDKConfig import SDKConfig
from unionpay.AcpService import AcpService
import logging


def trade():
    time_now = datetime.now().strftime('%Y%m%d%H%M%S')
    req = {}

    req["version"] = SDKConfig().version
    req["encoding"] = SDKConfig().encoding
    req["signMethod"] = SDKConfig().signMethod
    req["txnType"] = "04"
    req["txnSubType"] = "00"
    req["bizType"] = "000201"
    req["accessType"] = "0"
    req["channelType"] = "07"
    req["backUrl"] = SDKConfig().backUrl

    req["orderId"] = time_now
    req["merId"] = "777290058110048"
    req["origQryId"] = "871803200930040336758"
    req["txnTime"] = time_now
    req["txnAmt"] = "100"

    # 签名示例
    req = AcpService.sign(req)
    url = SDKConfig().backTransUrl

    # 后台自提交表单示例
    resp = AcpService.post(req, url)
    if not AcpService.validate(resp):
        logging.error("回复报文验证失败")
        return jsonify({'status': 'error', 'error': 'not validate'})

    respCode = resp['respCode']

    if respCode == "00":
        logging.info("退款受理成功!")
        return jsonify({'status': 'ok', 'data': resp})

    if respCode == "03" or respCode == "04" or respCode == "05":
        logging.warning("退款受理超时")
        return jsonify({'status': 'error', 'error': '退款受理超时'})
    else:
        logging.error("退款受理失败")
        return jsonify({'status': 'error', 'error': '退款受理失败', 'detail': resp})
