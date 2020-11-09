# coding:utf-8
from flask import Flask, request, abort, render_template
import hashlib
import xmltodict
import time

# 微信的token令牌
WECHAT_TOKEN = ''
app = Flask(__name__)

@app.route("/_wechat", methods=["GET", "POST"])
def wechat():
    """验证服务器地址的有效性"""
    # 开发者提交信息后，微信服务器将发送GET请求到填写的服务器地址URL上，GET请求携带四个参数:
    # signature:微信加密, signature结合了开发者填写的token参数和请求中的timestamp参数 nonce参数
    # timestamp:时间戳(chuo这是拼音)
    # nonce: 随机数
    # echostr: 随机字符串
    # 接收微信服务器发送参数
    signature = request.args.get("signature")
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")

    # 校验参数
    # 校验流程：
    # 将token、timestamp、nonce三个参数进行字典序排序
    # 将三个参数字符串拼接成一个字符串进行sha1加密
    # 开发者获得加密后的字符串可与signature对比，标识该请求来源于微信
    if not all([signature, timestamp, nonce]):
        # 抛出400错误
        abort(400)

    # 按照微信的流程计算签名
    li = [WECHAT_TOKEN, timestamp, nonce]
    # 排序
    li.sort()
    # 拼接字符串
    tmp_str = "".join(li)
    tmp_str = tmp_str.encode('utf-8')

    # 进行sha1加密, 得到正确的签名值
    sign = hashlib.sha1(tmp_str).hexdigest()

    # 将自己计算的签名值, 与请求的签名参数进行对比, 如果相同, 则证明请求来自微信
    if signature != sign:
        abort(403)
    else:
        if request.method == "GET":
            # 表示第一次接入微信服务器的验证
            echostr = request.args.get("echostr")
            # 校验echostr
            if not echostr:
                abort(400)
            return echostr

        elif request.method == "POST":
            # 表示微信服务器转发消息过来
            # 拿去xml的请求数据
            xml_str = request.data

            # 当xml_str为空时
            if not xml_str:
                abort(400)

            # 对xml字符串进行解析成字典
            xml_dict = xmltodict.parse(xml_str)
            xml_dict = xml_dict.get("xml")

            # MsgType是消息类型
            msg_type = xml_dict.get("MsgType")

            if msg_type == "text":  # 表示发送文本消息
                resp_dict = receiveText(xml_dict)
            elif msg_type == 'event':
                resp_dict = receiveEvent(xml_dict)
            else:
                resp_dict = {
                    "xml": {
                        "ToUserName": xml_dict.get("FromUserName"),
                        "FromUserName": xml_dict.get("ToUserName"),
                        "CreateTime": int(time.time()),
                        "MsgType": "text",
                        "Content": "对不起，不能识别您发的内容！"
                    }
                }
            # 将字典转换为xml字符串
            resp_xml_str = xmltodict.unparse(resp_dict)
            # 返回消息数据给微信服务器
            return resp_xml_str

def receiveText(dict):
    pass

def receiveEvent(dict):
    pass

if __name__ == '__main__':
    app.run(port=8000, debug=True)
