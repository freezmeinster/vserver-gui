from lib import cherrypy
from lib.template_loader import render

class Controller:
    
    @cherrypy.expose
    def index(self):
        return render("login.html")
        
    @cherrypy.expose
    def dashboard(self,**kwargs):
        data = { 'config' : cherrypy.config }
        return render("dashboard.html",data)