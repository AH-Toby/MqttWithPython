#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：src 
@File    ：mqtt_subscribe.py
@Author  ：Toby
@Date    ：2023/3/6 11:33 
@Description：简单的mqtt订阅消息客户端
"""
import random

import paho.mqtt.client as mqtt


def connect_mqtt(broker, port, keep_alive, client_id):
    """
    连接mqtt代理服务器
    :param broker: 服务器地址
    :param port: 端口
    :param keep_alive:心跳时间
    :param client_id:客户端id（必须唯一）
    :return:
    """

    def on_connect(client, userdata, flag, rc):
        """
        连接回调函数
        :param client:客户端对象
        :param userdata: 用户数据
        :param flag:
        :param rc:
        :return:
        """
        if not rc:
            print("Connected to MQTT OK!")
        else:
            print(f"Failed to connect, return code {rc}\n")

    # 连接mqtt服务器，并获取连接引用
    client = mqtt.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port, keep_alive)
    return client


def subscribe(client, topic):
    """
    订阅主题，并接收消息
    :param client:
    :param topic:
    :return:
    """

    def on_message(client, userdata, msg):
        """
        订阅消息回调
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    # 订阅主题
    client.subscribe(topic)
    # 回调函数
    client.on_message = on_message


def run(broker, port, keep_alive, topic):
    """
    入口函数
    :param broker: 服务端地址
    :param port: 端口
    :param keep_alive:心跳时间
    :param topic:主题
    :return:
    """
    client_id = f'python-mqtt-{random.randint(0, 1000)}'  # 客户端id
    print(client_id)
    client = connect_mqtt(broker, port, keep_alive, client_id)
    subscribe(client, topic)
    #  运行一个线程来自动调用loop()处理网络事件, 阻塞模式
    client.loop_forever()


if __name__ == '__main__':
    broker = "test.ranye-iot.net"
    port = 1883
    keep_alive = 60
    topic = "mqtt/run/test"
    run(broker, port, keep_alive, topic)
