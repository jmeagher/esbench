# ElasticSearch performance for updates

This is a simple benchmark to test the performance of ElasticSearch versions under a heavy "update" workload. Starting with ElasticSearch 5 there is a significant performance penalty for updates. These appear to be fixed in 6.3 with the changes from https://github.com/elastic/elasticsearch/issues/26802 and https://github.com/elastic/elasticsearch/pull/29264.

# Instructions

Here's what I use to test from scratch (note, the down -v will clear the stored ES data):

`docker-compose down -v ; ES_VERSION=6.3.2 ES_COUNT=1000 ES_URL=http://$(hostname):9200 docker-compose up`

When developing start ElasticSearch: `ES_VERSION=6.3.2 docker-compose up elasticsearch`

then setup the python basics with ```python3 -m venv `pwd`/venv && ./venv/bin/python3 setup.py build install```
and run the test with something like `./venv/bin/locust -f update_load.py -n 1000 -c 10 --no-web --host http://localhost:9200 --no-reset-stats`


# Larger batch updates tens per update

## ES 2.4.6

````
$ docker-compose down -v ; IMAGE_BASE=elasticsearch ES_VERSION=2.4.6 ES_COUNT=2000 ES_URL=http://$(hostname):9200 docker-compose up
...
Percentage of the requests completed within given times
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
--------------------------------------------------------------------------------------------------------------------------------------------
 POST bulk_update                                                 1882    100    120    120    130    150    160    190    350    407
 PUT create                                                         65     14     18     20     23     25     27     41    860    864
 GET fetch                                                          45      7      9     10     12     16     21     24     24     24
 GET wait_for_startup                                               10     15     20     21     22    120    120    120    120    117
````

## ES 5.6.10

````
$ docker-compose down -v ; ES_VERSION=5.6.10 ES_COUNT=2000 ES_URL=http://$(hostname):9200 docker-compose up
...
Percentage of the requests completed within given times
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
--------------------------------------------------------------------------------------------------------------------------------------------
 POST bulk_update                                                 1858    410    480    530    550    600    660    740    800    921
 PUT create                                                         65    350    400    470    490    550    590   1300   1300   1302
 GET fetch                                                          47     10     17     19     21     29     31     47     47     47
 GET wait_for_startup                                               10     24     24     28    280    280    280    280    280    278
````

## ES 6.2.4

````
$ docker-compose down -v ; ES_VERSION=6.2.4 ES_COUNT=2000 ES_URL=http://$(hostname):9200 docker-compose up
...
Percentage of the requests completed within given times
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
--------------------------------------------------------------------------------------------------------------------------------------------
 POST bulk_update                                                 1851    410    470    510    530    590    630    680    730    904
 PUT create                                                         73    320    360    400    440    520    590    890    910    911
 GET fetch                                                          30     18     22     25     30     36     41     44     44     44
 GET wait_for_startup                                               10     28     58     74    420    450    450    450    450    449
````

## ES 6.3.2

````
$ docker-compose down -v ; ES_VERSION=6.3.2 ES_COUNT=2000 ES_URL=http://$(hostname):9200 docker-compose up
...
Percentage of the requests completed within given times
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
--------------------------------------------------------------------------------------------------------------------------------------------
 POST bulk_update                                                 1868    110    120    130    140    160    200    260    300    410
 PUT create                                                         71     96    110    120    130    180    510   1100   1100   1139
 GET fetch                                                          37     82     91    100    120    160    190    190    190    193
 GET wait_for_startup                                               10     35     47     60    410    430    430    430    430    430
````

# Small batch update results

Initial results on my laptop with single digit size updates

## ES 2.4.6


````
$ docker-compose down -v ; IMAGE_BASE=elasticsearch ES_VERSION=2.4.6 ES_COUNT=2000 ES_URL=http://$(hostname):9200 docker-compose up
...
Percentage of the requests completed within given times
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
--------------------------------------------------------------------------------------------------------------------------------------------
 POST bulk_update                                                 1873     30     39     50     58     88    130    280    360    494
 PUT create                                                         73     24     29     37     43     81    140    330   1100   1110
 GET fetch                                                          45     14     18     27     29     49     67    160    160    163
 GET wait_for_startup                                               10     36     41     42     83    120    120    120    120    121
````

## ES 5.6.10

````
$ docker-compose down -v ; ES_VERSION=5.6.10 ES_COUNT=2000 ES_URL=http://$(hostname):9200 docker-compose up
...

Percentage of the requests completed within given times
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
--------------------------------------------------------------------------------------------------------------------------------------------
 POST bulk_update                                                 1874     87    110    130    140    180    220    270    300    428
 PUT create                                                         59     64     87    110    120    200    340   1000   1700   1729
 GET fetch                                                          36     17     26     43     48     59    110    130    130    128
````

## ES 6.2.4
````
$ docker-compose down -v ; ES_VERSION=6.2.4 ES_COUNT=2000 ES_URL=http://$(hostname):9200 docker-compose up
...
Percentage of the requests completed within given times
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
--------------------------------------------------------------------------------------------------------------------------------------------
 POST bulk_update                                                 1859     83    100    110    120    150    170    210    220    339
 PUT create                                                         70     78     96    110    120    200    220    770    820    822
 GET fetch                                                          44     16     26     36     41     49     66     77     77     77
 GET wait_for_startup                                               10     32     47     50    410    450    450    450    450    452
````

## ES 6.3.2
````
$ docker-compose down -v ; ES_VERSION=6.3.2 ES_COUNT=2000 ES_URL=http://$(hostname):9200 docker-compose up
...
Percentage of the requests completed within given times
 Name                                                           # reqs    50%    66%    75%    80%    90%    95%    98%    99%   100%
--------------------------------------------------------------------------------------------------------------------------------------------
 POST bulk_update                                                 1862     37     45     51     55     69     81     96    110    389
 PUT create                                                         68     34     43     52     55     63    170    840    860    865
 GET fetch                                                          48    110    120    140    150    200    200    250    250    248
 GET wait_for_startup                                               10     34     50     61    370    380    380    380    380    375
````