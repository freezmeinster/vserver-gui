import cherrypy
import threading
from lib.template_loader import render
from vapi.vapi import VpsFactory

class Controller:
    
    @cherrypy.expose
    def index(self):

        data = {
            'ip' : cherrypy.server.allip ,
             }
        return render("factory/index.html",data,url_name='factory')
    
    @cherrypy.expose
    def build(self,name,ip,memory,passwd1,passwd2):
        class BuildVps( threading.Thread ):
            def run(self):
                vps = VpsFactory(ip=self.ip,nama=self.nama,memory=self.memory,password=self.password)
                vps.save()
        
        if passwd1 == passwd2 :        
            thread = BuildVps()
            thread.ip = ip
            thread.nama = name
            thread.memory = memory
            thread.password = passwd1
            thread.start()
                
        return cherrypy.HTTPRedirect('/dashboard')