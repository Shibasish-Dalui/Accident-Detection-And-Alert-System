import smbus
import time
import math
import requests

# ThingSpeak parameters
THINGSPEAK_API_KEY = 'UYPEAD4CCHPHQNTR'
THINGSPEAK_URL = 'https://api.thingspeak.com/update'

# MPU6050 Registers
MPU6050_ADDR = 0x68
MPU6050_ACCEL_XOUT_H = 0x3B
MPU6050_ACCEL_YOUT_H = 0x3D
MPU6050_ACCEL_ZOUT_H = 0x3F

# Configuration
bus = smbus.SMBus(1)  # For Raspberry Pi 4, use bus 1
bus.write_byte_data(MPU6050_ADDR, 0x6B, 0)  # Wake up the MPU6050


def read_word_2c(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg+1)
    val = (high << 8) + low
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def get_acceleration_data():
    accel_xout = read_word_2c(MPU6050_ACCEL_XOUT_H)
    accel_yout = read_word_2c(MPU6050_ACCEL_YOUT_H)
    accel_zout = read_word_2c(MPU6050_ACCEL_ZOUT_H)
    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0
    return accel_xout_scaled, accel_yout_scaled, accel_zout_scaled


def calculate_magnitude(x, y, z):
    return math.sqrt(x**2 + y**2 + z**2)


def send_to_thingspeak(data):
    params = {'api_key': THINGSPEAK_API_KEY}
    response = requests.post(THINGSPEAK_URL, params=params, data=data)
    print("Response:", response.status_code)


try:
    while True:
        accel_x, accel_y, accel_z = get_acceleration_data()

        # Calculate the average acceleration magnitude
        a_avg = calculate_magnitude(accel_x, accel_y, accel_z)

        # Calculate the gravitational force (9.81 m/s^2 = 1 g)
        g_force = a_avg / 9.81

        print("Acceleration (x,y,z):", accel_x, accel_y, accel_z)
        print("Average Acceleration:", a_avg)
        print("Gravitational Force (g):", g_force)

        # Prepare data for ThingSpeak
        data = {'field1': accel_x, 'field2': accel_y,
                'field3': accel_z, 'field4': a_avg, 'field5': g_force}

        # Send data to ThingSpeak
        send_to_thingspeak(data)

        time.sleep(15)  # Update every 15 seconds

except KeyboardInterrupt:
    pass
