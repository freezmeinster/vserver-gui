import cherrypy
import threading
from lib.template_loader import render
from vapi.vapi import VpsFactory
from vapi.vapi import VpsServer

class Controller:
    
    @cherrypy.expose
    def index(self):
        server = VpsServer()
        print server.vps_obj
        data = {
            'list_vps' : server.vps_obj ,
             }
        return render("factory/index.html",data)
    
    @cherrypy.expose
    def new(self):
        return render('factory/new.html')
    
    @cherrypy.expose
    def running(self):
        return render("factory/running.html")
    
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