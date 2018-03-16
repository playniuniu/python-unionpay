import logging
import base64
from pathlib import Path
import rsa
from pyasn1.codec.der import decoder
from OpenSSL import crypto
from unionpay.SDKConfig import SDKConfig


class Cert():
    certId = None
    key = None
    cert = None


class CertUtil():
    __signCerts = {}
    __encryptCert = {}
    __verifyCerts = {}  # 5.0.0验签证书，key是certId
    __verifyCerts5_1_0 = {}  # 5.1.0验签证书，key是base64的证书内容
    __x509Store = None

    ###################################
    # Sign Cert
    ###################################
    @staticmethod
    def initSignCert(certPath, certPwd):
        if certPath is None or certPwd is None:
            logging.error("signCertPath or signCertPwd is none, exit initSignCert")
            return None

        logging.info("读取签名证书 ...")
        with open(certPath, 'rb') as fs:
            pkcs12 = crypto.load_pkcs12(fs.read(), certPwd.encode('ascii'))

        if pkcs12 is None:
            logging.error("load pkcs12 error")
            return None

        pkey = pkcs12.get_privatekey()
        pkey = CertUtil.pkcs8_to_pkcs1(pkey)
        pkey = rsa.PrivateKey.load_pkcs1(pkey, 'PEM')

        cert = Cert()
        cert.key = pkey
        cert.certId = str(pkcs12.get_certificate().get_serial_number())
        cert.cert = pkcs12.get_privatekey()
        CertUtil.__signCerts[certPath] = cert
        logging.info("签名证书读取成功, 序列号: " + cert.certId)
        return cert

    @staticmethod
    def getSignPriKey(certPath=SDKConfig().signCertPath, certPwd=SDKConfig().signCertPwd):
        if certPath not in CertUtil.__signCerts:
            CertUtil.initSignCert(certPath, certPwd)
        return CertUtil.__signCerts[certPath].cert

    @staticmethod
    def getSignCertId(certPath=SDKConfig().signCertPath, certPwd=SDKConfig().signCertPwd):
        if certPath not in CertUtil.__signCerts:
            CertUtil.initSignCert(certPath, certPwd)
        return CertUtil.__signCerts[certPath].certId

    @staticmethod
    def getDecryptPriKey(certPath=SDKConfig().signCertPath, certPwd=SDKConfig().signCertPwd):
        if certPath not in CertUtil.__signCerts:
            CertUtil.initSignCert(certPath, certPwd)
        return CertUtil.__signCerts[certPath].key

    ###################################
    # Encrypt Cert
    ###################################
    @staticmethod
    def initEncryptCert(certPath=SDKConfig().encryptCertPath):
        if certPath is None:
            logging.info("encryptCertPath is none, exit initEncryptCert")
            return None

        logging.info("读取加密证书 ...")

        with open(certPath, 'rb') as fs:
            c = crypto.load_certificate(crypto.FILETYPE_PEM, fs.read())

        pkey = crypto.dump_publickey(crypto.FILETYPE_PEM, c.get_pubkey())
        cert = Cert()
        cert.cert = rsa.PublicKey.load_pkcs1_openssl_pem(pkey)
        cert.certId = str(c.get_serial_number())
        CertUtil.__encryptCert[certPath] = cert
        logging.info("加密证书读取成功, 序列号: " + cert.certId)
        return cert

    @staticmethod
    def getEncryptKey(certPath=SDKConfig().encryptCertPath):
        if certPath not in CertUtil.__encryptCert:
            CertUtil.initEncryptCert(certPath)
        return CertUtil.__encryptCert[certPath].cert

    @staticmethod
    def getEncryptCertId(certPath=SDKConfig().encryptCertPath):
        if certPath not in CertUtil.__encryptCert:
            CertUtil.initEncryptCert(certPath)
        return CertUtil.__encryptCert[certPath].certId

    @staticmethod
    def resetEncryptCertPublicKey(certPath=SDKConfig().encryptCertPath):
        CertUtil.__encryptCert = {}
        CertUtil.initEncryptCert(certPath)

    ###################################
    # Root Cert
    ###################################
    @staticmethod
    def initRootCert(middleCertPath, rootCertPath):
        if CertUtil.__x509Store is not None:
            return

        if middleCertPath is None or rootCertPath is None:
            logging.error("rootCertPath or middleCertPath is none, exit initRootCert")
            return

        logging.debug("Start initRootCert")

        with open(middleCertPath, 'rb') as fs:
            middleCert = crypto.load_certificate(crypto.FILETYPE_PEM, fs.read())

        with open(rootCertPath, 'rb') as fs:
            rootCert = crypto.load_certificate(crypto.FILETYPE_PEM, fs.read())

        CertUtil.__x509Store = crypto.X509Store()
        CertUtil.__x509Store.add_cert(rootCert)
        CertUtil.__x509Store.add_cert(middleCert)
        logging.debug("initRootCert succeed")

    @staticmethod
    def verifyAndGetVerifyCert(certBase64String):
        if certBase64String in CertUtil.__verifyCerts5_1_0:
            return CertUtil.__verifyCerts5_1_0[certBase64String]

        if SDKConfig().middleCertPath is None or SDKConfig().rootCertPath is None:
            logging.error("rootCertPath or middleCertPath is none, exit initRootCert")
            return None

        if CertUtil.__x509Store is None:
            CertUtil.initRootCert(SDKConfig().middleCertPath, SDKConfig().rootCertPath)

        x509Cert = crypto.load_certificate(crypto.FILETYPE_PEM, certBase64String)

        if x509Cert.has_expired():
            logging.error("signPubKeyCert has expired")
            return None

        cn = CertUtil.getIdentitiesFromCertficate(x509Cert)
        if cn is None:
            logging.error('get identities error')
            return None

        UNIONPAY_CNNAME = "中国银联股份有限公司"
        if SDKConfig().ifValidateCNName.lower() != "false":
            if UNIONPAY_CNNAME != cn:
                logging.error("cer owner is not CUP:" + cn)
                return None
        elif UNIONPAY_CNNAME != cn and cn != "00040000:SIGN":  # 测试环境目前是00040000:SIGN
            logging.error("cer owner is not CUP:" + cn)
            return None

        try:
            x509StoreContext = crypto.X509StoreContext(CertUtil.__x509Store, x509Cert)
            x509StoreContext.verify_certificate()
            CertUtil.__verifyCerts5_1_0[certBase64String] = x509Cert
            return x509Cert
        except Exception:
            logging.info("validate signPubKeyCert by rootCert failed")
            return None

    @staticmethod
    def getIdentitiesFromCertficate(x509Cert):
        cpnts = x509Cert.get_subject().get_components()
        for cpnt in cpnts:
            key = cpnt[0].decode('utf-8')
            value = cpnt[1].decode('utf-8')
            if key == "CN":
                ss = value.split("@")
                if ss is not None and len(ss) > 2:
                    return ss[2]
        return None

    ###################################
    # Tools
    ###################################
    @staticmethod
    def initVerifyCerts(certDir=SDKConfig().validateCertDir):
        logging.info("读取验签证书文件夹下所有 cer 文件 ...")
        cert_path = Path(certDir)
        cert_files = list(cert_path.glob('**/*.cer'))

        if len(cert_files) == 0:
            logging.info("请确定 " + certDir + " 路径下是否存在 cer 文件")
            return

        for file_path in cert_files:
            try:
                with open(file_path, 'rb') as fs:
                    fCert = crypto.load_certificate(crypto.FILETYPE_PEM, fs.read())
                cert = Cert()
                cert.certId = str(fCert.get_serial_number())
                cert.cert = fCert
                CertUtil.__verifyCerts[cert.certId] = cert
                logging.info(file_path.name + " 读取成功, 序列号: " + cert.certId)

            except Exception as e:
                logging.error(file_path.name + " 读取失败, " + str(e))
                continue

    @staticmethod
    def getVerifyCertFromPath(certId, certDir=SDKConfig().validateCertDir):
        if len(CertUtil.__verifyCerts) == 0:
            CertUtil.initVerifyCerts(certDir)
        if len(CertUtil.__verifyCerts) == 0:
            logging.info("未读取到任何证书")
            return None
        if certId in CertUtil.__verifyCerts:
            return CertUtil.__verifyCerts[certId].cert
        else:
            logging.info("未匹配到序列号为 " + certId + " 的证书")
            return None

    @staticmethod
    def pkcs8_to_pkcs1(pkey):
        '''
        pkcs8 -> pkcs1 transfer

        :param pkey: 
        :return: pkey
        '''
        pkey = crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey).decode('ascii')
        pkey = pkey.replace("-----BEGIN PRIVATE KEY-----", "") \
            .replace("-----END PRIVATE KEY-----", "") \
            .replace("\n", "")
        pkey = base64.b64decode(pkey)
        pkey = base64.b64encode(decoder.decode(pkey)[0].getComponentByPosition(2)._value)
        pkey = "-----BEGIN RSA PRIVATE KEY-----\n" + pkey.decode('ascii') + "\n-----END RSA PRIVATE KEY-----"
        return pkey.encode('ascii')
