from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.api.urlfetch import fetch
from MultipartPostHandler import *
import facebook as fb
import os
import urllib
import urllib2
import logging
import utils
import cStringIO as StringIO

APP_KEY = "1c6f5e338c7989f098ad50f8c1224878"
APP_SECRET = "7d6557c4b9ce6d061b7047041d6538b0"
GRAPH_PHOTO_URL = "https://graph.facebook.com/me/photos"
MEME_URL = "http://www.willhughes.ca:8080"


class MainHandler(webapp.RequestHandler):
    def post(self):        
        template_values = {}
        path = os.path.join(os.path.dirname(__file__),
                            'templates', 'index.html')
        self.response.out.write(template.render(path, template_values))


class MemeHandler(webapp.RequestHandler):
    def post(self):

        user = fb.get_user_from_cookie(self.request.cookies, APP_KEY, APP_SECRET)
        access_token = user["access_token"]

        url = self.request.get('url')
        top = self.request.get('top')
        bot = self.request.get('bot')
 
        # Retrieve meme photo from meme server
        meme_params = urllib.urlencode({'url':url,
                                        'top':top,
                                        'bot':bot})
        logging.info(MEME_URL + '?' + meme_params)
        meme_data = fetch(MEME_URL + '?' + meme_params)
        logging.info(len(meme_data.content))
        
        # Post photo and message to user's album
        msg = top + " " + bot
#        post_data = {   
#            "access_token": access_token,
#            "message": msg,
#            "source": meme_data.content
#            }
        logging.info(access_token)
#        response = fetch(GRAPH_PHOTO_URL,
#              payload = post_data,
#              method = "POST",
#              headers = {"Content-Type":
#                             "multipart/form-data"})
#        request = urllib2.Request(GRAPH_PHOTO_URL, urllib.urlencode(post_data),
#                                   {"Content-Type":
#                             "multipart/form-data"})
#        response = urllib2.urlopen(request)
#
#        out = utils.posturl('https://graph.facebook.com/me/photos', [('access_token', access_token)], [('source', 'upload.jpg', str(response.read()))])
#        logging.info(out)

        opener = urllib2.build_opener(MultipartPostHandler)
        params = {   
                    "access_token": access_token,
                     "message": msg,
                  "source": StringIO.StringIO(meme_data.content)
                                   }
        try:
            opener.open(GRAPH_PHOTO_URL, params).read()
        except urllib2.HTTPError, ex:
            logging.info(ex.message)
        logging.info


def main():
    routes = [('/', MainHandler),
              ('/meme', MemeHandler)]
    application = webapp.WSGIApplication(routes,
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
