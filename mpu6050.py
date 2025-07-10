from machine import Pin, I2C, SoftI2C
import time
import math
from ssd1306 import SSD1306_I2C

print("Verificando dispositivos I2C...")
temp_i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)
devices_mpu = temp_i2c.scan()
print("Dispositivos no barramento MPU6050:", [hex(x) for x in devices_mpu])

i2c_mpu = I2C(1, scl=Pin(3), sda=Pin(2), freq=400000)

i2c_oled = SoftI2C(scl=Pin(15), sda=Pin(14))
devices_oled = i2c_oled.scan()
print("Dispositivos no barramento OLED:", [hex(x) for x in devices_oled])
oled = SSD1306_I2C(128, 64, i2c_oled)

MPU_ADDR = 0x68 if 0x68 in devices_mpu else 0x69
print(f"Usando endereço MPU: {hex(MPU_ADDR)}")

def mpu6050_init():
    i2c_mpu.writeto_mem(MPU_ADDR, 0x6B, b'\x00')
    time.sleep_ms(100)
    
  
    i2c_mpu.writeto_mem(MPU_ADDR, 0x1C, b'\x00')
    
   
    i2c_mpu.writeto_mem(MPU_ADDR, 0x1B, b'\x00')
    time.sleep_ms(100)


def read_raw_data(reg):
    high = i2c_mpu.readfrom_mem(MPU_ADDR, reg, 1)[0]
    low = i2c_mpu.readfrom_mem(MPU_ADDR, reg+1, 1)[0]
    value = (high << 8) | low
    if value > 32767:
        value -= 65536
    return value

# Lê acelerômetro (g)
def read_accel():
    ax = read_raw_data(0x3B) / 16384.0
    ay = read_raw_data(0x3D) / 16384.0
    az = read_raw_data(0x3F) / 16384.0
    return (ax, ay, az)

# Lê giroscópio (°/s)
def read_gyro():
    gx = read_raw_data(0x43) / 131.0
    gy = read_raw_data(0x45) / 131.0
    gz = read_raw_data(0x47) / 131.0
    return (gx, gy, gz)

# Calcula ângulos roll e pitch
def get_inclination():
    ax, ay, az = read_accel()
    roll = math.atan2(ay, az) * 180 / math.pi
    pitch = math.atan2(-ax, math.sqrt(ay*ay + az*az)) * 180 / math.pi
    return roll, pitch

# Inicializa sensor
try:
    mpu6050_init()
    print("MPU6050 inicializado com sucesso!")
    oled.fill(0)
    oled.text("MPU6050 OK", 0, 24)
    oled.show()
    time.sleep(1)
except Exception as e:
    print("Erro na inicializacao:", e)
    oled.fill(0)
    oled.text("Erro MPU6050", 0, 24)
    oled.show()
    time.sleep(2)

prev_roll, prev_pitch = 0, 0
ALPHA = 0.2  

while True:
    try:
        roll, pitch = get_inclination()
        ax, ay, az = read_accel()
        gx, gy, gz = read_gyro()
        
    
        smooth_roll = ALPHA * roll + (1 - ALPHA) * prev_roll
        smooth_pitch = ALPHA * pitch + (1 - ALPHA) * prev_pitch
        prev_roll, prev_pitch = smooth_roll, smooth_pitch

        
        print(f"Roll: {smooth_roll:.2f} deg, Pitch: {smooth_pitch:.2f} deg")
        print(f"Accel: X={ax:.2f}g Y={ay:.2f}g Z={az:.2f}g")
        print(f"Gyro: X={gx:.2f} deg/s Y={gy:.2f} deg/s Z={gz:.2f} deg/s")
        print("-" * 40)

 
        oled.fill(0)
        oled.text(f"R: {smooth_roll:.1f} deg", 0, 0)
        oled.text(f"P: {smooth_pitch:.1f} deg", 0, 12)
        oled.text(f"A: {ax:.2f},{ay:.2f},{az:.2f}", 0, 26)
        oled.text(f"G: {gx:.2f},{gy:.2f},{gz:.2f}", 0, 40)
        oled.show()

        time.sleep(0.2)

    except Exception as e:
        print("Erro durante operacao:", e)
        oled.fill(0)
        oled.text("Erro na leitura", 0, 24)
        oled.text("Reiniciando...", 0, 40)
        oled.show()
        time.sleep(2)
        
    
        try:
            mpu6050_init()
        except:
            pass