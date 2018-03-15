from datetime import datetime
from unionpay.SDKConfig import SDKConfig
from unionpay.AcpService import AcpService


# 包含样例：签名、验签

def getDemoHtml():
    req = {}

    req["version"] = SDKConfig().version
    req["encoding"] = SDKConfig().encoding
    req["signMethod"] = SDKConfig().signMethod

    req["frontUrl"] = SDKConfig().frontUrl
    req["backUrl"] = SDKConfig().backUrl

    req["txnType"] = "01"
    req["txnSubType"] = "01"
    req["bizType"] = "000201"
    req["channelType"] = "07"
    req["currencyCode"] = "156"
    req["txnAmt"] = "1000"

    req["merId"] = "777290058110048"
    req["orderId"] = datetime.now().strftime('%Y%m%d%H%M%S')
    req["txnTime"] = datetime.now().strftime('%Y%m%d%H%M%S')
    req["accessType"] = "0"

    # 签名示例
    AcpService.sign(req)
    url = SDKConfig().frontTransUrl

    # 前台自提交表单示例
    resp = AcpService.createAutoFormHtml(req, url)

    return resp
