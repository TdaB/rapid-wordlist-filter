# Rapid wordlist filter
Rapidly filter a newline-delimited file of words against merriam-webster.com. Uses asyncio and aiolimiter for maximum speed.

370,000+ words from **_words_alpha.txt_** were filtered in 83 minutes (~74 requests per second) with the default configuration.

```
$ python rapid_wordlist_filter.py --help
usage: rapid_wordlist_filter.py [-h] [-i INVALID_OUTFILE] [-c CONNECTIONS] [-m MAX_IN_FLIGHT_REQUESTS] [-r REQUESTS_PER_SECOND] infile outfile

Read a newline-delimited file of words and check every word against www.merriam-webster.com before writing to a new file.

positional arguments:
  infile                Input wordlist
  outfile               Output wordlist

optional arguments:
  -h, --help            show this help message and exit
  -i INVALID_OUTFILE, --invalid_outfile INVALID_OUTFILE
                        Output file for invalid words (default: None)
  -c CONNECTIONS, --connections CONNECTIONS
                        Number of TCP connections to make (default: 20)
  -m MAX_IN_FLIGHT_REQUESTS, --max_in_flight_requests MAX_IN_FLIGHT_REQUESTS
                        Max number of requests allowed in flight before waiting for responses (default: 3000)
  -r REQUESTS_PER_SECOND, --requests_per_second REQUESTS_PER_SECOND
                        Maximum number of requests to transmit per second (default: 1000)
```
