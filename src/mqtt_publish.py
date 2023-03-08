#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Project ：src 
@File    ：mqtt_publish.py
@Author  ：Toby
@Date    ：2023/3/6 16:50 
@Description：简单的mqtt发布消息客户端
"""
import random
import time

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


def publish(client, topic, msg):
    """
    发布消息
    :param client: 客户端对象
    :param topic: 发送主题
    :param msg: 信息
    :return:
    """
    while 1:
        # 每隔4s发送一次消息
        time.sleep(4)
        result = client.publish(topic, msg)
        status = result[0]
        if not status:
            print(f"Send '{msg}' to topic '{topic}'")
        else:
            print(f"Failed to send message to topic {topic}")


def run(broker, port, keep_alive, topic, msg):
    """
    运行入口函数
    :param broker:
    :param port:
    :param keep_alive:
    :param topic:
    :param msg:
    :return:
    """
    client_id = f'python-mqtt-pub-{random.randint(0, 1000)}'  # 客户端id不能重复
    client = connect_mqtt(broker, port, keep_alive, client_id)
    # 运行一个线程来自动调用loop()处理网络事件, 非阻塞
    client.loop_start()
    publish(client, topic, msg)


if __name__ == '__main__':
    broker = "test.ranye-iot.net"
    port = 1883
    keep_alive = 60
    topic = "mqtt/run/test"
    msg = input("请输入你想发送的内容")
    run(broker, port, keep_alive, topic, msg)
