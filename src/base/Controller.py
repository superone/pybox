#-*- encoding:utf-8 -*- 
class Controller(object):
    def __init__(self , request = None , params = None):
        self.request = request
        self.params = params
    def run(self , request , route ):
        print"run controller"
        pass