from datetime import datetime
from unionpay.SDKConfig import SDKConfig
from unionpay.AcpService import AcpService


# 包含样例：签名、加密、生成自动提交的html表单，注意涉及加密的业务上规定只能用证书方式签名，请勿使用密钥方式签名的配置文件

def getDemoHtml():
    accNo = "6226090000000048"
    customerInfo = {}
    customerInfo['phoneNo'] = '18100000000'
    customerInfo['certifTp'] = '01'
    customerInfo['certifId'] = '510265790128303'
    customerInfo['customerNm'] = '张三'
    customerInfo['cvn2'] = '248'
    customerInfo['expired'] = '1912'

    req = {}

    req["version"] = SDKConfig().version
    req["encoding"] = SDKConfig().encoding
    req["signMethod"] = SDKConfig().signMethod

    req["frontUrl"] = SDKConfig().frontUrl
    req["backUrl"] = SDKConfig().backUrl

    req["txnType"] = "79"
    req["txnSubType"] = "00"
    req["bizType"] = "000301"
    req["channelType"] = "07"

    req["merId"] = "777290058110097"
    req["orderId"] = datetime.now().strftime('%Y%m%d%H%M%S')
    req["txnTime"] = datetime.now().strftime('%Y%m%d%H%M%S')
    req["accessType"] = "0"

    # accNo、customerInfo组装示例
    req["accNo"] = AcpService.encryptData(accNo)
    req["customerInfo"] = AcpService.getCustomerInfoWithEncrypt(customerInfo)
    req["encryptCertId"] = AcpService.getEncryptCertId()

    # 签名示例
    AcpService.sign(req)
    url = SDKConfig().frontTransUrl

    # 前台自提交表单示例
    resp = AcpService.createAutoFormHtml(req, url)

    return resp
