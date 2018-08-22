Here's what I use to test from scratch (note, the down -v will clear the stored ES data):

`docker-compose down -v ; ES_VERSION=6.3.2 ES_COUNT=1000 ES_URL=http://$(hostname):9200 docker-compose up`

When developing start ElasticSearch: `ES_VERSION=6.3.2 docker-compose up elasticsearch`

then setup the python basics with ```python3 -m venv `pwd`/venv && ./venv/bin/python3 setup.py build install```
and run the test with something like `./venv/bin/locust -f update_load.py -n 1000 -c 10 --no-web --host http://localhost:9200 --no-reset-stats`

Here are some non-scientific outputs from a local run on my laptop:

ES 5.6.10

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

ES 6.2.4
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

ES 6.3.2
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