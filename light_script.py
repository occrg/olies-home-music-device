from gpiozero import Button
from gpiozero import LED

from config import config

button = Button(config["BLUETOOTH_BUTTON_NUM"])
light = LED(config["BLUETOOTH_LIGHT_NUM"])

while True:
    print("waiting for button press")
    button.wait_for_press()
    print("button pressed")
    button.wait_for_release()
    print("button released")
    light.toggle()
    print("light toggled")
