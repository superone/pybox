#/usr/bin/env python
# -*- coding: UTF-8 -*-
from controller import Controller 

def sayHey():
    print 'Hey route ll'

class Ctrl(Controller):
    def index(slef , req , info):
        buf = '''<!DOCTYPE HTML>
                    <html>
                    <head><title>Get page</title></head>
                    <body>
                        <h1>I am [[info]].<br>刚修改aaa</h1>
                    </body>
                    </html>'''
        return buf.encode('utf-8')