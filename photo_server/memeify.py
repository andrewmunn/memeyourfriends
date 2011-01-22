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

    if top: 
        drawText(img, top, True)
    if bot:
        drawText(img, bot, False)
    
    stringio = cStringIO.StringIO()
    img.save(stringio, "JPEG")
    output = stringio.getvalue()

    data.close()
    stringio.close()
    return output

def drawText(img, text, top):
    width, height = img.size

    font_size = get_font_size(len(text), width, height)
    font = ImageFont.truetype("impact.ttf", font_size)
    draw = ImageDraw.Draw(img)

    text = wordwrap(text.upper(), font, width)
    for i, line in enumerate(text):
        fw, fh = font.getsize(line)
        x = (width - fw) / 2
        y = fh * i if top else height - fh * (len(text) - i)
        
        draw.text((x-2, y-2), line, (0,0,0), font=font)
        draw.text((x+2, y-2), line, (0,0,0), font=font)
        draw.text((x-2, y+2), line, (0,0,0), font=font)
        draw.text((x+2, y+2), line, (0,0,0), font=font)

        draw.text((x, y), line, (255,255,255), font=font)

def get_font_size(length, width, height):
#    font_size = 2 * width / length

    font_size = height / 4 - length * 2
    if font_size < 12:
        font_size = 12

    return font_size

def wordwrap(s, font, width):
    words = s.split(" ")
    lines = [""]
    width_so_far = 0

    for i, word in enumerate(words):
        if i is not 0:
            word = " " + word

        str_width = font.getsize(word)[0]
        width_so_far += str_width

        if width_so_far > width:
            width_so_far = 0
            lines.append("")

        lines[-1] += word

    return lines            

if __name__ == '__main__':
    url = "http://profile.ak.fbcdn.net/hprofile-ak-snc4/hs1322.snc4/161348_1413751666_2615801_n.jpg"

    raw = memeify(url, "I LOVE LOVE LOVE LOVE LOVE LOVE LOVE LOVE", "CODING")

    data = cStringIO.StringIO(raw)        
    img = Image.open(data)
    img.save("meme.jpg")
