#!/bin/bash

# start services
service dbus start
service bluetooth start

# start application
python3 influx_Scanner.py
