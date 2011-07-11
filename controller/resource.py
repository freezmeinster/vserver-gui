from lib import cherrypy
from lib.template_loader import render

class Controller:
    
    @cherrypy.expose
    def index(self):
        return render("resource/index.html",url_name='resource')