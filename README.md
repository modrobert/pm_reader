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
$ ./rdtsc
447585918274014
$ ./rdtsc_a
447728419100158
$ ./rdtsc_a2
0x00019746544d5f59
$ printf "%llu\n" $((`./rdtsc_a2`))
448150994372265
</pre>

