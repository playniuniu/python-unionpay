import base64
from unionpay import SDKUtil
from unionpay.SDKConfig import SDKConfig
from unionpay.CertUtil import CertUtil


class AcpService():

    @staticmethod
    def sign(req, certPath=SDKConfig().signCertPath, certPwd=SDKConfig().signCertPwd):
        '''
        签名，证书路径和密码从配置文件读
        '''
        return SDKUtil.buildSignature(req, certPath, certPwd)

    @staticmethod
    def signByCertInfo(req, certPath, certPwd):
        '''
        签名，证书路径和密码从配置文件读
        '''
        return SDKUtil.buildSignature(req, certPath, certPwd)

    @staticmethod
    def signBySecureKey(req, secureKey):
        '''
        签名，证书路径和密码从配置文件读
        '''
        return SDKUtil.buildSignature(req, secureKey=secureKey)

    @staticmethod
    def validate(resp):
        '''
        验签
        '''
        return SDKUtil.verify(resp)

    @staticmethod
    def validateBySecureKey(resp, secureKey):
        '''
        验签
        '''
        return SDKUtil.verifyBySecureKey(resp, secureKey)

    @staticmethod
    def validateAppResponse(jsonData):
        '''
        此方法已弃用。控件返回信息请在手机端验证。
        对控件支付成功返回的结果信息中data域进行验签
        '''
        return SDKUtil.verifyAppResponse(jsonData)

    @staticmethod
    def post(params, url):
        content = SDKUtil.createLinkString(params, False, True)
        respString = SDKUtil.post(url, content)
        resp = SDKUtil.parseQString(respString)
        return resp

    @staticmethod
    def createAutoFormHtml(params, reqUrl):
        return SDKUtil.createAutoFormHtml(params, reqUrl)

    @staticmethod
    def getCustomerInfo(customerInfo):
        if customerInfo == None or customerInfo.length == 0:
            return ""
        b64_str = "{" + SDKUtil.createLinkString(customerInfo, False, False) + "}"
        b64_data = base64.b64encode(b64_str.encode('utf-8'))
        return b64_data.decode('utf-8')

    @staticmethod
    def getCustomerInfoWithEncrypt(customerInfo):
        '''
        加密时使用此方法
        '''
        if customerInfo is None or len(customerInfo) == 0:
            return ""

        encryptedInfo = {}
        for key in customerInfo.keys():
            if key == 'phoneNo' or key == 'cvn2' or key == 'expired':
                encryptedInfo[key] = customerInfo[key]

        del customerInfo['phoneNo']
        del customerInfo['cvn2']
        del customerInfo['expired']

        if len(encryptedInfo):
            encryptedInfo = SDKUtil.createLinkString(encryptedInfo, False, False)
            encryptedInfo = AcpService.encryptData(encryptedInfo, SDKConfig().encryptCertPath)
            customerInfo["encryptedInfo"] = encryptedInfo

        b64_str = "{" + SDKUtil.createLinkString(customerInfo, False, False) + "}"
        b64_data = base64.b64encode(b64_str.encode('utf-8'))
        return b64_data.decode('utf-8')

    @staticmethod
    def parseCustomerInfo(customerInfostr, certPath=SDKConfig().signCertPath, certPwd=SDKConfig().signCertPwd):
        '''
        解析customerInfo。
        为方便处理，encryptedInfo下面的信息也均转换为customerInfo子域一样方式处理，
        '''
        customerInfostr = base64.b64decode(customerInfostr)
        customerInfostr = customerInfostr[1:len(customerInfostr) - 1]
        customerInfo = SDKUtil.parseQString(customerInfostr)
        if 'encryptedInfo' in customerInfo:
            encryptedInfoStr = customerInfo.pop("encryptedInfo")
            encryptedInfoStr = AcpService.decryptData(encryptedInfoStr, certPath, certPwd)
            encryptedInfo = SDKUtil.parseQString(encryptedInfoStr)
            for k, v in encryptedInfo.items():
                customerInfo[k] = v
        return customerInfo

    @staticmethod
    def getEncryptCertId():
        return CertUtil.getEncryptCertId()

    @staticmethod
    def encryptData(data, certPath=SDKConfig().encryptCertPath):
        return SDKUtil.encryptPub(data, certPath)

    @staticmethod
    def decryptData(data, certPath=SDKConfig().signCertPath, certPwd=SDKConfig().signCertPwd):
        return SDKUtil.decryptPri(data, certPath, certPwd)

    @staticmethod
    def deCodeFileContent(params, fileDirectory):
        return SDKUtil.deCodeFileContent(params, fileDirectory)

    @staticmethod
    def enCodeFileContent(path):
        return SDKUtil.enCodeFileContent(path)

    @staticmethod
    def updateEncryptCert(params):
        return SDKUtil.getEncryptCert(params)
