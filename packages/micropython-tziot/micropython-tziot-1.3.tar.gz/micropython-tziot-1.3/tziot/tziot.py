"""
Copyright 2021-2021 The jdh99 Authors. All rights reserved.
海萤物联网sdk
Authors: jdh99 <jdh821@163.com>
"""

import tziot.config as config
import tziot.param as param
import tziot.apply as apply
import tziot.fpipe as fpipe
import tziot.conn as conn
import tziot.parsecmp as parsecmp
import tziot.standardlayer as standardlayer
import tziot.fdcom as fdcom

import dcompy as dcom
import utzpy as utz
import _thread
import uasyncio as asyncio
import network
import time

_is_first_run = True


def call(pipe: int, dst_ia: int, rid: int, timeout: int, req: bytearray) -> (bytearray, int):
    """
    RPC同步调用
    :param pipe: 通信管道
    :param dst_ia: 目标ia地址
    :param rid: 服务号
    :param timeout: 超时时间,单位:ms.为0表示不需要应答
    :param req: 请求数据.无数据可填bytearray()或者None
    :return: 返回值是应答字节流和错误码.错误码非0表示调用失败
    """
    if param.parent.ia == utz.IA_INVALID or not param.parent.is_conn:
        return None, dcom.SYSTEM_ERROR_RX_TIMEOUT

    if pipe >= fpipe.PIPE_NET:
        pipe = param.parent.pipe
    return dcom.call(config.PROTOCOL_NUM, pipe, dst_ia, rid, timeout, req)


def register(rid: int, callback):
    """
    注册DCOM服务回调函数
    :param rid: 服务号
    :param callback: 回调函数.格式: func(req bytearray) (bytearray, int)
    :return: 返回值是应答和错误码.错误码为0表示回调成功,否则是错误码
    """
    dcom.register(config.PROTOCOL_NUM, rid, callback)


def bind_pipe_net(ia: int, pwd: str, ip: str, port: int) -> int:
    """ 绑定网络管道.绑定成功后返回管道号"""
    global _is_first_run

    if _is_first_run:
        _is_first_run = False
        _init_system()
    return fpipe.pipe_bind_net(ia, pwd, ip, port)


def _init_system():
    config.init()
    fpipe.init()
    apply.init()
    conn.init()
    parsecmp.init()
    standardlayer.init()
    fdcom.init_dcom()


def bind_pipe(ia: int, send, is_allow_send) -> int:
    """
    绑定管道.绑定成功后返回管道号
    :param ia: 设备单播地址
    :param send: 发送函数.格式:func(dst_pipe: int, data: bytearray)
    :param is_allow_send: 是否允许发送函数.格式:func() -> bool
    :return: 管道号
    """
    global _is_first_run

    if _is_first_run:
        _is_first_run = False
        _init_system()
    return fpipe.pipe_bind(ia, send, is_allow_send)


def str_to_bytearray(s: str, encoding: str = 'ascii') -> bytearray:
    """字符串转换成字节流.encoding是编码方式,默认是ascii码.如果有汉字需要选择utf-8等编码"""
    return bytearray(s.encode(encoding))


def bytearray_to_str(data: bytearray, encoding: str = 'ascii') -> str:
    """字节流转换成字符串.encoding是解码方式,默认是ascii码.如果有汉字需要选择utf-8等编码"""
    return data.decode(encoding)


def run(app):
    """运行应用程序.如果没有应用程序,app可填写None"""
    if app is not None:
        _thread.start_new_thread(app, ())
    loop = asyncio.get_event_loop()
    loop.run_forever()


def connect_wifi(ssid: str, key=None, timeout=10) -> bool:
    """
    连接wifi
    :param ssid: wifi热点名
    :param key: wifi密码.不需要密码则填None
    :param timeout: 超时时间.单位:s
    :return: 返回True表示连接成功.False是连接失败
    """
    sta_if = network.WLAN(network.STA_IF)
    if sta_if.isconnected():
        sta_if.disconnect()

    sta_if.active(True)
    sta_if.connect(ssid, key)

    count = 0
    while not sta_if.isconnected():
        if count >= timeout:
            return False
        time.sleep(1)
        count += 1
    return True
