#-*- encoding:utf-8 -*- 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import globals as glb
glb._init()

from werkzeug import Request as RequestBase, Response as ResponseBase, \
     LocalStack, LocalProxy, create_environ, cached_property, \
     SharedDataMiddleware

from config import app_config
from  BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import urllib
from utils.utils import utils
from route import Route
import socket # For gethostbyaddr()
import yaml

class Pybox(BaseHTTPRequestHandler):
    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        try:
            self.raw_requestline = self.rfile.readline(65537)
            if len(self.raw_requestline) > 65536:
                self.requestline = ''
                self.request_version = ''
                self.command = ''
                self.send_error(414)
                return
            if not self.raw_requestline:
                self.close_connection = 1
                return
            if not self.parse_request():
                # An error code has been sent, just exit
                return
            # if not hasattr(self, mname):
            #     self.send_error(501, "Unsupported method (%r)" % self.command)
            #     return
            self.run_route_method()
            self.wfile.flush() #actually send the response if not already done.
        except socket.timeout, e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return
    # 路由执行        
    def run_route_method(self):
        # print"in run_route_method"
        path = self.path#127.0.0.1:8000/wahaha提取出路径的后面部分
        print path
        #拆分url(也可根据拆分的url获取Get提交才数据),可以将不同的path和参数加载不同的html页面，或调用不同的方法返回不同的数据，来实现简单的网站或接口
        query = urllib.splitquery(path)
        print "query=",query
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.send_header("test","This is test!")
        self.end_headers()

        route = Route( self )
        buf = route.run()
        self.wfile.write(buf)
    @staticmethod
    def start_server(port = None):
        if port is None:
            port = app_config.get_key('Port')
        print "web server listen at port " + str(port) + "..."
        http_server = HTTPServer(('', int(port)), Pybox)#HTTPServer绑定对应的应答类ServerHTTP
        http_server.serve_forever()

# from werkzeug.wrappers import Request, Response

# @Request.application
# def application(request):
#     return Response('Hello, World!')

# if __name__ == '__main__':
#     from werkzeug.serving import run_simple
#     run_simple('localhost', 4000, application)