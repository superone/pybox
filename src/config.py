import sys
import os
import globals as glb
import yaml

config_obj = {}

class Config(object):
    def __init__(self):
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
            #合并include配置项
            if key == 'Includes':
                for fl in conf[key]:
                    try:
                        tmp = open(os.path.join( approot , fl ))
                        tmp = yaml.load(tmp)
                        self.include_config(tmp)
                    except:
                        print "Can't find config file:" + fl
            else:
                config_obj[ key ] = conf[key]

    #获取原始配置数据
    def get_ori_config(self , key , defValue = None):
        try:
            return config_obj[key]
        except KeyError:
            return defValue

    def include_config(self , conf = {}):
        merge_disc_by_key( config_obj , conf)
#end class

### Methods defined
def merge_disc_by_key( dict1 , dict2):
    if isinstance(dict1 , dict):
        for k in dict2:
            if hasattr(dict1 , k):
                merge_disc_by_key( dict1[k] , dict2[k])
        pass

sys_config = Config()