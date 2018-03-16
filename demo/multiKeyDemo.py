from datetime import datetime
from unionpay.SDKConfig import SDKConfig
from unionpay.AcpService import AcpService


# 多证书样例

def trade():
    req = {}

    req["version"] = SDKConfig().version
    req["encoding"] = SDKConfig().encoding
    req["signMethod"] = "11"

    req["txnType"] = "78"
    req["txnSubType"] = "00"
    req["bizType"] = "000301"
    req["channelType"] = "07"

    req["merId"] = "777290058110048"
    req["orderId"] = datetime.now().strftime('%Y%m%d%H%M%S')
    req["txnTime"] = datetime.now().strftime('%Y%m%d%H%M%S')
    req["accessType"] = "0"
    req["accNo"] = "6226090000000048"

    # 签名示例
    req = AcpService.signBySecureKey(req, "88888888")
    url = SDKConfig().backTransUrl

    # post示例
    resp = AcpService.post(req, url)

    result = "请求报文：" + map2str(req) + "<br>\n"
    result = result + "应答报文：" + map2str(resp) + "<br>\n"

    # 验签示例
    result = result + "验签成功<br>\n" if AcpService.validateBySecureKey(resp, "88888888") else "验签失败<br>\n"

    if "respCode" in resp:
        # 取应答报文里的参数的示例
        result = result + "respCode=" + resp["respCode"] + "<br>\n"
        result = result + "respMsg=" + resp["respMsg"] + "<br>\n"

        # 解密示例
        if "customerInfo" in resp:
            customerInfo = AcpService.parseCustomerInfo(resp["customerInfo"])
            if "phoneNo" in customerInfo:
                result = result + "phoneNo=" + customerInfo["phoneNo"] + "<br>\n"

    return result


def map2str(params):
    result = ""
    for key in params.keys():
        result = result + key + "=" + params[key] + ", "
    result = result[:-2]
    return result
