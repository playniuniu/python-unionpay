import unittest
from unionpay.CertUtil import CertUtil


class TestCertUtil(unittest.TestCase):
    def setUp(self):
        self.certPath = '../certs/acp_test_sign.pfx'
        self.certEncPath = '../certs/acp_test_enc.cer'
        self.certMiddlePath = '../certs/acp_test_middle.cer'
        self.certRootPath = '../certs/acp_test_root.cer'

    ###################################
    # Sign Cert
    ###################################
    def test_initSignCert(self):
        cert = CertUtil.initSignCert(self.certPath, '000000')
        self.assertEqual(cert.certId, "68759663125")

    def test_getSignPriKey(self):
        PriKey = CertUtil.getSignPriKey(self.certPath, '000000')
        self.assertIsNotNone(PriKey)

    def test_getSignCertId(self):
        certId = CertUtil.getSignCertId(self.certPath, '000000')
        self.assertEqual(certId, "68759663125")

    def test_getDecryptPriKey(self):
        PriKey = CertUtil.getDecryptPriKey(self.certPath, '000000')
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
        with open('../certs/verify_test.cer', 'rb') as fs:
            cert = CertUtil.verifyAndGetVerifyCert(fs.read())
            self.assertIsNotNone(cert)

    ###################################
    # Tools
    ###################################
    def test_getVerifyCertFromPath(self):
        cert = CertUtil.getVerifyCertFromPath('68759622183', '../certs/')
        self.assertIsNotNone(cert)


if __name__ == '__main__':
    unittest.main()
