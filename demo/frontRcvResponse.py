import logging
from unionpay.AcpService import AcpService


def notify(params):
    logging.info("notify req:[" + reqStr(params) + "]")
    result = "收到通知：" + reqStr(params) + "<br>\n"
    if (AcpService.validate(params)):  # 服务器签名验证成功
        # 请在这里加上商户的业务逻辑程序代码
        # 获取通知返回参数，可参考接口文档中通知参数列表(以下仅供参考)
        respCode = params["respCode"]  # 交易状态
        if respCode == "00" or respCode == "A6":
            # 判断respCode=00、A6后，对涉及资金类的交易，请再发起查询接口查询，确定交易成功后更新数据库。
            return result + "成功"
        else:
            return result + "fail"  # 这里正常的通知不会执行到
    else:  # 服务器签名验证失败
        return result + "验签失败"


def reqStr(params):
    result = ""
    for key in params.keys():
        result = result + key + "=" + params[key] + ", "
    result = result[:-2]
    return result
