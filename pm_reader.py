#!/usr/bin/env python3
# Copyright (C) 2020  Robert V. <modrobert@gmail.com> 
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#
# Reference: https://en.wikipedia.org/wiki/Air_quality_index#Computing_the_AQI


import argparse
import json
import signal
import sys
from pms7003 import Pms7003Sensor, PmsSensorException

aqi_pm2_5_levels = {
    "Good": [0.0, 12.0, 0, 50],
    "Moderate": [12.1, 35.4, 51, 100],
    "Unhealthy for Sensitive Groups": [35.5, 55.4, 101, 150],
    "Unhealthy": [55.5, 150.4, 151, 200],
    "Very Unhealthy": [150.5, 250.4, 201, 300],
    "Hazardous": [250.5, 350.4, 301, 400],
    "💀💀💀 GTFO!": [350.5, 500.4, 401, 500],
}

aqi_pm10_levels = {
    "Good": [0, 54, 0, 50],
    "Moderate": [55, 154, 51, 100],
    "Unhealthy for Sensitive Groups": [155, 254, 101, 150],
    "Unhealthy": [255, 354, 151, 200],
    "Very Unhealthy": [355, 424, 201, 300],
    "Hazardous": [425, 504, 301, 400],
    "💀💀💀 GTFO!": [505, 604, 401, 500],
}


def compute_aqi(c, clow, chigh, ilow, ihigh):
    return (((ihigh - ilow) / (chigh - clow)) * (c - clow)) + ilow


def signal_handler(sig, frame):
    print(" Ctrl+C detected, aborting.")
    sys.exit(0)


def main():
    # Catching Ctrl+C for the sake of "continous" mode.
    signal.signal(signal.SIGINT, signal_handler)
    # Handle command line arguments.
    parser = argparse.ArgumentParser(
        description="Read data from PMS7003 particle sensor and calculate AQI."
    )
    parser.add_argument(
        "-c", "--continous", action="store_true", help="keep reading serial data"
    )
    parser.add_argument(
        "-d",
        "--device",
        default="/dev/ttyUSB0",
        help="serial device to read data from",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-j", "--json", action="store_true", help="output in JSON format"
    )
    group.add_argument("-v", "--verbose", action="store_true", help="show more data")
    args = parser.parse_args()

    # Initializing sensor.
    sensor = Pms7003Sensor(args.device)

    continous = True

    # Main loop reading particle sensor.
    while continous:

        try:
            sensor_data = sensor.read()
        except PmsSensorException:
            print("Serial connection problem.")

        pm2_5 = sensor_data["pm2_5cf1"]
        pm10 = sensor_data["pm10cf1"]

        aqi2_5 = 0
        for aqi_category, levels in aqi_pm2_5_levels.items():
            if pm2_5 >= levels[0] and pm2_5 <= levels[1]:
                aqi2_5 = compute_aqi(pm2_5, levels[0], levels[1], levels[2], levels[3])
                if not args.json:
                    print(
                        "PM2.5 AQI: {}  Category: '{}'  [{} μg/m3]".format(
                            round(aqi2_5), aqi_category, pm2_5
                        )
                    )

        aqi10 = 0
        for aqi_category, levels in aqi_pm10_levels.items():
            if pm10 >= levels[0] and pm10 <= levels[1]:
                aqi10 = compute_aqi(pm10, levels[0], levels[1], levels[2], levels[3])
                if args.verbose:
                    print(
                        "PM10 AQI: {}  Category: '{}'  [{} μg/m3]".format(
                            round(aqi10), aqi_category, pm10
                        )
                    )
                    print("--- sensor dump ---")
                    for title, value in sensor_data.items():
                        print("{}: {}".format(title, value))
                    print("-------------------")

        if args.json:
            sensor_data["aqi2_5"] = round(aqi2_5)
            sensor_data["aqi10"] = round(aqi10)
            json_data = json.dumps(sensor_data, sort_keys=False)
            print(json_data)

        continous = args.continous

    sensor.close()


if __name__ == "__main__":
    main()
