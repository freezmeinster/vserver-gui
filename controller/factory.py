import cherrypy
import threading
from lib.template_loader import render

from lib.remote.master import VpsList

class Controller:
    
    @cherrypy.expose
    def index(self):

        data = {
            'list_vps' : VpsList() ,
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
       
                
        return cherrypy.HTTPRedirect('/dashboard')