#!/usr/bin/env python3
# Author: Chris Kuethe <chris.kuethe@gmail.com> , https://github.com/ckuethe/
# SPDX-License-Identifier: MIT

import os
import time

from appmetrics import AppMetrics

ams = AppMetrics(appname=os.path.realpath(__file__))


def read_cputemp(cpu: int) -> float:
    "making some linux-y assumptions about where the sensors are"
    try:
        with open(f"/sys/class/thermal/thermal_zone{int(cpu)}/temp") as ifd:
            return float(ifd.readline().strip()) / 1000
    except Exception:
        return float("nan")


def read_meminfo():
    "just a bunch of statistics"
    meminfos = [
        "MemTotal",
        "MemFree",
        "MemAvailable",
        "Buffers",
        "Cached",
        "Active",
        "Inactive",
        "Active(anon)",
        "Active(file)",
        "Unevictable",
        "Mlocked",
        "AnonPages",
        "Mapped",
        "Shmem",
        "VmallocTotal",
        "VmallocUsed",
    ]
    with open("/proc/meminfo") as ifd:
        rv = {}
        for l in ifd:
            words = l.replace(":", "").split()
            if words[0] not in meminfos:
                continue
            rv[words[0]] = int(words[1]) * 1024 if (len(words) > 2 and words[2] == "kB") else 1
        return rv


def main() -> None:
    n = 0
    spin_chars = "|/-\\"

    ams.counter_create("loops")
    ams.flag_create("is_odd")
    ams.gauge_create("cpu0temp")
    ams.gauge_create("cpu1temp")

    ms = read_meminfo()
    for m in ms:
        ams.gauge_create(f"mem_{m}")
        ams.gauge_update(f"mem_{m}", ms[m])

    while True:
        print(f"\b{spin_chars[n%len(spin_chars)]}", end="", flush=True)
        ams.counter_increment("loops")
        ams.flag_setval("is_odd", n % 2 == 0)
        ams.gauge_update("cpu0temp", read_cputemp(0))
        ams.gauge_update("cpu1temp", read_cputemp(1))
        for m in read_meminfo():
            ams.gauge_update(f"mem_{m}", ms[m])

        n += 1
        time.sleep(1)


if __name__ == "__main__":
    main()
