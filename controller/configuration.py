import cherrypy
from lib.template_loader import render

class Controller:
    
    @cherrypy.expose
    def index(self):
        return render("configuration/index.html")