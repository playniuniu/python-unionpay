from datetime import datetime, timedelta
from unionpay.SDKConfig import SDKConfig
from unionpay.AcpService import AcpService


def getDemoHtml():
    time_now = datetime.now().strftime('%Y%m%d%H%M%S')
    time_out = datetime.now() + timedelta(minutes=15)
    time_out = time_out.strftime('%Y%m%d%H%M%S')
    req = {}

    req["version"] = SDKConfig().version
    req["encoding"] = SDKConfig().encoding
    req["txnType"] = "01"
    req["txnSubType"] = "01"
    req["bizType"] = "000202"
    req["frontUrl"] = SDKConfig().frontUrl
    req["backUrl"] = SDKConfig().backUrl
    req["signMethod"] = SDKConfig().signMethod
    req["channelType"] = "07"
    req["accessType"] = "0"
    req["currencyCode"] = "156"

    req["merId"] = "777290058110048"
    req["orderId"] = time_now
    req["txnTime"] = time_now
    req["txnAmt"] = "1000"
    req['payTimeout'] = time_out

    # 签名示例
    req = AcpService.sign(req)
    url = SDKConfig().frontTransUrl

    # 前台自提交表单示例
    resp = AcpService.createAutoFormHtml(req, url)

    return resp
