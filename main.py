from ili9341 import ILI9341, color565
from machine import Pin, SPI
from touch import Touch
import font
import font14
import font24
import font32
import utime

colors = [color565(255,0,0),color565(255,255,0),color565(0,255,0),color565(0,255,255),color565(0,0,255),color565(255,0,255),color565(0,0,0),color565(255,255,255)]
fonts = [font,font14,font24,font32]

led_onboard = Pin(25, Pin.OUT)
#utime.sleep_ms(5000)

# define pins
#-------------------
cs = Pin(17, Pin.OUT)
rst = Pin(14, Pin.OUT)
dc = Pin(15, Pin.OUT)
spi = SPI(0, 60000000, mosi=Pin(19), miso=Pin(16), sck=Pin(18))
display = ILI9341(spi, cs,dc,rst, w=320, h=240, r=1)

spi2 = SPI(1,
baudrate=5000000,
sck=Pin(10), 
mosi=Pin(11), 
miso=Pin(12))

for c in colors:
    display.fill_rectangle(0,0,320,240, c)
    utime.sleep_ms(500)
    
display.fill_rectangle(85, 50, 150, 50, color565(0,0,255))

display.fill_rectangle(5, 140, 150, 50, color565(0,0,255))
display.set_pos(30, 150)
display.set_color(color565(255,255,255),color565(0,0,255))
display.set_font(font32)
display.print("LED ON")

display.fill_rectangle(165, 140, 150, 50, color565(255,0,0))
display.set_pos(185, 150)
display.set_color(color565(255,255,255),color565(255,0,0))
display.set_font(font32)
display.print("LED OFF")


class Screen(object): 
    # Simple screen demo
    CYAN    = color565(0, 255, 255)
    RED     = color565(255, 0, 0)
    PURPLE  = color565(255, 0, 255)
    WHITE   = color565(255, 255, 255)

    def __init__(self,spi2):

        self.touch = Touch(spi2, 
                           cs=Pin(13), 
                           int_pin=Pin(9),
                           int_handler=self.touchscreen_press)

        self.dot = bytearray(b'\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\xF8\x00\xF8\x00\x07\xE0\xF8\x00\xF8\x00\xF8\x00\x07\xE0\x00\x00\x07\xE0\xF8\x00\x07\xE0\x00\x00')

    def touchscreen_press(self, x, y):
        display.set_pos(0,0)
        display.set_font(font14)
        display.print("{0:03d}, {1:03d}".format(x, y))
        
        if 100 <= x <= 200 and 20 <= y <= 155:
           display.fill_rectangle(85, 50, 150, 50, color565(0,0,255))
           led_onboard.value(0)

        if 115 <= x <= 195 and 187 <= y <= 300: 
            display.fill_rectangle(85, 50, 150, 50, color565(255,0,0))
            led_onboard.value(1)




def main():

    # Init SPI1 for touchscreen
    spi2 = SPI(1,
               baudrate=5000000,
               sck=Pin(10), 
               mosi=Pin(11), 
               miso=Pin(12))
    
    Screen(spi2)





while True: 
         main()