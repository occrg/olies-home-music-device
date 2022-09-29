import pexpect
import time

child = pexpect.spawn("bluetoothctl")
time.sleep(1)
child.send("power on\n")
print("'power on' command run")
time.sleep(1)
child.send("agent on\n")
print("'agent on' command run")
time.sleep(1)
child.send("default-agent\n")
print("'default-agent' command run")
time.sleep(1)
child.send("discoverable on\n")
print("'discoverable on' command run")
time.sleep(1)

try:
    child.expect("Device (([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2}))")
    device_mac = child.match.group(1)
    print("Device " + device_mac.decode("utf-8") + " is attempting to connect.\n")

    child.expect("Confirm passkey ([\w\W]{6}) \(yes\/no\)")
    passkey = child.match.group(1)
    print("Passkey (" + passkey.decode("utf-8") + ") confirmation requested.\n")
    child.send("yes\n")
    print("Confirmed passkey\n")

    child.expect("Authorize service ([\w\W]{8}-[\w\W]{4}-[\w\W]{4}-[\w\W]{4}-[\w\W]{12}) \(yes\/no\):")
    service_key_one = child.match.group(1)
    print("Service key one (" + service_key_one.decode("utf-8") + ") confirmation requested.\n")
    child.send("yes\n")
    print("Confirmed service key one\n")

    time.sleep(1)

    child.expect("Authorize service ([\w\W]{8}-[\w\W]{4}-[\w\W]{4}-[\w\W]{4}-[\w\W]{12}) \(yes\/no\):")
    service_key_two = child.match.group(1)
    print("Service key two (" + service_key_two.decode("utf-8") + ") confirmation requested.\n")
    child.send("yes\n")
    print("Confirmed service key two\n")

    time.sleep(1)    

    child.send("trust " + device_mac.decode("utf-8") + "\n")
    print("Trusted device " + device_mac.decode("utf-8") + "\n")

    child.close()

except KeyboardInterrupt:
    child.send("exit\n")
    child.close()
