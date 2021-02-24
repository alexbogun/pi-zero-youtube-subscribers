#!/usr/bin/python3
# -*- coding:utf-8 -*-
if True: # Imports
    import sys
    import os
    from time import sleep
    from pyyoutube import Api
    api = Api(api_key='AIzaSyApihYliKGLhNkjJty-TejEIwPu4PRNeuU')

    picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
    libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
    if os.path.exists(libdir):
        sys.path.append(libdir)

    import logging
    import time
    from PIL import Image,ImageDraw,ImageFont
    import traceback

    try:
        from waveshare_epd import epd2in13b_V3
        debug = False 
    except:
        debug = True # debug mode mode (on PC)

    # setting loging level
    logging.basicConfig(level=logging.DEBUG)

    # importing fonts
    font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
    font17 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 17)
    font14 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 14)
    font13 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 13)
    subs1 = 0
    subs2 = 0


if True: # functions
    def drawcenteredtext(string, top, font, col=1, colnum=2, color = 'black' ):
        w = int(width*((col-1)/colnum) + (width/colnum - drawblack.textsize(string, font = font)[0]) / 2)
        if color == 'black':
            drawblack.text((w, top), string + ' ', font = font, fill = 0)
        else:
            drawred.text((w, top), string + ' ', font = font, fill = 0)

    def prettyfy (s, maxdig=6):
        s = str(s)
        n = int(s)
        suf = ''
        if len(s)>maxdig:
            suf='k'
            n = n // 1000
            s = str(n)
        if len(s)>maxdig:
            suf='m'
            n = n // 1000
        return f'{n:,}'.replace(',', '\'') + suf


try: # main loop
    l = 0
    while True: 
        # Get Data
        subs1_old = subs1
        subs2_old = subs2
        logging.info("Getting Youtube Data")
        channel1 = api.get_channel_info(channel_id="UCKulTRgkMWsNz5X4f_l9Pjw").items[0].to_dict()
        subs1 = channel1['statistics']['subscriberCount']
        views1 = channel1['statistics']['viewCount']
        channel2 = api.get_channel_info(channel_id="UCRZHPQN3Z-CG-FACzvUOSAA").items[0].to_dict()
        subs2 = channel2['statistics']['subscriberCount']
        views2 = channel2['statistics']['viewCount']

        if (subs1_old != subs1) or (subs2_old != subs2) or (l > 36): #update if something changed, or 6h passed
            l = 0 # reset counter
            if not debug: #wake up
                epd = epd2in13b_V3.EPD()
                logging.info("Init")
                epd.init()
                #epd.Clear()
                time.sleep(1)
                width = epd.height # the display orientation is different
                height = epd.width
                print("width:" + str(width))
                print("height:" + str(height))
            else:
                width = 212
                height = 104
            
            # Drawing on the image
            logging.info("Drawing")    
            Blackimage = Image.new('1', (width, height), 255)  # 212*104
            Redimage = Image.new('1', (width, height), 255)  # 212*104  ryimage: red or yellow image  
            
            h1 = 5 
            h2 = 30
            h3 = 48
            h4 = 75
            h5 = 90

            w1 = 40
        
            drawblack = ImageDraw.Draw(Blackimage)
            drawred = ImageDraw.Draw(Redimage)
            logoimage = Image.open(os.path.join(picdir, 'logo_4.bmp'))
            
            Redimage.paste(logoimage, (w1,h1))
            drawblack.text((w1+40, h1), 'YouTube', font = font20, fill = 0)

            drawcenteredtext(u'Инвестиции', h2, font17, 1)
            drawcenteredtext(u'и Финансы', h3, font17, 1)

            drawcenteredtext(u'Ольга', h2, font17, 2)
            drawcenteredtext(u'Галкина', h3, font17, 2)

            drawcenteredtext(u'Subs: ' + prettyfy(subs1),  h4, font14, 1, 2, 'red')
            drawcenteredtext(u'Views: '+ prettyfy(views1), h5, font13, 1)

            drawcenteredtext(u'Subs: ' + prettyfy(subs2),  h4, font14, 2, 2, 'red')
            drawcenteredtext(u'Views: '+ prettyfy(views2), h5, font13, 2)

            drawblack.line((width/2, h2 + 5, width/2, height - 5), fill = 0)


            if not debug:
                # Rotate output
                Blackimage = Blackimage.transpose(Image.ROTATE_180)
                Redimage = Redimage.transpose(Image.ROTATE_180)
                # actual display 
                epd.display(epd.getbuffer(Blackimage), epd.getbuffer(Redimage))
                time.sleep(2)
            else:
                Redpixels = Redimage.load()
                Combinedimage = Image.new("RGB", (width, height))
                Combinedimage.paste(Blackimage)
                for i in range(width):
                    for j in range(height):
                        if Redpixels[i,j] == 0:
                            Combinedimage.putpixel((i, j), (255, 0, 0))
                #display(Blackimage)
                #display(Redimage)
                display(Combinedimage)


            if not debug:    # Sleep
                logging.info("Goto Sleep...")
                epd.sleep()
        sleep(600) # 10 minutes
        l = l + 1


except IOError as e:
    logging.info(e)
    logging.info("Clear...")
    epd.init()
    epd.Clear()
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    logging.info("Clear...")
    epd.init()
    epd.Clear()
    epd2in13b_V3.epdconfig.module_exit()
    exit()