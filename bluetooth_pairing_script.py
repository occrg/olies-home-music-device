import pexpect
import time
import traceback
import sys

def allow_bluetooth_connection():
    pexpect_child = initial_setup_commands()
    expect_connections(pexpect_child)

def initial_setup_commands():
    pexpect_child = pexpect.spawn("bluetoothctl")
    pexpect_child.logfile = sys.stdout.buffer
    pexpect_child.send("power on\n")
    pexpect_child.send("agent on\n")
    pexpect_child.send("default-agent\n")
    pexpect_child.send("discoverable on\n")
    return pexpect_child

def expect_connections(pexpect_child):
    try:
        pexpect_child.expect("Device (([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2}))")
        device_mac = pexpect_child.match.group(1)

        pexpect_child.expect("Confirm passkey ([\w\W]{6}) \(yes\/no\)")
        passkey = pexpect_child.match.group(1)
        pexpect_child.send("yes\n")

        expect_authorise_service_with_response(pexpect_child, "one")
        expect_authorise_service_with_response(pexpect_child, "two")

        time.sleep(1)

        pexpect_child.send("trust " + device_mac.decode("utf-8") + "\n")

        pexpect_child.close()

    except BaseException as e:
        if type(e).__name__ == "TIMEOUT":
            print("Timeout error")
        else:
            print("Other error")
            print(e)
            print(traceback.format_exc())
        pexpect_child.send("exit\n")
        pexpect_child.close()

def authorise_service_response(pexpect_child, service_key_request_num):
    service_key = pexpect_child.match.group(1)
    pexpect_child.send("yes\n")
    time.sleep(1)

def expect_authorise_service(pexpect_child):
    pexpect_child.expect("Authorize service ([\w\W]{8}-[\w\W]{4}-[\w\W]{4}-[\w\W]{4}-[\w\W]{12}) \(yes\/no\):")
    return pexpect_child

def expect_authorise_service_with_response(pexpect_child, service_key_request_num):
    try:
        expect_authorise_service(pexpect_child)
        authorise_service_response(pexpect_child, service_key_request_num)
    except BaseException as e:
        if type(e).__name__ == "TIMEOUT":
            print("Timeout for expect authorise service " + service_key_request_num + " call")
        else:
            print("Other error")
            print(e)
            print(traceback.format_exc())
            pexpect_child.send("exit\n")
            pexpect_child.close()
            sys.exit(1)

allow_bluetooth_connection()
