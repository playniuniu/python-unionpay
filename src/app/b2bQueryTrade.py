import logging
from datetime import datetime
from flask import jsonify
from unionpay.SDKConfig import SDKConfig
from unionpay.AcpService import AcpService


def trade():
    time_now = datetime.now().strftime('%Y%m%d%H%M%S')
    req = {}

    req["version"] = SDKConfig().version
    req["encoding"] = SDKConfig().encoding
    req["signMethod"] = SDKConfig().signMethod
    req["txnType"] = "00"
    req["txnSubType"] = "00"
    req["bizType"] = "000000"
    req["accessType"] = "0"
    req["channelType"] = "07"

    req["orderId"] = "20180320093004"
    req["merId"] = "777290058110048"
    req["txnTime"] = time_now

    # 签名示例
    req = AcpService.sign(req)
    url = SDKConfig().singleQueryUrl

    # 前台自提交表单示例
    resp = AcpService.post(req, url)
    if not AcpService.validate(resp):
        logging.error("回复报文验证失败")
        return jsonify({'status': 'error', 'error': 'not validate'})

    respCode = resp['respCode']
    if respCode == "00":
        origRespCode = resp['origRespCode']
        if origRespCode == "00":
            return jsonify({'status': 'ok', 'msg': '交易成功', 'data': resp})
        if origRespCode == "03" or origRespCode == "04" or origRespCode == "05":
            return jsonify({'status': 'pending', 'msg': '交易处理中', 'data': resp})
        else:
            return jsonify({'status': 'error', 'msg': '交易失败', 'data': resp})

    return jsonify({'status': 'error', 'msg': '应答码错误', 'data': resp})
