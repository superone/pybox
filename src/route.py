#-*- encoding:utf-8 -*- 
import urllib
from config import app_config
class Route(object):
    # request info
    requestInfo = {}

    def __init__(self , requestHandler ):
        self.requestHandler = requestHandler
        self.analytical()
        pass
    def analytical(self):
        path = self.requestHandler.path #127.0.0.1:8000/wahaha提取出路径的后面部分
        query = urllib.splitquery(path)
        self.requestInfo['path'] = path
        self.requestInfo['query'] = query
        self.requestInfo['headers'] = self.requestHandler.headers
        self.requestInfo['request_version'] = self.requestHandler.request_version
        self.requestInfo['command'] = self.requestHandler.command

        # BaseHTTPRequestHandler.path                    #包含的请求路径和GET请求的数据
        # BaseHTTPRequestHandler.command                 #请求类型GET、POST...
        # BaseHTTPRequestHandler.request_version         #请求的协议类型HTTP/1.0、HTTP/1.1
        # BaseHTTPRequestHandler.headers                 #请求的头
        # BaseHTTPRequestHandler.responses               #HTTP错误代码及对应错误信息的字典

        self.routeConf = app_config.route_config_by_request( self.requestInfo )
        pass

    def run(self):
        if not self.routeConf:
            buf = '''<!DOCTYPE HTML>
                    <html>
                    <head><title>Get page</title></head>
                    <body>
                        <h1>Can't find page.</h1>
                    </body>
                    </html>'''
        else:
            buf = '''<!DOCTYPE HTML>
                    <html>
                    <head><title>Get page</title></head>
                    <body>
                        <h1>[[info]]</h1>
                    </body>
                    </html>'''
        buf = buf.replace("[[info]]" , str(self.requestInfo['query'][0]))
        return buf