# appmetrics

I needed a little statistics server to embed into a different project
and didn't want a whole prometheus client. That may have been a bad
choice but I learned some new stuff.

Add `appmetrics.py` to your project, import it, and off you go. Look
at `demo.py` for a trivial example.

Some basic process metrics are created:
- pid
- process name
- process cputime
- run time
- system time

In one terminal run `./demo.py` and observe the output:
```
Starting AppMetrics server on ('localhost', 8274)
```

In another terminal run `curl localhost:8274` and observe some output similar to:
```json
{
 "process": {
  "pid": 125137,
  "appname": "/tmp/appmetrics/demo.py",
  "real": 36.934859697998036,
  "wall": 1718053569.9552777,
  "proc": 0.034161479
 },
 "counter": {
  "loops": 37
 },
 "flag": {
  "is_odd": true
 },
 "gauge": {
  "cpu0temp": 68.0,
  "cpu1temp": 34.0,
  "mem_MemTotal": 58533916672,
  "mem_MemFree": 45508042752,
  "mem_MemAvailable": 46502510592,
  "mem_Buffers": 473497600,
  "mem_Cached": 4851924992,
  "mem_Active": 7980494848,
  "mem_Inactive": 2507583488,
  "mem_Active(anon)": 6164226048,
  "mem_Active(file)": 1816268800,
  "mem_Unevictable": 801316864,
  "mem_Mlocked": 98304,
  "mem_AnonPages": 5963849728,
  "mem_Mapped": 1483362304,
  "mem_Shmem": 1001570304,
  "mem_VmallocTotal": 35184372087808,
  "mem_VmallocUsed": 248848384
 }
}
```
