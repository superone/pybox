import sys
import os
import globals as glb


class Config(object):
    __init__(self):
        configFile = glb.get_value('config_file')
        approot = glb.get_value('app_root')
        conf = open( os.path.join( approot , configFile ) )

        

sys_config = Config()