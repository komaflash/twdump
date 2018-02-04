# -*- coding: utf-8 -*-

import datetime as dt
import logging
from Timer import Timer
from TweetQuery import TweetQuery

# setup logging (will include logs from all used packages)
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', level=logging.INFO)

if __name__ == '__main__':

    #
    # CONFIG BEGIN
    #

    account_file = 'DataSources/accounts.txt'
    output_directory = "DataSets"
    begin = dt.date(2015, 1, 1)
    end = dt.date(2015, 12, 31)

    #
    # CONFIG END
    #

    with open(account_file, 'r') as f:
        handles = f.readlines()

    handles = [h.rstrip('\n') for h in handles]

    timer = Timer()
    for handle in handles:
        timer.start()
        query = TweetQuery(handle, output_directory)
        cnt = query.download_tweets_to_csv(begin, end)
        timer.stop()
        logging.info("SUCCESS (company=%s tweets=%s duration=%s)", handle, cnt, timer.elapsed())
