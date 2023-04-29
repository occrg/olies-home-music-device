from gpiozero import Button
from gpiozero import LED
import pexpect
import time
import traceback
import sys

from config import config

def initiate_button_loop():
    button = Button(config["BLUETOOTH_BUTTON_NUM"])
    light = LED(config["BLUETOOTH_LIGHT_NUM"])

    while True:
        print("restarted function")
        light.on()
        button.wait_for_press()
        button.wait_for_release()
        print("button pressed")
        light.blink(1, 1)
        allow_bluetooth_connection(button, light)


def allow_bluetooth_connection(button, light):
    pexpect_child = initial_setup_commands()
    expect_connections(pexpect_child, button, light)

def initial_setup_commands():
    pexpect_child = pexpect.spawn("bluetoothctl")
    pexpect_child.logfile = sys.stdout.buffer
    pexpect_child.send("power on\n")
    pexpect_child.send("agent on\n")
    pexpect_child.send("default-agent\n")
    pexpect_child.send("discoverable on\n")
    return pexpect_child

def expect_connections(pexpect_child, button, light):
    try:
        res = pexpect_child.expect([
            "Confirm passkey ([\w\W]{6}) \(yes\/no\)",
            "Authorize service ([\w\W]{8}-[\w\W]{4}-[\w\W]{4}-[\w\W]{4}-[\w\W]{12}) \(yes\/no\):",
            pexpect.TIMEOUT
        ], timeout=30)

        if res == 0:
            light.blink(0.25, 0.25)
            button.wait_for_press()
            button.wait_for_release()
            light.on()
            pexpect_child.send("yes\n")
            expect_authorise_service_with_response(pexpect_child, "one")
            expect_authorise_service_with_response(pexpect_child, "two")
        elif res == 1:
            authorise_service_response(pexpect_child)
            expect_authorise_service_with_response(pexpect_child, "two")
        elif res == 2:
            print("Timeout for initial call. No attempt to connect.")

        pexpect_child.close()

    except BaseException as e:
        print("Unknown error")
        print(e)
        print(traceback.format_exc())
        pexpect_child.send("exit\n")
        pexpect_child.close()

def authorise_service_response(pexpect_child):
    pexpect_child.send("yes\n")
    time.sleep(1)

def expect_authorise_service(pexpect_child, service_key_request_num):
    res = pexpect_child.expect([
        "Authorize service ([\w\W]{8}-[\w\W]{4}-[\w\W]{4}-[\w\W]{4}-[\w\W]{12}) \(yes\/no\):",
        pexpect.TIMEOUT
    ], timeout=10)

    if res == 1:
        print("Timeout for expect authorise service " + service_key_request_num + " call")

    return pexpect_child


def expect_authorise_service_with_response(pexpect_child, service_key_request_num):
    try:
        expect_authorise_service(pexpect_child, service_key_request_num)
        authorise_service_response(pexpect_child)
    except BaseException as e:
        print("Unknown error")
        print(e)
        print(traceback.format_exc())
        pexpect_child.send("exit\n")
        pexpect_child.close()

if __name__ == "__main__":
    initiate_button_loop()
