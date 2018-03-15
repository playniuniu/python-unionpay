from datetime import datetime
from unionpay.SDKConfig import SDKConfig
from unionpay.AcpService import AcpService


# 包含样例：签名、加密、后台post、验签、解customerInfo
# 以下样例使用的接口为无跳转产品的开通状态查询接口，后台类接口可以根据此demo修改代码，注意url参数也请根据不同接口替换
# 不同的值，具体参数如何填写请尽量参考其他语言开发包demo文件夹下的示例和注释说明。


def demoTrade():
    req = {}

    req["version"] = SDKConfig().version
    req["encoding"] = SDKConfig().encoding
    req["signMethod"] = SDKConfig().signMethod

    req["txnType"] = "95"
    req["txnSubType"] = "00"
    req["bizType"] = "000000"
    req["channelType"] = "07"
    req["accessType"] = "0"
    req["certType"] = "01"

    req["merId"] = "777290058110097"
    req["orderId"] = datetime.now().strftime('%Y%m%d%H%M%S')
    req["txnTime"] = datetime.now().strftime('%Y%m%d%H%M%S')

    # 签名示例
    AcpService.sign(req)
    url = SDKConfig().backTransUrl

    # post示例
    resp = AcpService.post(req, url)

    result = "请求报文：" + map2str(req) + "<br>\n"
    result = result + "应答报文：" + map2str(resp) + "<br>\n"

    # 验签示例
    result = result + "验签成功<br>\n" if AcpService.validate(resp) else "验签失败<br>\n"

    if "respCode" in resp:
        # 取应答报文里的参数的示例
        result = result + "respCode=" + resp["respCode"] + "<br>\n"
        result = result + "respMsg=" + resp["respMsg"] + "<br>\n"

        if resp["respCode"] == "00":
            resultCode = AcpService.updateEncryptCert(resp)
            if resultCode == 1:
                result += "加密公钥更新成功" + "<br>\n"
            elif resultCode == 0:
                result += "加密公钥无更新" + "<br>\n"
            else:
                result += "加密公钥更新失败" + "<br>\n"
    return result


def map2str(params):
    result = ""
    for key in params.keys():
        result = result + key + "=" + params[key] + ", "
    result = result[:-2]
    return result
