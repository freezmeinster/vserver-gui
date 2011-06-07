import cherrypy
from lib.template_loader import render

class Root:
    
    @cherrypy.expose
    def index(self):
        return render("login.html")
        
    @cherrypy.expose
    def dashboard(self,**kwargs):
        data = { 'nguk' : 'syalala' }
        return render("dashboard.html",data)