# Plot-Sysbench

## Commands to run before

### Prepare

```shell
sysbench /tmp/sysbench-master/src/lua/oltp_read_write.lua  --mysql-user=root --mysql-password=mysql --mysql-port=3306 \
--mysql-socket=/data/mysql55/mysql.sock  --mysql-host=localhost \
--mysql-db=sysbenchtest  --tables=10 --table-size=5000000  --threads=30 \
--events=5000000 --report-interval=5 prepare
```

### Run

```shell
sysbench \
/tmp/sysbench-master/src/lua/oltp_read_write.lua \
--mysql-user=root  --mysql-password=mysql --mysql-port=3306 \
--mysql-socket=/data/mysql55/mysql.sock  --mysql-host=localhost \
--mysql-db=sysbenchtest  --tables=10 --table-size=5000000 \
--threads=30 --report-interval=5 --time=300 run > oltp_read_write.txt
```

_Generated output to parse_:

```
[ 5s ] thds: 30 tps: 73.76 qps: 1538.67 (r/w/o: 1084.35/300.82/153.51) lat (ms,95%): 733.00 err/s: 0.00 reconn/s: 0.00
[ 10s ] thds: 30 tps: 75.80 qps: 1519.27 (r/w/o: 1062.85/304.81/151.61) lat (ms,95%): 590.56 err/s: 0.00 reconn/s: 0.00
[ 15s ] thds: 30 tps: 58.39 qps: 1183.57 (r/w/o: 831.24/235.55/116.78) lat (ms,95%): 926.33 err/s: 0.00 reconn/s: 0.00
[ 20s ] thds: 30 tps: 48.21 qps: 961.19 (r/w/o: 672.13/192.64/96.42) lat (ms,95%): 1129.24 err/s: 0.00 reconn/s: 0.00
[ 25s ] thds: 30 tps: 43.57 qps: 863.96 (r/w/o: 606.66/170.15/87.14) lat (ms,95%): 1109.09 err/s: 0.00 reconn/s: 0.00
[ 30s ] thds: 30 tps: 21.70 qps: 418.24 (r/w/o: 291.07/83.77/43.41) lat (ms,95%): 2585.31 err/s: 0.00 reconn/s: 0.00
[...]
[ 285s ] thds: 30 tps: 36.41 qps: 720.35 (r/w/o: 503.91/143.63/72.82) lat (ms,95%): 1561.52 err/s: 0.00 reconn/s: 0.00
[ 290s ] thds: 30 tps: 35.80 qps: 740.01 (r/w/o: 523.00/145.40/71.60) lat (ms,95%): 1678.14 err/s: 0.00 reconn/s: 0.00
[ 295s ] thds: 30 tps: 32.94 qps: 662.28 (r/w/o: 466.61/129.78/65.89) lat (ms,95%): 1973.38 err/s: 0.00 reconn/s: 0.00
[ 300s ] thds: 30 tps: 32.27 qps: 639.95 (r/w/o: 439.33/136.09/64.54) lat (ms,95%): 1869.60 err/s: 0.00 reconn/s: 0.00
SQL statistics:
    queries performed:
        read:                            139958
        write:                           39988
        other:                           19994
        total:                           199940
    transactions:                        9997   (33.18 per sec.)
    queries:                             199940 (663.60 per sec.)
    ignored errors:                      0      (0.00 per sec.)
    reconnects:                          0      (0.00 per sec.)

General statistics:
    total time:                          301.2969s
    total number of events:              9997

Latency (ms):
         min:                                 13.53
         avg:                                901.57
         max:                               5107.53
         95th percentile:                   2238.47
         sum:                            9012972.28

Threads fairness:
    events (avg/stddev):           333.2333/6.55
    execution time (avg/stddev):   300.4324/0.32

```

# Render

```shell
./plot-sysbench.py -f  oltp_read_write [-f some_other_benchmark_to_compare]
```
