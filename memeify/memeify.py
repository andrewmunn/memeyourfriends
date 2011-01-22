import os, sys
import cStringIO
from urllib2 import Request, urlopen, URLError, HTTPError
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def memeify(url, top, bot):
    req = Request(url)

    try:
        f = urlopen(req)
        data = cStringIO.StringIO(f.read())        
        img = Image.open(data)

    except HTTPError, e:
        print "HTTP Error:",e.code , url
    except URLError, e:
        print "URL Error:",e.reason , url

    drawText(img, top, True)
    drawText(img, bot, False)
    
    stringio = cStringIO.StringIO()
    img.save(stringio, "JPEG")
    output = stringio.getvalue()

    data.close()
    stringio.close()
    return output

def drawText(img, text, top):
    width, height = img.size

    font_size = 50 - len(text) * 3
    if font_size < 12:
        font_size = 12

    font = ImageFont.truetype("impact.ttf", font_size)
    draw = ImageDraw.Draw(img)

    text = [text.upper()]
    for i, line in enumerate(text):
        fw, fh = font.getsize(line)
        x = (width - fw) / 2
        y = fh * i if top else height - fh * (len(text) - i)
        
        draw.text((x-2, y-2), line, (0,0,0), font=font)
        draw.text((x+2, y-2), line, (0,0,0), font=font)
        draw.text((x-2, y+2), line, (0,0,0), font=font)
        draw.text((x+2, y+2), line, (0,0,0), font=font)

        draw.text((x, y), line, (255,255,255), font=font)

if __name__ == '__main__':
    url = "http://profile.ak.fbcdn.net/hprofile-ak-snc4/hs1322.snc4/161348_1413751666_2615801_n.jpg"

    raw = memeify(url, "I LOVE", "CODING")

    data = cStringIO.StringIO(raw)        
    img = Image.open(data)
    img.save("meme.jpg")

