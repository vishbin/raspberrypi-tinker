#!/usr/bin/env python3

import time
import subprocess
import board
import digitalio
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
from yahoo_fin import stock_info

# which stock to track
TICKER_SYMBOL = 'AAPL'
TICKER_SYMBOL_ARR = ["AAPL", "MA", "COF","PLTR","TSLA","GOOGL","AFRM","C","NFLX","CCL","MSFT","NVDA","V","ABNB","AI","DASH","GE","BAC"]


# configs
OLED_ADDR = 0x3C
OLED_WIDTH = 128
OLED_HEIGHT = 64

# initialize i2c and bus
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c, addr=OLED_ADDR)

# clear display
oled.fill(0)
oled.show()

# create blank image for drawing, and initialiize the draw/fonts
image = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
draw = ImageDraw.Draw(image)
ticker_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 16)
price_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 26)
diff_font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeSans.ttf", 12)

try:
    while True:
        for x in TICKER_SYMBOL_ARR:

            print("Querying stock...:" + x )


            # get stock information
            quote = stock_info.get_quote_table(x)
            price = round(quote['Quote Price'], 2)
            prev_close = round(quote['Previous Close'], 2)
            delta = round(((price - prev_close)*100)/prev_close, 2)
            symbol = '\u25b2' if delta >= 0 else '\u25bc'   # display up/down arrow based on movement

            # convert to strings to display/handle display
            price_str = str(price)
            delta_str = str(delta)

            # calculate positioning
            (price_font_width, price_font_height) = price_font.getsize(price_str)
            (diff_font_width, diff_font_height) = diff_font.getsize(delta_str)

                # Scroll from right-hand side (x 128 to 0 in steps of 16)
            for y in range(128,-64,-8):
                # clear and draw stock info to screen
                draw.rectangle((0, 0, OLED_WIDTH, OLED_HEIGHT), outline=0, fill=0)
                draw.text((y   - ticker_font.getsize(x)[0] // 2, 0), x, font=ticker_font, fill=255)
                draw.text((y   - price_font_width // 2, oled.height // 2 - price_font_height // 2), "{}".format(price_str), font=price_font, fill=255)
                draw.text((y   - diff_font_width // 2, OLED_HEIGHT - diff_font_height), "{} {}%".format(symbol, delta_str), font=diff_font, fill=255)
                oled.image(image)
                oled.show()


                 # Draw a black filled box to clear image.
                #draw.rectangle((0,0,width,height), outline=0, fill=0)    
                
                # Display large Pi-Hole ads blocked percentage
                #draw.text((y, top-2),   "%s%%" % r.json()["ads_percentage_today"],  font=font2, fill=255)
                #draw.text((y, top+34),   "Ads blocked:", font=font, fill=255) 
                #draw.text((y, top+48),   "%s" % r.json()["ads_blocked_today"], font=font, fill=255) 
      

            # sleep between queries
            #print("Done!")
            #time.sleep(5)
except KeyboardInterrupt:
    print("SIGINT detected - releasing screen")
    oled.fill(0)
    oled.show()
    exit(0)


## based on https://jekhokie.github.io/raspberry-pi/oled/python/linux/2020/08/04/stock-display-oled-raspi.html
