# Python3 Unionpay SDK - Python3 银联SDK


## 说明

本项目是银联 SDK 的 Python3 非官方实现，参考了银联论坛中 Python2 的实现，原代码可以从[这里](https://open.unionpay.com/ajweb/help/faq/list?id=38&level=0&from=0)下载。

## 运行 

Docker 方式

```bash
docker run -d -p 8000:8000 playniuniu/unionpay
```

Python3 方式

```bash
cd src
mkdir files
pip3 install requirements.txt
python3 debug.py
```

## 测试

由于官方没有单元测试，所以本项目只按照基本要求，做了一定量的测试，没有覆盖全部函数。测试方法如下:

```bash
cd src/
python3 -m unittest unionpay/*_test.py
```

## Pycharm

如果使用 Pycharm 编辑器，请把根目录设置为 src/, 如果要在 Pycharm 中做单元测试，请使用 `unionpay/acp_sdk_test.ini` 替换 `unionpay/acp_sdk.ini`