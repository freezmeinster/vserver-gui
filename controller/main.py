import cherrypy
from template_loader import render
from vapi.vapi import VpsServer

class Controller:
    
    @cherrypy.expose
    def index(self):
        return render("form.html")
        
    @cherrypy.expose
    def dashboard(self,**kwargs):
        return render("dashboard.html")