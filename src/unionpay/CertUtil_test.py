import unittest
from unionpay.SDKConfig import SDKConfig
from unionpay.CertUtil import CertUtil


class TestCertUtil(unittest.TestCase):
    def setUp(self):
        self.certPath = SDKConfig().signCertPath
        self.certPassword = SDKConfig().signCertPwd
        self.certEncPath = SDKConfig().encryptCertPath
        self.certMiddlePath = SDKConfig().middleCertPath
        self.certRootPath = SDKConfig().rootCertPath
        self.certVerifyPath = SDKConfig().validateCertDir + 'verify_test.cer'

    ###################################
    # Sign Cert
    ###################################
    def test_initSignCert(self):
        cert = CertUtil.initSignCert(self.certPath, self.certPassword)
        self.assertEqual(cert.certId, "68759663125")

    def test_getSignPriKey(self):
        PriKey = CertUtil.getSignPriKey(self.certPath, self.certPassword)
        self.assertIsNotNone(PriKey)

    def test_getSignCertId(self):
        certId = CertUtil.getSignCertId(self.certPath, self.certPassword)
        self.assertEqual(certId, "68759663125")

    def test_getDecryptPriKey(self):
        PriKey = CertUtil.getDecryptPriKey(self.certPath, self.certPassword)
        self.assertIsNotNone(PriKey)

    ###################################
    # Encrypt Cert
    ###################################
    def test_initEncryptCert(self):
        cert = CertUtil.initEncryptCert(self.certEncPath)
        self.assertEqual(cert.certId, '68759622183')

    def test_getEncryptKey(self):
        pub_key = CertUtil.getEncryptKey(self.certEncPath)
        self.assertIsNotNone(pub_key)

    def test_getEncryptCertId(self):
        certId = CertUtil.getEncryptCertId(self.certEncPath)
        self.assertEqual(certId, '68759622183')

    def test_resetEncryptCertPublicKey(self):
        CertUtil.resetEncryptCertPublicKey(self.certEncPath)

    ###################################
    # Root Cert
    ###################################
    def test_verifyAndGetVerifyCert(self):
        with open(self.certVerifyPath, 'rb') as fs:
            cert = CertUtil.verifyAndGetVerifyCert(fs.read())
            self.assertIsNotNone(cert)

    ###################################
    # Tools
    ###################################
    def test_getVerifyCertFromPath(self):
        cert = CertUtil.getVerifyCertFromPath('68759622183', SDKConfig().validateCertDir)
        self.assertIsNotNone(cert)


if __name__ == '__main__':
    unittest.main()
