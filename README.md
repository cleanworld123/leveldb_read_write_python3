# dumpleveldb

Dumps the content of a leveldb to stdout and into 3 different dat files (str4files, decoded and uncoded content) to the current working directory.

Use `leveldbdump.py -d ../../path/to/leveldb`

## dependencies
`pip install leveldb`

## how to
```
$ ./leveldbdump.py --help
usage: leveldbdump.py [-h] [-d LEVEL_DB_PATH]

leveldbdump.py dumps the content of a leveldb to stdout and into 3 different
dat files (str4files, decoded and uncoded content) to the current working
directory. Use `leveldbdump.py -d ../../path/to/leveldb` or it will create a
dump of './leveldb' - https://github.com/bithon/python-leveldbdump

optional arguments:
  -h, --help            show this help message and exit
  -d LEVEL_DB_PATH, --db-path LEVEL_DB_PATH
                        Path to database directory

```

```
$ sudo ./leveldbdump.py -d ../path-to-app/lib/leveldb
===================== BEGIN ====================
1
key: graceful_shutdown
value:disabled

====================== END =====================
===================== BEGIN ====================
1
key: b'trigger_graceful_shutdown'
value:b'disabled'

====================== END =====================
Begin print undecoded record, total:0 

End print undecoded record.
```

```
$ ls -l
-rw-r--r-- 1 root   root    157 Mär  2 23:06 leveldbdump.py_decodedCookieContent.dat
-rw-r--r-- 1 root   root    165 Mär  2 23:06 leveldbdump.py_str4bytesCookieContent.dat
-rw-r--r-- 1 root   root      0 Mär  2 23:06 leveldbdump.py_undecodedCookieContent.dat
```