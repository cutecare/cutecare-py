## Functionality 
This is the Python package for reading a measurement from the CuteCare DIY sensor.
Use the library within Home Assistant.

## Backends
As there is unfortunately no universally working Bluetooth Low Energy library for Python, the project currently 
offers support for two Bluetooth implementations:
* bluez tools (via a wrapper around gatttool)
* bluepy library

## Development environment setup steps
### Linux (Ubuntu)
```
sudo apt-get install python3-pip python3-dev python3-venv python3-setuptools
sudo apt-get install libboost-all-dev libssl-dev libxml2-dev libxslt1-dev libjpeg-dev libffi-dev libudev-dev zlib1g-dev libpython-dev libudev-dev
sudo apt-get install libglib2.0-dev libboost-python-dev luetooth libbluetooth-dev net-tools rfkill nmap iputils-ping
sudo ln -s /usr/lib/x86_64-linux-gnu/libboost_python-py35.so /usr/lib/x86_64-linux-gnu/libboost_python-py34.so
sudo pip3 install gattlib
```
