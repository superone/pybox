#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os

def _init():
    global _global_dict
    _global_dict = {}
    
    set_value('argvs' , sys.argv)
    set_value('config_file' , 'config.yaml')
    set_value('app_root' , os.path.abspath('.') )

def set_value(name, value):
    _global_dict[name] = value

def get_value(name, defValue=None):
    try:
        return _global_dict[name]
    except KeyError:
        return defValue