#!/usr/bin/python3
# -*- coding: utf-8 -*-
from config.base_setting import CSS_VERSION
import time


class CreateNewVersion(object):
    @staticmethod
    def get_version():
        # return CSS_VERSION
        return str(time.time())