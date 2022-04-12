# Rapid wordlist filter
Rapidly filter a newline-delimited file of words against merriam-webster.com. Uses ayncio and aiolimiter for maximum speed.

370,000+ words from words_alpha.txt were filtered in 83 minutes.

```
$ python rapid_wordlist_filter.py --help
usage: rapid_wordlist_filter.py [-h] [-i INVALID_OUTFILE] [-c CONNECTIONS]
                                [-m MAX_IN_FLIGHT_REQUESTS]
                                [-r REQUESTS_PER_SECOND]
                                infile outfile

Read a newline-delimited file of words and check every word against merriam-
webster.com before outputting to a new file

positional arguments:
  infile                Input wordlist
  outfile               Output wordlist

options:
  -h, --help            show this help message and exit
  -i INVALID_OUTFILE, --invalid_outfile INVALID_OUTFILE
                        Output file for invalid words
  -c CONNECTIONS, --connections CONNECTIONS
                        Number of TCP connections to make
  -m MAX_IN_FLIGHT_REQUESTS, --max_in_flight_requests MAX_IN_FLIGHT_REQUESTS
                        Max number of requests allowed in flight before
                        waiting for responses
  -r REQUESTS_PER_SECOND, --requests_per_second REQUESTS_PER_SECOND
                        Maximum number of requests to transmit per second
```
