#-*- encoding:utf-8 -*- 
class Route(object):
    __init__(self , request = None , params = None):
        self.request = request
        self.params = params