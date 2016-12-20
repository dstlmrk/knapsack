# The knapsack problem

Implementation of several algorithms for solving 1/0 knapsack problem.

## Usage

Input path is expected. For example `./inst/knap_4.inst.dat` is used solution in `./sol/knap_4.sol.dat`.

```
Usage: main.py [OPTIONS]

Options:
  --method TEXT                   bruteforce / ratio / bb / dynamic / fptas /
                                  sa (simulated annealing) / all (without sa)
                                  [bruteforce]
  --path TEXT                     Input file. [./inst/knap_4.inst.dat]
  --relative-error FLOAT          Relative error for FPTAS alg. [0.5]
  --solution / --no-solution      If solution file is available or not. [True]
  --time-test / --no-time-test    It returns avg time only. [False]
  --error-test / --no-error-test  It returns avg relative error only. [False]
  -v, --verbose / --no-verbose    [False]
  -t, --temperature INTEGER       Init temperature for simulated annealing.
                                  [1000]
  -c, --cooling FLOAT             Cooling for simulated annealing. [0.9]
  -i, --inner-loop INTEGER        Number of iterations in inner loop for
                                  simulated annealing. [5]
  --help                          Show this message and exit.
```

## Example of output
```
$ ./main.py --method sa --path ./data/inst/knap_10.inst.dat -v -i 50 -c 0.92 -t 100
OK      798 [0, 1, 1, 0, 0, 1, 1, 1, 0, 1]
OK      942 [1, 1, 1, 0, 1, 1, 1, 1, 0, 1]
OK      740 [0, 1, 1, 1, 0, 0, 1, 1, 1, 1]
OK      956 [1, 1, 1, 1, 1, 0, 1, 0, 1, 0]
OK     1501 [1, 1, 1, 1, 1, 0, 1, 1, 1, 0]
OK     1351 [1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
FAIL   1233 [1, 1, 1, 1, 1, 1, 1, 0, 0, 0] != 1375 [1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
OK     1153 [0, 1, 1, 1, 0, 1, 1, 1, 1, 1]
FAIL   1220 [1, 1, 1, 0, 0, 1, 1, 1, 1, 0] != 1234 [1, 0, 1, 0, 1, 1, 1, 1, 1, 0]
FAIL   1183 [1, 1, 1, 0, 1, 1, 1, 0, 0, 1] != 1260 [1, 0, 1, 1, 1, 0, 0, 1, 1, 1]
OK     1319 [1, 1, 1, 0, 1, 1, 0, 0, 1, 1]
OK     1169 [1, 1, 1, 1, 1, 1, 0, 1, 1, 1]
FAIL     90 [1, 1, 1, 1, 1, 1, 1, 1, 1, 0] != 99 [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
OK     1023 [0, 1, 1, 1, 1, 1, 1, 1, 0, 0]
OK     1389 [1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
OK     1168 [0, 1, 0, 1, 0, 1, 1, 0, 0, 1]
OK     1024 [1, 1, 0, 1, 0, 1, 1, 1, 1, 1]
OK     1195 [1, 1, 1, 1, 0, 0, 1, 0, 1, 1]
OK      872 [1, 1, 1, 1, 1, 1, 0, 1, 0, 0]
OK     1099 [1, 1, 1, 0, 1, 0, 1, 1, 1, 0]
OK     1286 [0, 0, 1, 1, 1, 1, 1, 1, 1, 1]
OK     1178 [0, 1, 1, 1, 1, 1, 1, 0, 0, 1]
FAIL   1192 [1, 1, 0, 1, 1, 0, 1, 1, 1, 1] != 1217 [1, 1, 0, 1, 0, 1, 0, 1, 1, 1]
FAIL    911 [0, 1, 0, 1, 1, 1, 0, 0, 1, 0] != 939 [1, 0, 0, 1, 1, 1, 1, 0, 1, 1]
FAIL    756 [0, 1, 1, 1, 1, 0, 0, 1, 1, 0] != 784 [1, 1, 1, 1, 0, 0, 0, 1, 1, 0]
OK     1240 [1, 1, 1, 1, 0, 0, 1, 1, 1, 1]
OK      917 [1, 0, 1, 1, 1, 1, 0, 1, 0, 0]
OK     1033 [1, 1, 0, 1, 1, 1, 1, 0, 1, 0]
FAIL   1336 [1, 1, 0, 1, 1, 1, 1, 1, 1, 0] != 1386 [1, 1, 1, 1, 1, 1, 0, 1, 1, 1]
OK     1266 [0, 1, 1, 1, 1, 1, 1, 1, 0, 1]
FAIL    981 [1, 1, 1, 1, 0, 0, 1, 1, 0, 0] != 1054 [1, 1, 1, 0, 0, 0, 1, 1, 1, 0]
FAIL    963 [1, 1, 0, 1, 1, 1, 0, 0, 0, 1] != 980 [1, 1, 0, 0, 1, 1, 0, 1, 0, 0]
FAIL    873 [1, 0, 0, 1, 0, 0, 0, 1, 1, 1] != 952 [1, 1, 0, 0, 0, 0, 1, 1, 1, 1]
FAIL   1331 [1, 1, 1, 1, 1, 1, 1, 0, 1, 0] != 1446 [1, 0, 1, 1, 1, 1, 1, 1, 1, 1]
OK     1196 [1, 0, 0, 1, 1, 1, 1, 1, 1, 1]
OK     1062 [1, 1, 0, 1, 1, 0, 1, 0, 1, 1]
OK      748 [1, 1, 1, 1, 1, 0, 0, 0, 1, 0]
FAIL    861 [0, 0, 1, 0, 1, 0, 1, 1, 0, 1] != 1059 [1, 0, 1, 1, 1, 0, 1, 1, 0, 0]
OK     1578 [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
FAIL    600 [1, 1, 0, 1, 1, 0, 0, 0, 1, 1] != 694 [1, 0, 1, 1, 1, 0, 1, 0, 1, 1]
FAIL   1115 [1, 1, 1, 1, 1, 1, 0, 1, 1, 1] != 1143 [1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
OK     1043 [1, 1, 0, 1, 1, 1, 1, 1, 1, 1]
OK     1436 [1, 1, 1, 1, 1, 0, 1, 1, 1, 1]
OK     1368 [0, 1, 1, 1, 1, 1, 1, 1, 1, 1]
OK     1315 [0, 1, 1, 1, 1, 1, 0, 1, 0, 1]
OK     1005 [1, 1, 1, 1, 0, 0, 1, 1, 0, 1]
OK     1187 [1, 1, 1, 1, 1, 0, 1, 1, 0, 1]
OK      959 [1, 1, 1, 0, 1, 1, 1, 1, 1, 0]
OK      925 [0, 1, 1, 1, 0, 0, 1, 1, 1, 0]
OK     1243 [1, 1, 1, 1, 1, 1, 1, 0, 0, 1]
----------------------------------
= sa
average duration       = 27.473478 ms
average relative error = 1.969642 %
    max relative error = 18.696884 %
----------------------------------
```