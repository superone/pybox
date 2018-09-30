#-*- encoding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")

from  BaseHTTPServer import HTTPServer
from  src.app import Pybox


if __name__ == "__main__":
    Pybox.start_server()