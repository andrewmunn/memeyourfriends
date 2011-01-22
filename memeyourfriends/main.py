
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import os
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
    def get(self):
        template_values = {
                   'greetings': ["Hi", "Hello", "Howdy", "DIE IN A FIRE YOU COMMUNIST!"],
                   'url': "http://www.google.com",
                   'url_linktext': "Go to Google!",
               }
        path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        self.response.out.write(template.render(path, template_values))


def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
