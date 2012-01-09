import cherrypy
from lib.template_loader import render

class Controller:
    
    @cherrypy.expose
    def about(self):
        return render("resource/about.html")
        
    @cherrypy.expose
    def status(self):
        return render("resource/status.html")
        
    @cherrypy.expose
    def server_stock(self):
        return render("server/stock.html")