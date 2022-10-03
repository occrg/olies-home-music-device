import pexpect
import time
import traceback

def allow_bluetooth_connection():
    pexpect_child = initial_setup_commands()
    expect_connections(pexpect_child)

def initial_setup_commands():
    pexpect_child = pexpect.spawn("bluetoothctl")
    pexpect_child.send("power on\n")
    print("'power on' command run")
    pexpect_child.send("agent on\n")
    print("'agent on' command run")
    pexpect_child.send("default-agent\n")
    print("'default-agent' command run")
    pexpect_child.send("discoverable on\n")
    print("'discoverable on' command run")
    return pexpect_child

def expect_connections(pexpect_child):
    try:
        pexpect_child.expect("Device (([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2}))")
        device_mac = pexpect_child.match.group(1)
        print("Device " + device_mac.decode("utf-8") + " is attempting to connect.\n")

        pexpect_child.expect("Confirm passkey ([\w\W]{6}) \(yes\/no\)")
        passkey = pexpect_child.match.group(1)
        print("Passkey (" + passkey.decode("utf-8") + ") confirmation requested.\n")
        pexpect_child.send("yes\n")
        print("Confirmed passkey\n")

        service_auth_key(pexpect_child, "one")
        service_auth_key(pexpect_child, "two")

        time.sleep(1)

        pexpect_child.send("trust " + device_mac.decode("utf-8") + "\n")
        print("Trusted device " + device_mac.decode("utf-8") + "\n")

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

def service_auth_key(pexpect_child, service_key_request_num):
    res_service_key_auth = pexpect_child.expect("Authorize service ([\w\W]{8}-[\w\W]{4}-[\w\W]{4}-[\w\W]{4}-[\w\W]{12}) \(yes\/no\):")
    service_key = pexpect_child.match.group(1)
    print("Service key " + service_key_request_num +
        " (" + service_key.decode("utf-8") + ") confirmation requested.\n")
    pexpect_child.send("yes\n")
    print("Confirmed service key " + service_key_request_num + "\n")
    time.sleep(1)

allow_bluetooth_connection()
