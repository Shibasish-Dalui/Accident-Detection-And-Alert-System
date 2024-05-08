import serial
import pynmea2


def parse_gps_data(data):
    try:
        if data.find('GGA') > 0:
            msg = pynmea2.parse(data)
            print("Timestamp: {} -- Lat: {} {} -- Lon: {} {} -- Altitude: {} {}".format(
                msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units))
    except Exception as e:
        print("Error parsing GPS data:", str(e))


def main():
    # Define the serial port
    serial_port = '/dev/ttyS0'  # Adjust this based on your actual serial port

    # Open the serial port
    try:
        ser = serial.Serial(serial_port, baudrate=9600, timeout=0.5)
        print("Serial port opened successfully")
    except Exception as e:
        print("Error opening serial port:", str(e))
        return

    # Main loop to continuously read GPS data
    while True:
        try:
            # Read data from the serial port
            data = ser.readline().decode('utf-8')

            # Parse GPS data
            if data.startswith('$'):
                parse_gps_data(data)
        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print("Error reading serial data:", str(e))
            break

    # Close the serial port
    ser.close()


if __name__ == "__main__":
    main()
