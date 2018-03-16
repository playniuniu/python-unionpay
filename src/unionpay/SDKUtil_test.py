import unittest
from urllib import parse
import zlib
import base64
from unionpay import SDKUtil


class TestSDKUtil(unittest.TestCase):
    def setUp(self):
        pass

    def _test_Post(self):
        url = "https://gateway.test.95516.com/gateway/api/queryTrans.do"
        data = "version=5.0.0&encoding=utf-8&signMethod=01&txnType=00&txnSubType=00&bizType=000000&accessType=0&channelType=07&orderId=20160417090108&merId=777290058110097&txnTime=20160417090108&certId=68759663125&signature=Hyz31eHxPhXnXWSsquV1p%2FI%2BtD4pM9A5OQkPw4xO7Ntrb58eP8xdIMLvtaj%2BeqywBuw7g6w49RoukrQIStYzZ43pQanw5%2F%2F3xzmnn50PiJPYTbxCXd6by1Ct5QVpVbYRdF12ioJvxgoEPhT9kfdQ8lrOikFlInyDR3DTsVInng73lZqVpiFq21Eky0b0M46BiV94vnAtiCpZjpuD%2BycSsmljRgBUvAbrpuS6G7qZCDlRBCeXB%2B4y7%2BoWo%2F07ZFcB0pCqzxUaG822Om49m54%2B86ywUzig8mDGBZ0LbTrwvZV22zE9wlKglQkAH4iL2aZeLqL%2BY4yoaE9rFiKModfuoA%3D%3D"

        res_data = SDKUtil.post(url, data)
        parse_res = parse.parse_qs(res_data)
        if 'merId' not in parse_res:
            raise KeyError
        self.assertEqual(parse_res['merId'][0], '777290058110097')

    def test_createLinkString(self):
        a = {"transType": "01", "sysReserved": "{aaa=a&bbb=b}", "merId": "888888888888888"}
        sort_url = SDKUtil.createLinkString(a, True, False)
        self.assertEqual(sort_url, 'merId=888888888888888&sysReserved={aaa=a&bbb=b}&transType=01')
        sort_encode_url = SDKUtil.createLinkString(a, True, True)
        self.assertEqual(sort_encode_url, 'merId=888888888888888&sysReserved=%7Baaa%3Da%26bbb%3Db%7D&transType=01')

    def test_filterNoneValue(self):
        test_dict = {'a': 123, 'b': '', 'c': '456'}
        filter_dict = {'a': 123, 'c': '456'}
        self.assertDictEqual(SDKUtil.filterNoneValue(test_dict), filter_dict)

    def test_BuildSignature(self):
        req_dict = {"transType": "01", "sysReserved": "{aaa=a&bbb=b}", "merId": "888888888888888"}

        req_dict['signMethod'] = '01'
        req_dict['version'] = '5.0.0'
        sign_res = SDKUtil.buildSignature(req_dict, "../certs/acp_test_sign.pfx", "000000")

        check_sign = ('ClTZLArDgM7rE9KORsgEiCmaPo/8G4xg4SrTJAET9xcymexSSlYDjQMIfhvZ0qgtYzlI'
                      '+fV/5/ZKbnpJD0R2qOsvhT9e+Xb2wZzJFeYJVDNBqlZZLXUcB2kU0ut2fKdHCAcWApoGA1Ks0d5s'
                      '/CA4sp8ZdaejatHVuKnTHa8rgLallX9Gekxul538WtZoU4n4RNBEe2ythZnj5eUa'
                      'VFYdzzSQ6pAnlYfKzhby3p5/YFdZZHcYDbdrkQjS+ewgf6wQfFGu5X07BznqYjf6I6x25jPgidg6'
                      'OHE0m25uv2ksyZuEKwSM/WWUYOc0q/TF7XMhN1lpm3VZN8ePvIK5NPHPaA==')

        self.assertEqual(sign_res['signature'], check_sign)

        req_dict['signMethod'] = '01'
        req_dict['version'] = '5.1.0'
        sign_res = SDKUtil.buildSignature(req_dict, "../certs/acp_test_sign.pfx", "000000")
        check_sign = ('nCDm51Cju6CG0kvYNKJI0hlMMlPqKn2IftnBFWkeNftrNKxczLB2kAyASv6'
                      'Tr3PeOauGvgzv9KEpBBkZY1f7nhOuv/WfZVEHt4oWmxcd24TrEZ5dDtQb4t'
                      'amzUszl0p+TXDW4tqxzbwjjQ++acYtthLadhG44Cce0Lnno7LWIKDh1Fe6w'
                      'sMMAEXsJwZX7nIcskeymOTF98FopOt/RFsIHSJ4Z0UuqZ6gEOjPzSbqTgm2'
                      'SeAMFMmxMToUmY+doQHla5GNkI4VJox10LIZBlA8SRTwL6qt3kdHhFyP7mR'
                      'w2WbjzUA9kuqPtFhC7ucKJ5tFG1YmbnX5upg0Mg9h2UlofQ==')

        self.assertEqual(sign_res['signature'], check_sign)

        req_dict['signMethod'] = '11'
        sign_res = SDKUtil.buildSignature(req_dict, "../certs/acp_test_sign.pfx", "000000")
        check_sign = 'bda8e705fe9d67022f71e8ca14752abc402368ed142b3bc71837ac9dec99c18e'
        self.assertEqual(sign_res['signature'], check_sign)

        req_dict['signMethod'] = '12'
        sign_res = SDKUtil.buildSignature(req_dict, "../certs/acp_test_sign.pfx", "000000")
        check_sign = 'e3d147d4d1b835a3453c7f900acf8ad4370ebea0e750452a4a02db43c398af81'
        self.assertEqual(sign_res['signature'], check_sign)

    def test_paraFilter(self):
        test_dict = {"signature": "111", "transType": "01", "sysReserved": "{aaa=a&bbb=b}", "merId": "888888888888888"}
        check_dict = {"transType": "01", "sysReserved": "{aaa=a&bbb=b}", "merId": "888888888888888"}
        self.assertDictEqual(SDKUtil.paraFilter(test_dict), check_dict)

    def test_sha1(self):
        pass

    def test_sha256(self):
        pass

    def test_putKeyValueToMap(self):
        pass

    def test_parseQString(self):
        respString = ('accessType=0&bizType=000000&certId=68759585097&'
                      'encoding=utf-8&merId=777290058110097&orderId=20'
                      '160417104527&respCode=34&respMsg=查无此交易[26000'
                      '00]&signMethod=01&txnSubType=00&txnTime=20160417'
                      '104527&txnType=00&version=5.0.0')
        parse_dict = SDKUtil.parseQString(respString)
        check_dict = {
            'accessType': '0',
            'bizType': '000000',
            'certId': '68759585097',
            'encoding': 'utf-8',
            'merId': '777290058110097',
            'orderId': '20160417104527',
            'respCode': '34',
            'respMsg': '查无此交易[2600000]',
            'signMethod': '01',
            'txnSubType': '00',
            'txnTime': '20160417104527',
            'txnType': '00',
            'version': '5.0.0',
        }
        self.assertDictEqual(parse_dict, check_dict)

    def test_verify(self):
        # TODO : Add verify() test
        pass

    def test_verifyBySecureKey(self):
        # TODO : Add verifyBySecureKey() test
        pass

    def test_verifyAppResponse(self):
        # TODO : Add verifyAppResponse() test
        pass

    def test_createAutoFormHtml(self):
        # TODO : Add createAutoFormHtml() test
        data_dict = {
            "transType": "01",
            "sysReserved": "{aaa=a&bbb=b}",
            "merId": "888888888888888"
        }
        form_data = SDKUtil.createAutoFormHtml(data_dict, 'https://example.com')
        self.assertRegex(form_data, r'input.*hidden')

    def test_encryptPub(self):
        # TODO : Add encryptPub() test
        pass

    def test_DecryptPri(self):
        data = ('BxqNdggaUsjTf8BEDCLvUy/SdjhC5w49rrZ0lMvQbB'
                '4qXjcTnskImSxY8y1SbhI6lKZKbFKPhT8B2rFNuRdu'
                'DSglhLA/yvUUy7eTndBhELOtgxUL0Oddbw/cWD3HM8'
                'UIgvMc4300H2SJDJnWacjSqLbt5aedV9Ar2GefxUhJ'
                'N/UNnz6thbWsQGwjNL1+zMYf0ePC+M7qYVToPkKXxe'
                'oNaEj1Y3ibQYHsnIx3mXUhDPN1rink/AjAbeNkTXCO'
                'tPGjksKAtD52s9D0DVeSCFH8iA2cye/0MRodSDERpO'
                'bldnRoksZBeQ5p3qx0i++T57706TRAdk0vwcsaYiNe'
                'Yc+Qew==')
        check_data = 'phoneNo=18100000000'
        self.assertEqual(SDKUtil.decryptPri(data), check_data)

    def _test_deCodeFileContent(self):
        # Generate file content
        file_content = "test_data".encode('utf-8')
        file_content = zlib.compress(file_content)
        file_content = base64.b64encode(file_content)
        file_content = file_content.decode('utf-8')

        data_dict = {
            "merId": "888888888888888",
            "batchNo": "123456",
            "txnTime": 1234323223,
            "fileName": "test.txt",
            "fileContent": file_content,
        }
        SDKUtil.deCodeFileContent(data_dict, "../files/")

    def test_enCodeFileContent(self):
        file_content = "test_data".encode('utf-8')
        file_content = zlib.compress(file_content)
        file_content = base64.b64encode(file_content)
        file_content = file_content.decode('utf-8')

        data_dict = {
            "merId": "888888888888888",
            "batchNo": "123456",
            "txnTime": 1234323223,
            "fileName": "test.txt",
            "fileContent": file_content,
        }
        SDKUtil.deCodeFileContent(data_dict, "../files/")
        encode_str = SDKUtil.enCodeFileContent("../files/test.txt")
        self.assertEqual(encode_str, "eJwrSS0uiU9JLEkEABL5A7o=")

    def test_getEncryptCert(self):
        # TODO : add getEncryptCert() test
        pass


if __name__ == '__main__':
    unittest.main()
