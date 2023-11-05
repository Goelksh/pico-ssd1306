# Display Image & text on I2C driven ssd1306 OLED display 
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import utime
 
adcpin = 4
sensor = machine.ADC(adcpin)
  
def ReadTemperature():
    #subtracting 5000 from the ADC value to caliberate the our room temperature 
 	adc_value = sensor.read_u16() -5000
 	volt = (3.3/65535) * adc_value
 	temperature = 27 - (volt - 0.706)/0.001721
 	return round(temperature, 1)
 
V_OFFSET  = 8                                         # vertical offset for scrolling
WIDTH  = 128                                            # oled display width
HEIGHT = 32                                             # oled display height
 
i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=200000)       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config
 
 
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display
 
# Raspberry Pi logo as 32x32 bytearray
buffer = bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c \x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
 
while True:
    # Load the raspberry pi logo into the framebuffer (the image is 32x32)
    fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
 
    # Clear the oled display in case it has junk on it.
    oled.fill(0)
 
    # Blit the image from the framebuffer to the oled display
    oled.blit(fb, 96, 0)
    
    
    # adding a horizontal lines
    oled.hline(0, V_OFFSET, 96, 0xffff)
    
    # Add some text
    oled.text("ADC: " + str(ReadTemperature()),5,V_OFFSET + 2)
    oled.text("Programing! ",5,V_OFFSET + 12)
    
    # adding a horizontal lines
    oled.hline(0, V_OFFSET + 22, 96, 0xffff)
 
    # Finally update the oled display so the image & text is displayed
    oled.show()
    
    #scroll vertically
    for i in range (30):
        oled.scroll(0,-1)
        oled.show()
        utime.sleep(.1)    
    
    