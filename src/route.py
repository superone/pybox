#-*- encoding:utf-8 -*- 
import urllib
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
        pass

    def run(self):
        buf = '''<!DOCTYPE HTML>
                <html>
                <head><title>Get page</title></head>
                <body>
                <p>[[info]]</p>
                <form action="post_page" method="post">
                    usernameFF: <input type="text" name="username" /><br />
                    password: <input type="text" name="password" /><br />
                    <input type="submit" value="POST" />
                </form>
                
                </body>
                </html>'''
        buf = buf.replace("[[info]]" , str(self.requestInfo['query'][0]))
        return buf