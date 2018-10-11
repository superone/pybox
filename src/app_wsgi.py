#-*- encoding:utf-8 -*- 
from werkzeug.wrappers import Request, Response

@Request.application
def application(request):
    print 'come on...'
    return Response('Hello, World!')

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple('localhost', 8000, application)
# class Pybox:
#     @staticmethod
#     def start_server( port = 8000 ):
#         # if __name__ == '__main__':
#             print 'listen...'
#             from werkzeug.serving import run_simple
#             run_simple('localhost', port, application)
