#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2020/1/15 17:16
# @Author  : HelloWorld
# @File    : threading_test.py
from multiprocessing import Process
import threading
import requests
import time


class ThreadFunc(threading.Thread):
    def __init__(self, thread_id, name, count):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.count = count

    def run(self):
        print("开始线程：" + self.name)
        self.request_url()
        print("退出线程：" + self.name)

    def request_url(self):
        url = 'http://127.0.0.1:5000/'
        success_total_num = 0
        for i in range(self.count):
            response = requests.get(url)
            if response.status_code == 200:
                success_total_num += 1

        print("%s's number of success is %s" % (self.name, success_total_num))
        print("%s's success rate is %s%%" % (self.name, success_total_num / self.count * 100))


def create_many_thread():
    thread_list = []
    for i in range(100):
        thread_obj = ThreadFunc(i, 'T-' + str(i), 100)
        thread_list.append(thread_obj)

    for obj in thread_list:
        obj.start()

    for obj in thread_list:
        obj.join()


class ProcessFunc(Process):
    def __init__(self, process_id, name, count):
        super().__init__()
        self.process_id = process_id
        self.name = name
        self.count = count

    def run(self):
        print("开始进程：" + self.name)
        self.request_url()
        print("退出进程：" + self.name)

    def request_url(self):
        url = 'http://127.0.0.1:5000/'
        success_total_num = 0
        for i in range(self.count):
            response = requests.get(url)
            if response.status_code == 200:
                success_total_num += 1


def create_many_process():
    process_list = []
    for i in range(20):
        process_obj = ProcessFunc(i, 'T-' + str(i), 100)
        process_list.append(process_obj)

    for obj in process_list:
        obj.start()

    for obj in process_list:
        obj.join()


if __name__ == '__main__':
    try:
        create_many_process()
    except Exception as e:
        print(e)