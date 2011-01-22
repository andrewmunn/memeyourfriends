
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.urlfetch import fetch
import facebook as fb
import os
import settings
import memeify
import urllib
from google.appengine.ext.webapp import template

class MainHandler(webapp.RequestHandler):
    def get(self):
            
        path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
        self.response.out.write(template.render(path, template_values))
        
class MemePhoto(webapp.RequestHandler):
    def get(self):
        user = fb.get_user_from_cookie(self.request.cookies, key, secret)
        if user:
            photo_url = self.request.get('url')
            top_caption = self.request.get('top')
            bot_caption = self.request.get('bot')
        
            raw_data = fetch(photo_url, deadline = 10) //get the raw data
        
            meme = memeify.memeify(data, top, bot)
            
            graph = facebook.GraphAPI(user["access_token"])            
                
            graph._put_object("me", "photos", message=top_caption + " " + bot_caption, )
            
            post_data = {   
                            "access-token": user["access_token"],
                            "message": top_caption + " " + bot_caption,
                            "source": meme 
                        }
            fetch("https://graph.facebook.com/" + "me/photos",  payload = post_data, method = "POST", headers={"Content-Type": "multipart/form-data"})
def main():
    application = webapp.WSGIApplication([('/', MainHandler), ('memephoto/', MemePhoto)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
