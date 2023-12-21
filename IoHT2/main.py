from rpi_ws281x import Adafruit_NeoPixel, Color
from temp_luftsensor import temp_luftsensor
from minmåler import take_hr_spo2_readings
from nygas import gassensor
import RPi.GPIO as GPIO
import lysring as np
import Adafruit_DHT
import time

sensor_type = Adafruit_DHT.DHT11
dht_pin = 17


file_path = "readings.txt"

try:
    print("Program started. Press the button to pause air quality check for 5 seconds.")
    while True:
        # Set up GPIO for the button
        button_pin = 23 

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        temperature, humidity = temp_luftsensor(sensor_type, dht_pin)

        if humidity is not None:
            print(f'Humidity: {temperature} {humidity:.1f}%')

            # Set air quality level based on humidity range
            if 30 <= humidity < 45:
                humidity_air_quality = 1
            elif 45 <= humidity < 70:
                humidity_air_quality = 5
            elif 70 <= humidity < 80:
                humidity_air_quality = 9
            elif 80 <= humidity < 90:
                humidity_air_quality = np.alarm()
            else:
                humidity_air_quality = 0

        # Read ppm value after humidity
        ppm = gassensor()

        # Set air quality level based on ppm range
        if 40 <= ppm < 60:
            ppm_air_quality = 1
        elif 60 <= ppm < 100:
            ppm_air_quality = 5
        elif 100 <= ppm < 120:
            ppm_air_quality = 9
        elif 120 <= ppm < 900:
            ppm_air_quality = np.alarm()
        else:
            ppm_air_quality = 0

        # Choose the final air quality level based on both humidity and ppm
        final_air_quality = max(humidity_air_quality, ppm_air_quality)

        # Set the final air quality level
        np.set_air_quality(final_air_quality)

        # Check if the button is pressed
        if GPIO.input(button_pin) == GPIO.LOW:
            print("Button pressed! Pausing air quality check for 5 seconds...")
            np.loading()
            np.set_leds(1, Color(255, 0, 0))
            hr, spo2 = take_hr_spo2_readings()
            print("Resuming air quality check...")
            np.loading()

             # Write the values to the file
            with open(file_path, "w") as file:
                file.write(f"Temperature: {temperature}°C\n")
                file.write(f"Humidity: {humidity}%\n")
                file.write(f"Heart Rate: {hr} BPMN\n")
                file.write(f"SPO2: {spo2}%\n")

except KeyboardInterrupt:
    np.set_air_quality(0)  # turn off the LEDs
    print("\nProgram terminated by user.")

