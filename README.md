# Olie's Home Music Device
## Description
This project is to turn a Raspberry Pi into a Bluetooth adaptor that can plug into an amp to play out speakers and also display the music that's currently playing on Spotify.

## Notes for using this README
Below where I've used `${some text}`, this is used to denote the user's own input. The `${}` characters shouldn't be included.

## Raspberry Pi setup
Instructions and code were tested with the following setup as of the day of the repo's last commit. If you have a different setup, some instructions or code may need tweaking to be suitable to that setup.

Model: Raspberry Pi 3b+<br/>OS: Rapberry Pi OS 64-bit.

## Instructions
### Raspberry Pi as bluetooth adaptor
#### Test standard aux sound
First, it's wise to do a very basic test that the Pi can output sound to your speakers so when you follow future steps, you know that outputting to the speakers isn't the issue.
* Connect some speakers or headphones to the Pi using the Pi's 3.5mm headphone jack.
* Test that the Pi can output sound to the speakers (see the "Playing a test sound" subsection for an idea of how to do this).

#### Setup DAC
I've bought an external DAC (specifically the [DAC2 Pro](https://www.hifiberry.com/shop/boards/hifiberry-dac2-pro/)) in an attempt to improve the sound quality of the system. If you have one, you'll need to follow the below instructions to set it up. Otherwise, you can ignore this subsection.

You should follow these instructions before connecting the DAC to your Pi. The instructions tell you the appropriate time to connect them.
* The Pi defaults to outputting audio via the HDMI port and 3.5mm headphone jack. To change this so the DAC is the default audio output, make the changes to `/boot/firmware/config.txt` that are indented below.
  * Uncomment the `dtparam=i2s=on` line.
  * Comment out the line `dtparam=audio=on`.
  * Underneath the above line, add this line: `dtoverlay=${audio card driver}`.  [The appropriate audio card driver is in the "Configuration" of the DAC's data sheet](hifiberry.com/docs/) (for example, for me, the line was `dtoverlay=hifiberry-dacplus-pro`).
* Turn off your Raspberry Pi (for example, using `shutdown -h now` in the terminal).
* Connect the DAC to your Raspberry Pi.
* Connect some speakers or headphones to the DAC's line out connector.
* Test that the Pi can output sound to the speakers now the DAC is connected (see the "Playing a test sound" subsection for an idea of how to do this).

#### Setup bluetooth source
Next you need to configure the Pi's bluetooth and audio settings so the bluetooth is treated as an audio sink meaning that audio transferred to the Pi via bluetooth is treated as an audio source.
* Install necessary packages for controlling bluetooth and using the Pi as an audio sink by running `apt-get install bluez bluez-tools pulseaudio-module-bluetooth` in the terminal.
  * `bluez` and `bluez-tools` are installed to provide an interface to more easily use bluetooth functionality on Linux.
  * `pulseaudio-module-bluetooth` is the bluetooth module for the Pulse Audio sound server.

#### Connect a device to the pi
At this point, you should already be able to connect a device and play music. Make sure to repeat this consistently when making changes to ensure that you haven't broken anything!
* Run `python bluetooth_pairing_script_simple.py` in the root folder of this project in the terminal. This will make the Raspberry Pi discoverable to all devices within range and accept any passcode and permissions that it's asked to (you may want to be aware that this isn't the best security wise and will be improved when I add IO buttons).
* Click to connect to the Pi when it comes up on your device.
* Play some sound on your device and it should come out of the speakers that are connected to your Pi!

#### Optional Configuration
Now you're playing music from your device, that's the main thing. There are a few other things to tweak the Pi's sound and bluetooth to your taste as well as things I saw in many tutorials but I found I didn't need.

* Set a name that your Pi can be recognised by via bluetooth. This is the name that will show up on bluetooth menus.
  * This can be done by adding the line `PRETTY_HOSTNAME=${some device name}` to `/etc/machine-info`. This file may need to be created if it doesn't already exist.
  * Restart bluetooth (as in the "Restarting bluetooth" subsection) for the change to take effect.
  * You can check that this change has taken effect by running `hciconfig -a` in the terminal and checking the "Name" attribute.
* You may want to change the Pi's bluetooth class so other devices recognise that the Pi is a bluetooth speaker.
  * You can do this by adding `Class=0x240414` to the `[General]` section in `/etc/bluetooth/main.conf`. This sets the device's major service classes to Audio and Rendering; its Major Device Class as Audio/Video and its Minor Device Class as Loudspeaker. [Documentation here](https://www.ampedrftech.com/datasheets/cod_definition.pdf).
  * Then you should restart bluetooth as in the "Restarting bluetooth" subsection.
  * Restart bluetooth (as in the "Restarting bluetooth" subsection) for the change to take effect.
  * You can check that this change has taken place by running `hciconfig -a` in the terminal and checking the "Class" attribute. I found that the major classes were overriden. However, this seems to be fine as even though two extra classes have been included, "Capturing" and "Telephony", the classes I wanted have been included and the Pi shows as a loudspeaker on my laptop. I believe the extra classes are showing due to some configuration that I should change but can't work out.
* You may want to update the resample method of Pulse Audio as there is a pay off between the quality of the audio, its latency and the amount of CPU the audio server takes up.
  * This can be updated by adding `resample-method = ${resample method}` to `/etc/pulse/daemon.conf` and commenting out any existing `resample-method` (for example I decided to go for the line `resample-method = soxr-vhq`). [Examples and definitions of resample methods are here](https://manpages.debian.org/unstable/pulseaudio/pulse-daemon.conf.5.en.html#resample_method=).
  * Restart bluetooth (as in the "Restarting bluetooth" subsection) for the change to take effect.
  * You can check this this change has taken effect by running `pulseaudio --dump-conf` in the terminal and checking the "resample-method" attribute.

### Some repeat instructions
#### Playing a test sound
I used the `speaker-test` terminal command (for example, `speaker-test -c2 -twav -l3`) [which is documented here](https://linux.die.net/man/1/speaker-test).

#### Restarting bluetooth
To make sure any of the above changes take effect, you may need to restart bluetooth by following the below steps.
* Run `systemctl daemon-reload` in the terminal. This resets the system configuration which will apply the changes you made to config files.
* Run `service bluetooth restart` in the terminal. This restarts the bluetooth service.

## Relevant Documentation
* [LED](https://gpiozero.readthedocs.io/en/stable/api_output.html#led)
* [Button](https://gpiozero.readthedocs.io/en/stable/api_input.html#button)
