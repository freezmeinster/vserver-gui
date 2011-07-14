import cherrypy
from template_loader import render
from vapi.vapi import VpsServer

class Controller:
    
    @cherrypy.expose
    def index(self):
        return render("login.html",url_name='login')
        
    @cherrypy.expose
    def dashboard(self,**kwargs):
        vserver = VpsServer()
        data = {
                'list_vps' : vserver.vps_obj
            }
        return render("dashboard.html",data,url_name='dashboard')