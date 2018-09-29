#-*- encoding:utf-8 -*- 
# @explain: 实现GET方法和POST方法请求
import sys
import os
import globals as glb
glb._init()

from config import app_config
from  BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
import urllib
from utils.utils import utils
import yaml

f = open( os.path.join( os.path.abspath('.') , "route.yaml" ) )
sysconfig = yaml.load(f)
print app_config.get_ori_config('routes')
#sys.path.append(os.path.join( os.path.abspath('.') , sysconfig['webrootdir']) )
# print sys.path
# print os.path.exists( os.path.join( os.path.abspath('.') , 'wwwroot/home(r)-{}-get.py'))
# moduld = __import__('home(r)-{}-get')
#moduld = __import__('user.getinfo')

# print moduld.controller()

class Pybox(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.portt = "portt"
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()
        
        print"argv length : " + sys.argv[0]
        utils.read_config()
        print glb.get_value('argvs')

        print self.portt
    # def __init__(self ,request, client_address, server):
    #    print"init "
    def handle_one_request(self):
        """Handle a single HTTP request.

        You normally don't need to override this method; see the class
        __doc__ string for information on how to handle specific HTTP
        commands such as GET and POST.

        """
        print "handle_one_request"
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
            mname = 'do_' + self.command
            if not hasattr(self, mname):
                self.send_error(501, "Unsupported method (%r)" % self.command)
                return
            method = getattr(self, mname)
            method()
            self.wfile.flush() #actually send the response if not already done.
        except socket.timeout, e:
            #a read or a write timed out.  Discard this connection
            self.log_error("Request timed out: %r", e)
            self.close_connection = 1
            return
    def do_GET(self):#针对GET请求方式的应答函数
        print"----------------------------------GET----------------------------------"
        path = self.path#127.0.0.1:8000/wahaha提取出路径的后面部分
        print path
        #拆分url(也可根据拆分的url获取Get提交才数据),可以将不同的path和参数加载不同的html页面，或调用不同的方法返回不同的数据，来实现简单的网站或接口
        query = urllib.splitquery(path)
        print "query=",query
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.send_header("test","This is test!")
        self.end_headers()
        buf = '''<!DOCTYPE HTML>
                <html>
                <head><title>Get page</title></head>
                <body>
                
                <form action="post_page" method="post">
                  username: <input type="text" name="username" /><br />
                  password: <input type="text" name="password" /><br />
                  <input type="submit" value="POST" />
                </form>
                
                </body>
                </html>'''
        self.wfile.write(buf)
        #GET方法对应的请求方式 curl -i 127.0.0.1:8000/wahaha
    def do_POST(self):#针对post请求方式的应答函数
        print"---------------------------------POST---------------------------------"
        path = self.path
        print path
        #获取post提交的数据
        datas = self.rfile.read(int(self.headers['content-length']))
        datas = urllib.unquote(datas).decode("utf-8", 'ignore')
        
        self.send_response(200)
        self.send_header("Content-type","text/html")
        self.send_header("test","This is test!")
        self.end_headers()
        buf = '''<!DOCTYPE HTML>
        <html>
            <head><title>Post page</title></head>
            <body>Post Data:%s  <br />Path:%s</body>
        </html>'''%(datas,self.path)
        self.wfile.write(buf)
        #curl -l -H "Content-type: application/json" -X POST -d '{"phone":"13521389587","password":"test"}'  127.0.0.1:8000/wahaha
    
    @staticmethod
    def start_server(port):
        print "web server listen at port " + str(port) + "..."
        http_server = HTTPServer(('', int(port)), Pybox)#HTTPServer绑定对应的应答类ServerHTTP
        http_server.serve_forever()