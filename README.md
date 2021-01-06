# MIDI-Spark-Control

Based on the great work here: https://github.com/jrnelson90/tinderboxpedal

## Control your Positive Grid Spark amp from a MIDI controller (via a Raspberry Pi)

This allows you to use a MIDI controller to send presets, change presets and change parameters (gain, volume, tone etc) on the Spark amp. It connects to the amp via bluetooth so can't be used at the same time as the App.

If you use a USB-MIDI cable then DIN connected MIDI devices can also work.

It is configurable via a text file to select which midi messages send which commands to the Spark.

## Example setup with USB midi device (Novation Launchkey 25)

![Spark Setups](https://github.com/paulhamsh/MIDI-Spark-Control/blob/main/digrams/Setup1.jpg)

## Example setup with DIN MIDI device (Behringer FCB1010)

![Spark Setups](https://github.com/paulhamsh/MIDI-Spark-Control/blob/main/digrams/Setup2.jpg)

## Instructions

Get a Raspberry Pi with bluetooth (Pi 4 and Pi Zero W, I think the Pi 3 Model B too)

Prepare the Raspberry Pi - load the SD card with Pi Os, boot, set up a password, wifi etc

The code is dependent on pygame but that is installed by default on a Raspberry Pi.

(Note - this code also works with Windows)

(If you want to set it up to run SSH and not start into the GUI:

```
sudo systemctl enable ssh
sudo systemctl start ssh

sudo raspi-config nonint do_boot_behaviour B2

```

You need the following installed:

```
sudo apt-get install libbluetooth-dev
python3 -m pip install pybluez
```

And get this code and install it:

```

```

Edit MidiConfig.py to select the interface you are using and set the MIDI - Spark mapping.

Then simply 

```
python MidiControl.py
```

