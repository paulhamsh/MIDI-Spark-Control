# MIDI-Spark-Control

## Control your Positive Grid Spark amp from a MIDI controller (via a Raspberry Pi)

This allows you to use a MIDI controller to send presets, change presets and change parameters (gain, volume, tone etc) on the Spark amp. It connects to the amp via bluetooth so can't be used at the same time as the App.

If you use a USB-MIDI cable then DIN connected MIDI devices can also work.

It is configurable via a text file to select which midi messages send which commands to the Spark.


![Spark Setups](Setup1.jpg)

![Spark Setups](Setup2.jpg)

## Instructions

Get a Raspberry Pi with bluetooth (Pi 4 and Pi Zero W, I think the Pi 3 Model B too)

Prepare the Raspberry Pi - load the SD card with Pi Os, boot, set up a password, wifi etc

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
python MidiControl
```
