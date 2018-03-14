import logging
import pathlib
from configparser import ConfigParser


class SDKConfig():

    def __init__(self):
        current_dir = pathlib.Path(__file__).parent
        config_path = str(current_dir / "acp_sdk.ini")
        logging.debug("load conf: {}".format(config_path))
        self._read_config(config_path)

    def _read_config(self, config_path):
        config_parser = ConfigParser()
        config_parser.read(config_path, encoding='UTF-8')
        if 'acpsdk' not in config_parser:
            return
        cf = config_parser['acpsdk']

        self.frontTransUrl = cf.get("acpsdk.frontTransUrl", "").strip()
        self.backTransUrl = cf.get("acpsdk.backTransUrl", "").strip()
        self.singleQueryUrl = cf.get("acpsdk.singleQueryUrl", "").strip()
        self.batchTransUrl = cf.get("acpsdk.batchTransUrl", "").strip()
        self.fileTransUrl = cf.get("acpsdk.fileTransUrl", "").strip()
        self.appTransUrl = cf.get("acpsdk.appTransUrl", "").strip()
        self.cardTransUrl = cf.get("acpsdk.cardTransUrl", "").strip()
        self.jfFrontTransUrl = cf.get("acpsdk.jfFrontTransUrl", "").strip()
        self.jfBackTransUrl = cf.get("acpsdk.jfBackTransUrl", "").strip()
        self.jfSingleQueryUrl = cf.get("acpsdk.jfSingleQueryUrl", "").strip()
        self.jfCardTransUrl = cf.get("acpsdk.jfCardTransUrl", "").strip()
        self.jfAppTransUrl = cf.get("acpsdk.jfAppTransUrl", "").strip()
        self.qrcBackTransUrl = cf.get("acpsdk.qrcBackTransUrl", "").strip()
        self.qrcB2cIssBackTransUrl = cf.get("acpsdk.qrcB2cIssBackTransUrl", "").strip()
        self.qrcB2cMerBackTransUrl = cf.get("acpsdk.qrcB2cMerBackTransUrl", "").strip()
        self.signMethod = cf.get("acpsdk.signMethod", "").strip()
        self.version = cf.get("acpsdk.version", "").strip()
        self.ifValidateCNName = cf.get("acpsdk.ifValidateCNName", "").strip()
        self.ifValidateRemoteCert = cf.get("acpsdk.ifValidateRemoteCert", "").strip()
        self.signCertPath = cf.get("acpsdk.signCert.path", "").strip()
        self.signCertPwd = cf.get("acpsdk.signCert.pwd", "").strip()
        self.validateCertDir = cf.get("acpsdk.validateCert.dir", "").strip()
        self.encryptCertPath = cf.get("acpsdk.encryptCert.path", "").strip()
        self.rootCertPath = cf.get("acpsdk.rootCert.path", "").strip()
        self.middleCertPath = cf.get("acpsdk.middleCert.path", "").strip()
        self.frontUrl = cf.get("acpsdk.frontUrl", "").strip()
        self.backUrl = cf.get("acpsdk.backUrl", "").strip()
        self.encoding = cf.get("acpsdk.encoding", "").strip()
        self.secureKey = cf.get("acpsdk.secureKey", "").strip()

    def __setattr__(self, attr, value):
        if hasattr(self, attr):
            raise AttributeError("Already have attribute: {}".format(attr))
        super().__setattr__(attr, value)
