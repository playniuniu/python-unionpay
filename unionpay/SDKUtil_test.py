import unittest
from urllib import parse
from unionpay import SDKUtil


class TestSDKUtil(unittest.TestCase):
    def setUp(self):
        pass

    def _test_post(self):
        url = "https://gateway.test.95516.com/gateway/api/queryTrans.do"
        data = "version=5.0.0&encoding=utf-8&signMethod=01&txnType=00&txnSubType=00&bizType=000000&accessType=0&channelType=07&orderId=20160417090108&merId=777290058110097&txnTime=20160417090108&certId=68759663125&signature=Hyz31eHxPhXnXWSsquV1p%2FI%2BtD4pM9A5OQkPw4xO7Ntrb58eP8xdIMLvtaj%2BeqywBuw7g6w49RoukrQIStYzZ43pQanw5%2F%2F3xzmnn50PiJPYTbxCXd6by1Ct5QVpVbYRdF12ioJvxgoEPhT9kfdQ8lrOikFlInyDR3DTsVInng73lZqVpiFq21Eky0b0M46BiV94vnAtiCpZjpuD%2BycSsmljRgBUvAbrpuS6G7qZCDlRBCeXB%2B4y7%2BoWo%2F07ZFcB0pCqzxUaG822Om49m54%2B86ywUzig8mDGBZ0LbTrwvZV22zE9wlKglQkAH4iL2aZeLqL%2BY4yoaE9rFiKModfuoA%3D%3D"

        res_data = SDKUtil.post(url, data)
        parse_res = parse.parse_qs(res_data)
        if 'merId' not in parse_res:
            raise KeyError
        self.assertEqual(parse_res['merId'][0], '777290058110097')

    def test_CreateLinkString(self):
        a = {"transType": "01", "sysReserved": "{aaa=a&bbb=b}", "merId": "888888888888888"}
        print(SDKUtil.createLinkString(a, True, True))
        print(SDKUtil.createLinkString(a, False, True))
        print(SDKUtil.createLinkString(a, True, False))

    # def test_DecryptPri(self):
    #     data = "BxqNdggaUsjTf8BEDCLvUy/SdjhC5w49rrZ0lMvQbB4qXjcTnskImSxY8y1SbhI6lKZKbFKPhT8B2rFNuRduDSglhLA/yvUUy7eTndBhELOtgxUL0Oddbw/cWD3HM8UIgvMc4300H2SJDJnWacjSqLbt5aedV9Ar2GefxUhJN/UNnz6thbWsQGwjNL1+zMYf0ePC+M7qYVToPkKXxeoNaEj1Y3ibQYHsnIx3mXUhDPN1rink/AjAbeNkTXCOtPGjksKAtD52s9D0DVeSCFH8iA2cye/0MRodSDERpObldnRoksZBeQ5p3qx0i++T57706TRAdk0vwcsaYiNeYc+Qew=="
    #     print(SDKUtil.decryptPri(data))

    #
    # def testBuildSignature():
    #     a = {"transType": "01", "sysReserved": "{aaa=a&bbb=b}", "merId": "888888888888888"}
    #     print(buildSignature(a, "d:/certs/acp_test_sign.pfx", "000000"))
    #

    # def testParaFilter():
    #     a = {"signature": "111", "transType": "01", "sysReserved": "{aaa=a&bbb=b}", "merId": "888888888888888"}
    #     print(paraFilter(a))
    #
    # def testParseQString():
    #     respString = "accessType=0&bizType=000000&certId=68759585097&encoding=utf-8&merId=777290058110097&orderId=20160417104527&respCode=34&respMsg=查无此交易[2600000]&signMethod=01&txnSubType=00&txnTime=20160417104527&txnType=00&version=5.0.0&signature=PZ+yd0zaI8EChNs+SjRZVyoVDK3ZaRhEV4NK7fHk1gmAlCezvM1RZBNwFOsux/JWFSgxSEclh6vvfqlCKjr+WC/J7Xg6GW0poDwjJE5SjAREP4zAw8/DjVWn+OqBxPX+d3WSURnmOWdq7tr8k2aigsM+o+nsmuBaWWDvvMRI7ayAhFuG/kyrEL40nlfMnCD5W9tEeK6E27IrZk+wTqN8aP/jxLZq2JYBRYIJr8kWAV3xtnB2XmulyCOqDPPtGRwGUKUk9hM609L66ceITQkbfe5nlWaTmvqWBTrhICGnYA8xfhuXOM/jcPWi+VY+Jar40+q7as4D3qZqcKkyF+6ZzA=="
    #     resp = parseQString(respString)
    #     print(resp)
    #
    # def testVerify():
    #     a = {"certId": "68759585097",
    #          "signature": "vgEL+lPX394JTxHHlcLgC/bcwMKumwb9jjsR0EE+apQm4Jcq16x65eAei2MMUZfxvTkviYupOyAEkC/97btz1/Vi9PeTAyX4AModdDXvFVmnvSu91Aen2IJzv8Q0D6wpULkAPTKU5uqxzQne7P2G/LkXFA76Jqvmln8ZwwpR9D5JvWDHj7IApq5VJkGjVwJoyOpM3qTvcP9oUr8FVgGp4mL04jxi04spJnjAVdZK5gX4Hki3eEnM4J08TDFPUcOLl7iwOgGy59C7TQhIjch0Bgz2NYykGroRsbNXXNqkYkDKlncQ9ZfADAfDtdSaE+fpBjm8NO/WUcg5L0iRP8jqlg==",
    #          "transType": "01", "sysReserved": "{aaa=a&bbb=b}", "merId": "888888888888888"}
    #     print(verify(a))


if __name__ == '__main__':
    unittest.main()
