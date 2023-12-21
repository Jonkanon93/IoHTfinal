import Adafruit_DHT

def temp_luftsensor(sensor_type, gpio_pin):
    # Set up the GPIO pin
    sensor = sensor_type
    pin = gpio_pin

    # Try to grab a sensor reading.
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    # Check if reading was successful
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        print('Failed to get reading. Try again!')
        return None, None

