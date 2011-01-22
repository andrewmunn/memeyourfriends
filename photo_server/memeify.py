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

    font_size = get_font_size2(len(text), width, height)
    font = ImageFont.truetype("impact.ttf", font_size)
    draw = ImageDraw.Draw(img)

    text = wordwrap(text.upper(), font, width)
    for i, line in enumerate(text):
        fw, fh = font.getsize(line)
        x = (width - fw) / 2
        y = fh * i if top else height - fh * (len(text) - i)

        off = 1 if font < 20 else 2
        
        draw.text((x-off, y-off), line, (0,0,0), font=font)
        draw.text((x+off, y-off), line, (0,0,0), font=font)
        draw.text((x-off, y+off), line, (0,0,0), font=font)
        draw.text((x+off, y+off), line, (0,0,0), font=font)

        draw.text((x, y), line, (255,255,255), font=font)

def get_font_size(length, width, height):
    font_size = height / 4 - length * 2
    if font_size < 12:
        font_size = 12

    return font_size

def get_font_size2(length, width, height):
    font_size = 2 * int(math.sqrt( (.9 * width * height / 5) / (2 * length)))
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
        "http://profile.ak.fbcdn.net/hprofile-ak-snc4/hs1322.snc4/161348_1413751666_2615801_n.jpg",
        "http://t3.gstatic.com/images?q=tbn:ANd9GcTbhbwZ_m0GcUAve6aICiTo7kgvQJjWr0gRogdbLZFNSWghOQUx1A",
        "http://thechive.files.wordpress.com/2009/06/a-random-hot-chicks-r5-21.jpg?w=500&h=375",
        "http://www.wired.com/images_blogs/underwire/images/2009/04/09/random_dannyhajek.jpg"
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


