import urllib3
from urllib import parse
import requests
import hashlib
import base64
import json
import shutil
import logging
import rsa
import zlib

from OpenSSL import crypto
from unionpay.SDKConfig import SDKConfig
from unionpay.CertUtil import CertUtil
from unionpay.sm3 import sm3


def post(url, url_args):
    data_dict = parse.parse_qs(url_args)
    logging.debug("Post URL: " + url)

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if SDKConfig().ifValidateRemoteCert.lower() == "false":
        r = requests.post(url, data=data_dict, verify=False)
    else:
        r = requests.post(url, data=data_dict)

    if r.status_code != 200:
        logging.error("request to {} error: {}".format(url, r.status_code))
        return None

    return r.text


def createLinkString(para, sort, encode):
    linkString = ""
    keys = para.keys()
    if (sort):
        keys = sorted(keys)
    for key in keys:
        value = para[key]
        if encode:
            value = parse.quote(value)
        linkString += (key + "=" + value + "&")
    linkString = linkString[:-1]
    return linkString


def filterNoneValue(para):
    res_dict = {}
    keys = para.keys()
    for key in keys:
        value = para[key]
        if value is None or value == "":
            continue
        res_dict[key] = value
    return res_dict


def buildSignature(req_dict, signCertPath=SDKConfig().signCertPath,
                   signCertPwd=SDKConfig().signCertPwd,
                   secureKey=SDKConfig().secureKey):
    req = filterNoneValue(req_dict)
    signature = ""

    if "signMethod" not in req:
        logging.error("signMethod must not null")
        return None

    if "version" not in req:
        logging.error("version must not null")
        return None

    if "01" == req["signMethod"]:
        req["certId"] = CertUtil.getSignCertId(signCertPath, signCertPwd)

        logging.debug("=== start to sign ===")
        prestr = createLinkString(req, True, False)
        logging.debug("sorted: [" + prestr + "]")

        if "5.0.0" == req["version"]:
            prestr = sha1(prestr)
            logging.debug("sha1: [" + prestr + "]")
            logging.debug("sign cert: [" + signCertPath + "], pwd: [" + signCertPwd + "]")

            key = CertUtil.getSignPriKey(signCertPath, signCertPwd)
            signature = base64.b64encode(crypto.sign(key, prestr.encode('utf-8'), 'sha1'))
            signature = signature.decode('utf-8')
            logging.debug("signature: [" + signature + "]")

        else:
            prestr = sha256(prestr)
            logging.debug("sha256: [" + prestr + "]")
            logging.debug("sign cert: [" + signCertPath + "], pwd: [" + signCertPwd + "]")
            key = CertUtil.getSignPriKey(signCertPath, signCertPwd)
            signature = base64.b64encode(crypto.sign(key, prestr.encode('utf-8'), 'sha256'))
            signature = signature.decode('utf-8')
            logging.debug("signature: [" + signature + "]")

    elif "11" == req["signMethod"]:
        logging.debug("=== start to sign ===")
        prestr = createLinkString(req, True, False)
        logging.debug("sorted: [" + prestr + "]")

        if secureKey is None:
            logging.error("secureKey must not null")
            return None
        prestr = prestr + "&" + sha256(secureKey)
        logging.debug("before final sha256: [" + prestr + "]")
        signature = sha256(prestr)
        logging.debug("signature: [" + signature + "]")

    elif "12" == req["signMethod"]:
        logging.debug("=== start to sign ===")
        prestr = createLinkString(req, True, False)
        logging.debug("sorted: [" + prestr + "]")
        if secureKey is None:
            logging.error("secureKey must not null")
            return None
        prestr = prestr + "&" + sm3(secureKey)
        logging.debug("before final sm3: [" + prestr + "]")
        signature = sm3(prestr)
        logging.debug("signature: [" + signature + "]")

    else:
        logging.error("invalid signMethod: [" + req["signMethod"] + "]")
        return None

    logging.debug("=== end of sign ===")
    req["signature"] = signature
    return req


def paraFilter(para):
    result = {}
    for key in para.keys():
        if key == "signature" or para[key] == "":
            continue
        else:
            result[key] = para[key]
    return result


def sha1(data):
    data = data.encode('utf-8')
    return hashlib.sha1(data).hexdigest()


def sha256(data):
    data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def putKeyValueToMap(temp, isKey, key, m):
    if isKey:
        m[str(key)] = ""
    else:
        m[str(key)] = temp


def parseQString(respString):
    resp = {}
    temp = ""
    key = ""
    isKey = True
    isOpen = False
    openName = "\0"

    for curChar in respString:  # 遍历整个带解析的字符串
        if (isOpen):
            if (curChar == openName):
                isOpen = False
            temp = temp + curChar
        elif (curChar == "{"):
            isOpen = True
            openName = "}"
            temp = temp + curChar
        elif (curChar == "["):
            isOpen = True
            openName = "]"
            temp = temp + curChar
        elif (isKey and curChar == "="):
            key = temp
            temp = ""
            isKey = False
        elif (curChar == "&" and not isOpen):  # 如果读取到&分割符
            putKeyValueToMap(temp, isKey, key, resp)
            temp = ""
            isKey = True
        else:
            temp = temp + curChar

    putKeyValueToMap(temp, isKey, key, resp)
    return resp


def verify(resp):
    if "signMethod" not in resp:
        logging.error("signMethod must not null")
        return False

    if "version" not in resp:
        logging.error("version must not null")
        return False

    if "signature" not in resp:
        logging.error("signature must not null")
        return False

    signMethod = resp["signMethod"]
    version = resp["version"]
    result = False

    if "01" == signMethod:
        logging.debug("=== start to verify signature ===")

        if "5.0.0" == version:
            signature = resp.pop("signature")
            logging.debug("signature: [" + signature + "]")
            prestr = createLinkString(resp, True, False)
            logging.debug("sorted: [" + prestr + "]")
            prestr = sha1(prestr)
            logging.debug("sha1: [" + prestr + "]")
            cert = CertUtil.getVerifyCertFromPath(resp["certId"])
            if cert is None:
                logging.warning("no cert was found by certId: " + resp["certId"])
                result = False
            else:
                signature = base64.b64decode(signature)
                try:
                    crypto.verify(cert, signature, prestr.encode('utf-8'), 'sha1')
                    result = True
                except Exception:
                    result = False
        else:
            signature = resp.pop("signature")
            logging.debug("signature: [" + signature + "]")
            prestr = createLinkString(resp, True, False)
            logging.debug("sorted: [" + prestr + "]")
            prestr = sha256(prestr)
            logging.debug("sha256: [" + prestr + "]")
            cert = CertUtil.verifyAndGetVerifyCert(resp["signPubKeyCert"])
            if cert is None:
                logging.warning("no cert was found by signPubKeyCert: " + resp["signPubKeyCert"])
                result = False
            else:
                signature = base64.b64decode(signature)
                try:
                    crypto.verify(cert, signature, prestr.encode('utf-8'), 'sha256')
                    result = True
                except Exception:
                    result = False
        logging.debug("verify signature " + "succeed" if result else "fail")
        logging.debug("=== end of verify signature ===")
        return result

    elif "11" == signMethod or "12" == signMethod:
        return verifyBySecureKey(resp, SDKConfig().secureKey)
    else:
        logging.error("Error signMethod [" + signMethod + "] in validate. ")
        return False


def verifyBySecureKey(resp, secureKey):
    if "signMethod" not in resp:
        logging.error("signMethod must not null")
        return False

    if "signature" not in resp:
        logging.error("signature must not null")
        return False

    signMethod = resp["signMethod"]
    result = False

    logging.debug("=== start to verify signature ===")
    if "11" == signMethod:
        signature = resp.pop("signature")
        logging.debug("signature: [" + signature + "]")
        prestr = createLinkString(resp, True, False)
        logging.debug("sorted: [" + prestr + "]")
        beforeSha256 = prestr + "&" + sha256(secureKey)
        logging.debug("before final sha256: [" + beforeSha256 + "]")
        afterSha256 = sha256(beforeSha256)
        result = afterSha256 == signature
        if not result:
            logging.debug("after final sha256: [" + afterSha256 + "]")
    elif "12" == signMethod:
        signature = resp.pop("signature")
        logging.debug("signature: [" + signature + "]")
        prestr = createLinkString(resp, True, False)
        logging.debug("sorted: [" + prestr + "]")
        beforeSm3 = prestr + "&" + sm3(secureKey)
        logging.debug("before final sm3: [" + beforeSm3 + "]")
        afterSm3 = sm3(beforeSm3)
        result = afterSm3 == signature
        if not result:
            logging.debug("after final sha256: [" + afterSm3 + "]")
    logging.debug("verify signature " + "succeed" if result else "fail")
    logging.debug("=== end of verify signature ===")
    return result


def verifyAppResponse(jsonData):
    data = json.loads(jsonData)
    sign = data["sign"]
    data = data["data"]
    dataMap = parseQString(data)
    vCert = CertUtil.getVerifyCertFromPath(dataMap["cert_id"])
    signature = base64.b64decode(sign)
    return crypto.verify(vCert, signature, sha1(data).encode('utf-8'), 'sha1')


def createAutoFormHtml(params, reqUrl):
    result = "<html>\
<head>\
    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\
</head>\
<body>\
    <form id=\"pay_form\" name=\"pay_form\" action=\"" + reqUrl + "\" method=\"post\">"
    for key, value in params.items():
        result = result + "    <input type=\"hidden\" name=\"" + key + "\" id=\"" + key + "\" value=\"" + value + "\" />\n";
    result = result + "<input type=\"submit\"></input>\
    </form>\
</body>\
</html>"
    return result


def encryptPub(data, certPath=SDKConfig().encryptCertPath):
    rsaKey = CertUtil.getEncryptKey(certPath)
    result = rsa.encrypt(data.encode('utf-8'), rsaKey)
    result = base64.b64encode(result)
    return result.decode('utf-8')


def decryptPri(data, certPath=SDKConfig().signCertPath, certPwd=SDKConfig().signCertPwd):
    pkey = CertUtil.getDecryptPriKey(certPath, certPwd)
    data = base64.b64decode(data)
    result = rsa.decrypt(data, pkey)
    return result.decode('utf-8')


def deCodeFileContent(params, fileDirectory):
    if ("fileContent" not in params) or (params["fileContent"] is None):
        logging.error("No file content")
        return False

    logging.info("---------处理后台报文返回的文件---------")
    fileContent = params["fileContent"]
    fileContent = base64.b64decode(fileContent)
    fileContent = zlib.decompress(fileContent)

    if "fileName" not in params:
        logging.debug("文件名为空")
        fileName = "{}_{}_{}.txt".format(
            params["merId"], params["batchNo"], params["txnTime"])
    else:
        fileName = params['fileName']

    filePath = fileDirectory + fileName

    with open(filePath, 'wb') as f:
        f.write(fileContent)
        logging.info("文件位置: " + filePath)

    return True


def enCodeFileContent(path):
    with open(path, 'rb') as f:
        fileContent = f.read()

    fileContent = zlib.compress(fileContent)
    fileContent = base64.b64encode(fileContent)

    return fileContent.decode('utf-8')


def getEncryptCert(params):
    if ("encryptPubKeyCert" not in params) or ("certType" not in params):
        logging.error("encryptPubKeyCert or certType is null")
        return -1

    strCert = params["encryptPubKeyCert"]
    certType = params["certType"]

    x509Cert = crypto.load_certificate(crypto.FILETYPE_PEM, strCert)
    if "01" == certType:
        # 更新敏感信息加密公钥
        if str(x509Cert.get_serial_number()) == CertUtil.getEncryptCertId():
            return 0
        else:
            localCertPath = SDKConfig().encryptCertPath
            newLocalCertPath = genBackupName(localCertPath)
            # 将本地证书进行备份存储
            try:
                shutil.move(localCertPath, newLocalCertPath)
            except Exception as e:
                logging.error("备份旧加密证书失败: {}".format(e))
                return -1
            # 备份成功,进行新证书的存储
            try:
                with open(localCertPath, "w+") as f:
                    f.write(strCert)
            except Exception as e:
                logging.error("写入新加密证书失败: {}".format(e))
                return -1

            logging.info("save new encryptPubKeyCert success")
            CertUtil.resetEncryptCertPublicKey()
            return 1

    elif "02" == certType:
        return 0

    else:
        logging.error("unknown cerType:" + certType)
        return -1


def genBackupName(fileName):
    i = fileName.rfind(".")
    leftFileName = fileName[0: i]
    rightFileName = fileName[i + 1:]
    newFileName = leftFileName + "_backup" + "." + rightFileName
    return newFileName
