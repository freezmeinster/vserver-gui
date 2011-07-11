from lib import cherrypy
from lib.template_loader import render

class Controller:
    
    @cherrypy.expose
    def index(self):
        return render("login.html",url_name='login')
        
    @cherrypy.expose
    def dashboard(self,**kwargs):
        return render("dashboard.html",url_name='dashboard')