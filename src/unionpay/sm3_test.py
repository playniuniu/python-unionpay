import unittest
from unionpay.sm3 import hash_msg, sm3


class TestSM3(unittest.TestCase):
    def test_hash_msg(self):
        test_msg = hash_msg("abc")
        test_res = " ".join(["%08x" % i for i in test_msg])
        test_result = "66c7f0f4 62eeedd9 d1f2d46b dc10e4e2 4167c487 5cf2f7a2 297da02b 8f4ba8e0"
        self.assertEqual(test_res, test_result)

    def test_sm3(self):
        test_msg = sm3("abc")
        self.assertEqual(test_msg, "66c7f0f462eeedd9d1f2d46bdc10e4e24167c4875cf2f7a2297da02b8f4ba8e0")


if __name__ == '__main__':
    unittest.main()
