import max30102
import hrcalc
import RPi.GPIO as GPIO
from lysring import set_leds
from rpi_ws281x import Adafruit_NeoPixel, Color
import time

# Set up GPIO
BUTTON_PIN = 23
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def take_hr_spo2_readings():
    m = max30102.MAX30102()

    # Initialize lists to store readings
    hr_values = []
    spo2_values = []

    try:
        # Take five valid readings or until the button is pressed
        while len(hr_values) < 6:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                raise KeyboardInterrupt  # Raise KeyboardInterrupt to exit the loop and end the script

            red, ir = m.read_sequential()
            Heartrate, _, SPO2, _ = hrcalc.calc_hr_and_spo2(ir, red)

            # Check if the readings are within range
            if 50 <= Heartrate < 110 and 80 <= SPO2 < 100:
                print(f"Heartrate {Heartrate} BPM: SPO2 {SPO2}%")
                hr_values.append(Heartrate)
                spo2_values.append(SPO2)
                
                if len(hr_values) == 1:
                    set_leds(2, Color(255, 0, 0))
                elif len(hr_values) == 2:
                    set_leds(4, Color(255, 0, 0))
                elif len(hr_values) == 3:
                    set_leds(6, Color(255, 0, 0))
                elif len(hr_values) == 4:
                    set_leds(8, Color(255, 0, 0))
                elif len(hr_values) == 5:
                    set_leds(10, Color(255, 0, 0))
                elif len(hr_values) == 6:
                    set_leds(12, Color(255, 0, 0))

            # Add a short delay to avoid high CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        pass  # This will be executed when the button is pressed

    finally:
        # Cleanup GPIO
        GPIO.cleanup()

    if len(hr_values) == 6:
        # Calculate the average values and print the final reading
        average_hr = int(sum(hr_values) / len(hr_values))
        average_spo2 = int(sum(spo2_values) / len(spo2_values))
        print(f"Average Heartrate: {average_hr} BPM, Average SPO2: {average_spo2}%")
        return average_hr, average_spo2
    else:
        return 0, 0  # Placeholder values when interrupted

