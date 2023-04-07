# Olie's Home Music Device
## Description
This project is to turn a Raspberry Pi 3b+ into a Bluetooth adaptor that can plug into an amp to play out speakers and also display the music that's currently playing on Spotify.

## Notes for using this README
Below where I've used `${some text}`, this is used to denote the user's own input. The `${}` characters shouldn't be included.

## Configuration of Raspberry Pi
* Install necessary packages for controlling bluetooth and using the Pi as an audio sink by running `sudo apt-get install bluez pulseaudio-module-bluetooth bluez-tools` in the terminal
* Set the resample method by adding `resample-method = ${a resample method}` to `/etc/pulse/daemon.conf` and commenting out any existing `resample-method`. [Examples and definitions of resample methods are here](https://manpages.debian.org/unstable/pulseaudio/pulse-daemon.conf.5.en.html#resample_method=)
* Set the device's bluetooth class by adding `Class=0x240414` to the `[General]` section in `/etc/bluetooth/main.conf`. This sets the device's major service classes to Audio and Rendering; its Major Device Class as Audio/Video and its Minor Device Class as Loudspeaker. [Documentation here](https://www.ampedrftech.com/datasheets/cod_definition.pdf)
* Set the device's bluetooth display name by adding `PRETTY_HOSTNAME=${some device name}` to `/etc/machine-info` (file may need to be created first) 
