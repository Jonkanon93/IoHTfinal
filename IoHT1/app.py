import speech_recognition as sr
import time
from sense_hat import SenseHat
import requests 

# Initialize Sense HAT and Speech Recognizer
sense = SenseHat()
recognizer = sr.Recognizer()

# Colors
r = (255, 0, 0)     # red
g = (0, 255, 0)     # green
p = (255, 0, 255)   # purple
k = (0, 0, 0)       # black

red_heart = [
    k, r, r, k, k, r, r, k,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    r, r, r, r, r, r, r, r,
    k, r, r, r, r, r, r, k,
    k, k, r, r, r, r, k, k,
    k, k, k, r, r, k, k, k
]

green_heart = [
    k, g, g, k, k, g, g, k,
    g, g, g, g, g, g, g, g,
    g, r, r, g, g, r, r, g,
    g, g, g, g, g, g, g, g,
    g, g, r, g, g, r, g, g,
    k, g, g, r, r, g, g, k,
    k, k, g, g, g, g, k, k,
    k, k, k, g, g, k, k, k
]

purple_heart = [
    k, p, p, k, k, p, p, k,
    p, p, p, p, p, p, p, p,
    p, p, p, p, p, p, p, p,
    p, p, p, p, p, p, p, p,
    p, p, p, p, p, p, p, p,
    k, p, p, p, p, p, p, k,
    k, k, p, p, p, p, k, k,
    k, k, k, p, p, k, k, k
]

# Function to display a green heart
def display_green_heart():
    sense.set_pixels(green_heart)

# Function to display red while recording
def display_red():
    sense.set_pixels(red_heart)

# Function to blink purple heart
def blink_purple(times=3, duration=0.5):
    for _ in range(times):
        sense.set_pixels(purple_heart)
        time.sleep(duration)
        sense.clear()
        time.sleep(duration)

# Variable to control recording state
recording = False

# Function to record audio
def record_audio():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Recording started. Speak now...")
        return recognizer.listen(source)

# Function to recognize speech from audio and save to a file
def process_audio(audio_data):
    try:
        text = recognizer.recognize_google(audio_data, language='da-DK')
        print("Transcription: " + text)
        if text:
            with open("recording.txt", "w") as file:
                file.write(text)
            send_file("recording.txt", "http://192.168.3.100:5000/upload")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        blink_purple()
        display_green_heart()  # Display green heart again after error
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        blink_purple()
        display_green_heart()  # Display green heart again after error

# Function to send file
def send_file(file_path, url):
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (file_path, f)}
            response = requests.post(url, files=files)
            print(f"File sent, server responded: {response.status_code}, {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Main loop
try:
    display_green_heart()
    audio_data = None
    while True:
        for event in sense.stick.get_events():
            if event.action == 'pressed':
                recording = not recording
                if recording:
                    display_red()
                    audio_data = record_audio()
                else:
                    if audio_data:
                        process_audio(audio_data)
                    display_green_heart()  # Ensure green heart is shown when ready
                    print("Ready to record")
                    audio_data = None
except KeyboardInterrupt:
    sense.clear()
