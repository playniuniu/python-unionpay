from datetime import datetime
from unionpay.SDKConfig import SDKConfig
from unionpay.AcpService import AcpService


# 批量交易样例，此处样例为批量代付

def trade():
    req = {}

    req["version"] = SDKConfig().version
    req["encoding"] = SDKConfig().encoding
    req["signMethod"] = SDKConfig().signMethod

    req["txnType"] = "22"
    req["txnSubType"] = "03"
    req["bizType"] = "000401"
    req["accessType"] = "0"
    req["channelType"] = "07"

    req["merId"] = "777290058110097"
    req["txnTime"] = datetime.now().strftime('%Y%m%d%H%M%S')
    req["batchNo"] = "0001"

    # 签名示例
    AcpService.sign(req)
    url = SDKConfig().batchTransUrl

    # post示例
    resp = AcpService.post(req, url)

    result = "请求报文：" + map2str(req) + "<br>\n"
    result += "应答报文：" + map2str(resp) + "<br>\n"

    # 验签示例
    result += ("验签成功<br>\n" if AcpService.validate(resp) else "验签失败<br>\n")

    if "respCode" in resp:
        # 取应答报文里的参数的示例
        result += "respCode=" + resp["respCode"] + "<br>\n"
        result += "respMsg=" + resp["respMsg"] + "<br>\n"
        if resp["respCode"] == "00":
            path = "./files/"  # 先建立好文件夹哦
            result += "文件保存到：" \
                      + path + ("成功<br>\n" if AcpService.deCodeFileContent(resp, path) else "失败<br>\n")

    return result


def map2str(params):
    result = ""
    for key in params.keys():
        result = result + key + "=" + params[key] + ", "
    result = result[:-2]
    return result
