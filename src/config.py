#-*- encoding:utf-8 -*- 
import sys
import os
import globals as glb
import yaml
import copy
import pdb 
import urllib2
import re
from utils.utils import split_by_sep

config_obj = {}

### Methods defined
def method_a():
    print 'in method a'
# 深度合并字典
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
        dict1[key] = dict2[key]
# 重新调入config
def reload_config():
    app_config = Config()
    return app_config
# 解析路由配置key值
def analy_r_key( r_key):
    # re.findall(r"a(.+?)b", str)
    ret = {}
    keys = keystr_analy( r_key )

    methods = []
    methods.extend( keys['methods'] )

    refsKeys = trans_route_key( keys['route'] )
    # print keys['methods']
    # print refsKeys
    # print methods
    # print refsKeys['methods']
    #keys = trans_route_key(s)
    methods.extend( refsKeys['methods'] )
    ret['route'] = refsKeys['route']
    ret['methods'] = methods
    # print ret
    return ret
# 解析路由字符串
def keystr_analy( keystr ):
    ret = {} 
    s = keystr.replace(' ' , '')
    methods = re.findall(r"\[(.+?)\]" , keystr)
    s = s.split(',')
    s = s[0]

    if( len(methods) > 0):
        methods = methods[0]
    else:
        methods = ""
    methods = split_by_sep( methods , ',')
    # 转换成大写
    for i,m in enumerate(methods):
        methods[i] = m.upper()

    s = split_by_sep (s , '|')

    for i,v in enumerate(s):
        if cmp(v,'/') != 0 :
            s[i] = v.strip('/')

    ret['route'] = s
    ret['methods'] = methods

    # print ret
    return ret
# 解析路由list
def trans_route_key( rt = [] ):
    ret = {}
    ret.setdefault( 'route' , [] )
    ret.setdefault( 'methods' , [] )
    
    for v in rt:
        if "#" in v:
            tmp = split_by_sep( v , '#')
            if cmp( tmp[0], "ref") == 0:
                routes = config_obj['Routes']
                for k in routes:
                    ro = analy_r_value( routes[k] )
                    if ro.has_key('ref') and cmp( ro['ref'], tmp[1]) == 0 :
                        t = keystr_analy( k )
                        ret['route'].extend( t['route'] )
                        ret['methods'].extend( t['methods'] )
                        break
            # 有待定义
            else:
                ret['route'].extend( [v] )
        else:
            ret['route'].extend( [v] )

    return ret
# 解析路由配置信息
def analy_r_value( value ):
    ret = {}
    tret = {}
    if isinstance( value , str):
        value = value.replace(' ','')
        value = split_by_sep( value , '|')
        for v in value:
            tmp = split_by_sep( v , ':')
            tmp = tmp[0:2]
            tret[tmp[0]] = tmp[1]
    else:
        tret = copy.deepcopy( value )
    # print ret
    for k in tret:
        if k in ['where']:
            t_v = split_by_sep( tret[k] , "@" )
            if len(t_v)>1:
                ret['entry'] = t_v[0]
                ret['controller'] = t_v[1]
            else:
                ret['entry'] = 'index'
                ret['controller'] = t_v[0]
            
            pass
        else:
            ret[k] = tret[k]

    if ret.has_key('controller'):
        defs = re.findall(r"\{(.+?)\}" , ret['controller'])
        for k in defs:
            ori_defs = app_config.get_key('Defined')
            if ori_defs.has_key( k ):
                ret['controller'] = ret['controller'].replace('{'+k+'}' , ori_defs[k] + '\\')
        # ret['controller']
    return ret
# 解析path
def analy_path_str( pathstr ):
    ret = []
    if cmp( pathstr , '/') == 0:
        ret = ['/']
    else:
        tstr = pathstr.strip('/')
        ret = split_by_sep( tstr , '/')
    return ret

#class defined
class Config(object):
    def __init__(self):
        print 'loading config...'
        self._config = {}
        configFile = glb.get_value('config_file')
        approot = glb.get_value('app_root')

        try:
            conf = open(os.path.join( approot , configFile ))
            conf = yaml.safe_load(conf)
        except:
            print "Can't find config file:" + configFile
            return

        tmp = {}
        for key in conf:
            if key != 'Includes':
                config_obj[ key ] = copy.deepcopy(conf[key])

        # print config_obj
        # 合并include配置项
        if conf.has_key('Includes'):
            for fl in conf['Includes']:
                try:
                    tmp = open(os.path.join( approot , fl ))
                    tmp = yaml.safe_load(tmp)
                except:
                    print "Can't find config file:" + fl
                    return
                self.include_config(tmp)
        # print '===================='
        # print config_obj
        # print '===================='
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

    def get_key( self , key):
        if config_obj.has_key(key):
            return copy.deepcopy(config_obj[key])
        return None

    def route_config_by_request( self , request):
        path = request['path']
        path = path.replace(' ','')
        path = path.strip('/')

        print request

        routes = config_obj['Routes']
        mocks = config_obj['Mockroute']
        proxys = config_obj['Proxys']
        # 找出route mapping
        if proxys:
            for k in proxys:
                ro = analy_r_key( k )
                ro['value'] = analy_r_value( proxys[k] )
                if self.mapping_check( request , ro):
                    print 'in PROXYS:', ro
                    return ro

        if mocks:
            for k in mocks:
                ro = analy_r_key( k )
                ro['value'] = analy_r_value( mocks[k] )
                if self.mapping_check( request , ro):
                    print 'in MOCKS:', ro
                    return  ro

        if routes:
            for k in routes:
                ro = analy_r_key( k )
                ro['value'] = analy_r_value( routes[k] )
                if self.mapping_check( request , ro):
                    print 'in ROUTES:', ro
                    return ro

        # print routes
        # print mocks
        # print proxys
        return None
    
    def mapping_check( self , req ,  ro ):
        path = analy_path_str(req['path'])
        route = ro['route']
        ret = False

        for index , r in enumerate(route):
            is_r = True
            t_path = analy_path_str( r )
            if len(t_path) == len(path):
                for i , t_v in enumerate(path):
                    if cmp( t_v , t_path[i]) != 0:
                        if '{' not in t_path[i] :
                            is_r = False
                            break
            else :
                is_r = False

            if is_r:
                ret = True
                break

        if req['command'].upper() not in ro['methods']:
            if len(ro['methods']) == 0 or 'ALL' in ro['methods']:
                pass
            else:
                ret = False

        return ret
        
#end class

app_config = Config()
