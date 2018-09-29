#-*- encoding:utf-8 -*- 
import sys
import os
import globals as glb
import yaml
import copy
import pdb 

config_obj = {}

### Methods defined
def method_a():
    print 'in method a'

def merge_disc_by_key( dict1 , dict2 , key):
    # print key
    if isinstance(dict1 , dict):
        if dict1.has_key( key ):
            for skey in dict2[key]:
                if isinstance( dict2[key][skey] , dict):
                    merge_disc_by_key( dict1[key] , dict2[key] , skey)
                else:
                    dict1[key][skey] = dict2[key][skey]
        else:
            if not dict1.has_key(key):
                dict1.setdefault( key , '')
            dict1[key] = dict2[key]
    else:

        # dict1.setdefault( key , None)
        dict1[key] = dict2[key]


def reload_config():
    app_config = Config()
    return app_config

#class defined
class Config(object):
    def __init__(self):
        print 'loading config...'
        self._config = {}
        configFile = glb.get_value('config_file')
        approot = glb.get_value('app_root')

        try:
            conf = open(os.path.join( approot , configFile ))
            conf = yaml.load(conf)
        except:
            print "Can't find config file:" + configFile
            return

        tmp = {}
        for key in conf:
            if key != 'Includes':
                config_obj[ key ] = copy.deepcopy(conf[key])

        print config_obj
        #合并include配置项
        if conf.has_key('Includes'):
            for fl in conf['Includes']:
                try:
                    tmp = open(os.path.join( approot , fl ))
                    tmp = yaml.load(tmp)
                except:
                    print "Can't find config file:" + fl
                    return
                self.include_config(tmp)
        print '===================='
        print config_obj
        print '===================='
        print '...Done'
    #获取原始配置数据
    def get_ori_config(self , key , defValue = None):
        try:
            return config_obj[key]
        except KeyError:
            return defValue

    def include_config(self , conf = {}):
        for key in conf:
            merge_disc_by_key( config_obj , conf , key)
#end class
    
app_config = Config()
