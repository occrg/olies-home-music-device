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
        res = pexpect_child.expect([
            "Confirm passkey ([\w\W]{6}) \(yes\/no\)",
            "Authorize service ([\w\W]{8}-[\w\W]{4}-[\w\W]{4}-[\w\W]{4}-[\w\W]{12}) \(yes\/no\):",
            pexpect.TIMEOUT
        ], timeout=30)

        if res == 0:
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
        sys.exit(1)

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
        sys.exit(1)

allow_bluetooth_connection()
