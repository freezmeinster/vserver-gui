import cherrypy
from template_loader import render

class Controller:
    
    @cherrypy.expose
    def index(self):
        return render("form.html")
        
    @cherrypy.expose
    def dashboard(self,**kwargs):
        return render("dashboard.html")