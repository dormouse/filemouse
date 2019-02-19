#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Name:         option.py
# Purpose:      helper for option manage
# Author:       Dormouse.Young
# Created:      2019-01-15
# LastModify    2019-01-15
# Licence:      GPL V3.0
# ---------------------------------------------------------------------------

import json
import logging
import yaml

from project_conf import DEBUG

__author__ = 'Dormouse Young'
__version__ = '0.1'



class DictClass:
    """ covert dict to class """

    def __init__(self, **op_dict):
        for k, v in op_dict.items():
            if isinstance(v, dict):
                op_dict[k] = DictClass(**v)
        self.__dict__.update(op_dict)


class Option:
    def __init__(self, option_file='conf.yaml'):
        self.log = logging.getLogger(__name__)
        if DEBUG:
            option_file = 'conf_test.yaml'
        self.option_file = option_file
        self.read()

    def read(self):
        """ read data from file """
        try:
            with open(self.option_file, 'r', encoding="utf-8") as f:
                self.to_class(yaml.load(f))
        except Exception as e:
            self.log.warning('load config file error, use default config')
            self.log.warning(e)
            self.init_default()

    def to_class(self, op_dict):
        dc = DictClass(**op_dict)
        self.__dict__.update(dc.__dict__)

    def to_dict(self, op_class):
        op_dict = {}
        op_dict.update(op_class.__dict__)
        for k, v in op_dict.items():
            if k == 'option_file':
                pass
            else:
                if isinstance(v, DictClass):
                    op_dict[k] = self.to_dict(v)
        return op_dict

    @staticmethod
    def get_default():
        globe = {
            'width': 1000,
            'height': 690,
            'x': 0,
            'y': 0
        }
        default_dict = {'globe': globe}
        return default_dict

    def save(self):
        with open(self.option_file, 'w', encoding="utf-8") as f:
            op_dict = self.to_dict(self)
            for key in ['option_file', 'log']:
                del op_dict[key]
            yaml.dump(op_dict, f, default_flow_style=False)

    def init_default(self):
        self.to_class(self.get_default())
        self.save()

