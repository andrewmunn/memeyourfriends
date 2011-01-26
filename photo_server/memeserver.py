from memeify import memeify
import cherrypy
class HelloWorld:
    def index(self, url = None, top = None, bot = None, left = None, upper = None, right = None, lower = None):
        if not url:
            return "no url"
        cherrypy.response.headers["Content-Type"] = "image/jpeg"
        return memeify(url, top, bot, left, upper, right, lower)
    index.exposed = True

cherrypy.quickstart(HelloWorld(), "/", "cherrypy_config.py")
