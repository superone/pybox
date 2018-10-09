#-*- encoding:utf-8 -*- 
from controller import Controller 

def sayHey():
    print 'Hey route ll'

class Ctrl(Controller):
    def index(slef , req , info):
        return '''<!DOCTYPE HTML>
                    <html>
                    <head><title>Get page</title></head>
                    <body>
                        <h1>I am [[info]].<br>kao</h1>
                    </body>
                    </html>'''
    