import unittest
from unionpay.SDKConfig import SDKConfig


class TestSDKConfig(unittest.TestCase):
    def setUp(self):
        self.sdk_conf = SDKConfig()

    def test_sdk_read(self):
        self.assertRegex(self.sdk_conf.frontTransUrl, 'frontTransReq\.do')
        self.assertRegex(self.sdk_conf.backTransUrl, "backTransReq\.do")

    def test_sdk_set(self):
        with self.assertRaisesRegex(AttributeError, 'Already have attribute'):
            self.sdk_conf.frontUrl = "123"


if __name__ == '__main__':
    unittest.main()
