# pm_reader

## Read data from PMS7003 particle sensor and calculate AQI.

### Copyright (C) 2020  Robert V. &lt;modrobert@gmail.com&gt;
### Software licensed under GPLv3.

---

### Description

Command line tool which reads data from PMS7003 particle sensor and calculates AQI with several output options.

---

### Usage

<pre>
$ ./pm_reader.py -h
usage: pm_reader.py [-h] [-c] [-d DEVICE] [-j | -v]

Read data from PMS7003 particle sensor and calculate AQI.

optional arguments:
  -h, --help            show this help message and exit
  -c, --continous       keep reading serial data
  -d DEVICE, --device DEVICE
                        serial device to read data from
  -j, --json            output in JSON format
  -v, --verbose         show more data
 
$ ./pm_reader.py
PM2.5 AQI: 151  Category: 'Unhealthy'  [56 μg/m3]

$ ./pm_reader.py --verbose
PM2.5 AQI: 152  Category: 'Unhealthy'  [58 μg/m3]
PM10 AQI: 57  Category: 'Moderate'  [67 μg/m3]
--- sensor dump ---
pm1_0cf1: 39
pm2_5cf1: 58
pm10cf1: 67
pm1_0: 30
pm2_5: 45
pm10: 58
n0_3: 6750
n0_5: 1897
n1_0: 381
n2_5: 29
n5_0: 10
n10: 10
-------------------

$ ./pm_reader.py --json
{"pm1_0cf1": 34, "pm2_5cf1": 50, "pm10cf1": 56, "pm1_0": 27, "pm2_5": 41, "pm10": 51, "n0_3": 6102, "n0_5": 1749, "n1_0": 344, "n2_5": 18, "n5_0": 6, "n10": 2, "aqi2_5": 137, "aqi10": 51}
</pre>

