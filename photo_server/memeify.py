import os, sys
import cStringIO
import math
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

    text_array = wordwrap(text.upper(), font, width - width / 20)

    i = .8
    while len(text_array) * font_size > height / 4:
        font_size = get_font_size(len(text), width, height, i)
        text_array = wordwrap(text.upper(), font, width)
        i -= .1
        if i < .5:
            break

    for i, line in enumerate(text_array):
        fw, fh = font.getsize(line)
        x = (width - fw) / 2
        y = fh * i if top else height - fh * (len(text_array) - i)

        off = fh / 40 + 1
        print fh
        
        draw.text((x-off, y-off), line, (0,0,0), font=font)
        draw.text((x+off, y-off), line, (0,0,0), font=font)
        draw.text((x-off, y+off), line, (0,0,0), font=font)
        draw.text((x+off, y+off), line, (0,0,0), font=font)

        draw.text((x, y), line, (255,255,255), font=font)    

def get_font_size(length, width, height, ratio = .8):
    font_size = 2 * int(ratio * math.sqrt( (width * height / 5) / (2 * length)))
    if font_size > height / 6:
        font_size = height / 6
    return font_size

def wordwrap(s, font, width):
    words = s.split(" ")
    lines = [""]
    width_so_far = 0

    for word in words:
        if lines[-1] is not "":
            word = " " + word

        str_width = font.getsize(word)[0]
        width_so_far += str_width

        if width_so_far > width:
            lines.append("")
            word.strip()
            width_so_far = font.getsize(word)[0]

        lines[-1] += word

    return lines            

if __name__ == '__main__':
    import random

    urls = [
        "http://www.wired.com/images_blogs/underwire/images/2009/04/09/random_dannyhajek.jpg",
        "http://sphotos.ak.fbcdn.net/hphotos-ak-snc4/hs1358.snc4/163046_10150380922285181_787795180_16900389_5869434_n.jpg",
        ]

    words = ["penis", "love", "I", "the", "cow", "killed", "scary", "huge", "whhhhhhhhhat", "crazy", "WOOT!", "Fravic has man boobs"]
    
    for count, url in enumerate(urls):
        word_length = random.randint(1, 10)
        top = ""
        for i in range(word_length):
            if i is not 0:
                top += " "
            top += words[random.randint(0, len(words) - 1)]

        word_length = random.randint(1, 10)
        bot = ""
        for i in range(word_length):
            if i is not 0:
                bot += " "
            bot += words[random.randint(0, len(words) - 1)]
            
        raw = memeify(url, top, bot)
        data = cStringIO.StringIO(raw)        
        img = Image.open(data)
        img.save("meme1" + str(count) + ".jpg")
        data.close()


