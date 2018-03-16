from datetime import datetime
from unionpay.SDKConfig import SDKConfig
from unionpay.AcpService import AcpService
import zipfile
import os


# 文件下载接口样例


def trade():
    req = {}

    req["version"] = SDKConfig().version
    req["encoding"] = SDKConfig().encoding
    req["signMethod"] = SDKConfig().signMethod

    req["txnType"] = "76"
    req["txnSubType"] = "01"
    req["bizType"] = "000000"
    req["accessType"] = "0"
    req["fileType"] = "00"

    req["merId"] = "700000000000001"
    req["txnTime"] = datetime.now().strftime('%Y%m%d%H%M%S')
    req["settleDate"] = "0119"

    # 签名示例
    req = AcpService.sign(req)
    url = SDKConfig().fileTransUrl

    # post示例
    resp = AcpService.post(req, url)

    result = "请求报文：" + map2str(req) + "<br>\n"
    result = result + "应答报文：" + map2str(resp) + "<br>\n"

    # 验签示例
    result = result + ("验签成功<br>\n" if AcpService.validate(resp) else "验签失败<br>\n")

    if "respCode" in resp:
        # 取应答报文里的参数的示例
        result = result + "respCode=" + resp["respCode"] + "<br>\n"
        result = result + "respMsg=" + resp["respMsg"] + "<br>\n"
        if resp["respCode"] == "00":
            dir = "./files/"  # 先建立好文件夹哦
            result += "文件保存到：" + dir + ("成功<br>\n" if AcpService.deCodeFileContent(resp, dir) else "失败<br>\n")
            result += analyzeFile(dir, resp["fileName"])
    return result


def map2str(params):
    result = ""
    for key in params.keys():
        result = result + key + "=" + params[key] + ", "
    result = result[:-2]
    return result


def analyzeFile(fileDir, fileName):
    filePath = fileDir + "/" + fileName
    if not os.path.exists(filePath):
        return False
    f = zipfile.ZipFile(filePath)
    result = ""
    for name in f.namelist():
        # 下面的代码可以保存rar里的文件，不需要的话注释掉
        ext_filename = os.path.join(fileDir, name)
        ext_dir = os.path.dirname(ext_filename)
        if not os.path.exists(ext_dir):
            os.mkdir(ext_dir, 0o777)

        with open(ext_filename, 'wb') as outfile:
            outfile.write(f.read(name))

        # 分析文件
        content = f.read(name).decode('gbk')
        data_list = None
        if name[0:3] == "INN" and name[11:14] == "ZM_":
            data_list = parseZMFile(content)
        elif name[0:3] == "INN" and name[11:15] == "ZME_":
            data_list = parseZMEFile(content)
        if data_list != None:
            result += name + "部分参数读取（读取方式请参考Form_7_2_FileTransfer的代码）:<br>\n"
            result += "<table border='1'>\n"
            result += "<tr><th>txnType</th><th>orderId</th><th>txnTime（MMDDhhmmss）</th></tr>"
            # TODO
            # 参看https: // open.unionpay.com / ajweb / help?id = 258，根据编号获取即可，例如订单号12、交易类型20。
            # 具体写代码时可能边读文件边修改数据库性能会更好，请注意自行根据parseFile中的读取方法修改。

            for dic in data_list:
                result += "<tr>\n"
                result += "<td>" + dic[20] + "</td>\n"  # txnType
                result += "<td>" + dic[12] + "</td>\n"  # orderId
                result += "<td>" + dic[5] + "</td>\n"  # txnTime不带年份
                result += "</tr>\n"
            result += "</table>\n"

    if result == "":
        result = "文件读取失败<br>\n"

    return result


def parseZMFile(fileStr):
    lengthArray = [3, 11, 11, 6, 10, 19, 12, 4, 2, 21, 2, 32, 2, 6, 10, 13, 13, 4, 15, 2, 2, 6, 2, 4, 32, 1, 21, 15, 1,
                   15, 32, 13, 13, 8, 32, 13, 13, 12, 2, 1, 131]
    return parseFile(fileStr, lengthArray)


def parseZMEFile(fileStr):
    lengthArray = [3, 11, 11, 6, 10, 19, 12, 4, 2, 2, 6, 10, 4, 12, 13, 13, 15, 15, 1, 12, 2, 135]
    return parseFile(fileStr, lengthArray)


def parseFile(fileStr, lengthArray):
    dataList = []
    for line in fileStr.replace("\r\n", "\r").replace("\r", "\n").split("\n"):
        if line == "": continue
        left_index = 0
        right_index = 0
        dataMap = {}
        for i in range(len(lengthArray)):
            right_index = left_index + lengthArray[i]
            filed = line[left_index: left_index + lengthArray[i]]
            left_index = right_index + 1
            dataMap[i + 1] = filed
        dataList.append(dataMap)
    return dataList
