import argparse
import asyncio
import time
import aiohttp
import platform
from aiohttp.client import ClientSession
from aiolimiter import AsyncLimiter

M_W = 'https://www.merriam-webster.com'


async def filter_file(infile,
                      outfile,
                      invalid_outfile,
                      connections,
                      max_in_flight,
                      requests_per_second):
    words = []
    not_words = []
    requests_sent = 0
    conn = aiohttp.TCPConnector(limit=connections)
    limiter = AsyncLimiter(requests_per_second, 1)
    async with aiohttp.ClientSession(connector=conn) as session:
        tasks = []
        with open(infile) as f:
            for word in f:
                if requests_sent - (len(words) + len(not_words)) > max_in_flight:
                    await asyncio.gather(*tasks, return_exceptions=True)
                async with limiter:
                    task = asyncio.ensure_future(check_word(
                        session=session,
                        words=words,
                        not_words=not_words,
                        word=word.strip()))
                    tasks.append(task)
                    requests_sent = requests_sent + 1
                    if requests_sent % 1000 == 0:
                        print(f'Queued {requests_sent} requests')
        await asyncio.gather(*tasks, return_exceptions=True)

    print(f'Writing {len(words)} valid words...')
    with open(outfile, 'w') as f_out:
        f_out.write('\n'.join(words))
    if invalid_outfile is not None:
        print(f'Writing {len(not_words)} invalid words...')
        with open(invalid_outfile, 'w') as invalid_out:
            invalid_out.write('\n'.join(not_words))


async def check_word(session: ClientSession, words: list, not_words: list, word: str):
    url = M_W + '/dictionary/' + word
    async with session.head(url) as response:
        if response.status != 404:
            words.append(word)
        else:
            not_words.append(word)


def get_args():
    parser = argparse.ArgumentParser(description=
                                     'Read a newline-delimited file of words and check every word against '
                                     'merriam-webster.com before outputting to a new file')
    parser.add_argument('infile', help='Input wordlist')
    parser.add_argument('outfile', help='Output wordlist')
    parser.add_argument("-i", "--invalid_outfile",
                        help="Output file for invalid words")
    parser.add_argument("-c", "--connections", type=int, default=20,
                        help="Number of TCP connections to make")
    parser.add_argument("-m", "--max_in_flight_requests", type=int, default=3000,
                        help="Max number of requests allowed in flight before waiting for responses")
    parser.add_argument("-r", "--requests_per_second", type=int, default=1000,
                        help="Maximum number of requests to transmit per second")
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    start = time.time()
    asyncio.run(filter_file(args.infile,
                            args.outfile,
                            args.invalid_outfile,
                            args.connections,
                            args.max_in_flight_requests,
                            args.requests_per_second))
    end = time.time()
    print(f'Completed in {end - start:.1f} seconds')
