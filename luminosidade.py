from machine import Pin, I2C, SoftI2C
import time
from ssd1306 import SSD1306_I2C

BH1750_ADDR = 0x23
BH1750_CMD = 0x10

i2c_sensor = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)

i2c_oled = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c_oled)  

def iniciar_bh1750():
    i2c_sensor.writeto(BH1750_ADDR, bytes([BH1750_CMD]))

def ler_lux():
    data = i2c_sensor.readfrom(BH1750_ADDR, 2)
    raw = (data[0] << 8) | data[1]
    return raw / 1.2  

iniciar_bh1750()
time.sleep_ms(200)

while True:
    try:
        lux = ler_lux()
        print("Luminosidade: {:.2f} lux".format(lux))
        oled.fill(0)
        oled.text("Luminosidade:", 0, 16)
        oled.text("{:.2f} lux".format(lux), 0, 32)
        oled.show()

        time.sleep(1)

    except Exception as e:
        print("Erro na leitura:", e)
        oled.fill(0)
        oled.text("Erro leitura!", 0, 24)
        oled.show()
        time.sleep(2)
