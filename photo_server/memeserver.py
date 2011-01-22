from memeify import memeify
import cherrypy
class HelloWorld:
    def index(self, url = None, top = None, bot = None):
        if not url:
            return "no url"
        cherrypy.response.headers["Content-Type"] = "image/jpeg"
        return memeify(url, top, bot)
    index.exposed = True

cherrypy.quickstart(HelloWorld(), "/", "cherrypy_config.py")