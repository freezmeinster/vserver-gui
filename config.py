import os,sys

def data():
    conf = { 'global' :
                    {
                        'server.socket_host' : '192.168.70.250',
                        'server.socket_port' : 8080,
                        'server.thread_pool' : 10,
                        'tools.sessions.on' : True
                    }, 
            
               '/' :
                    {
                       'tools.staticdir.root' : os.path.dirname(__file__)
                    },
               '/public':
                   {
                       
                   }
             }
    return conf