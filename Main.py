# -*- coding: utf-8 -*-

import datetime as dt
import logging

from Timer import Timer
from TweetQuery import TweetQuery

# setup logging (will include logs from all used packages)
logging.basicConfig(format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    level=logging.INFO, filename='tweetQuery.log')


if __name__ == '__main__':

    #
    # CONFIG BEGIN
    #

    # account_file = 'DataSources/company_names.txt'
    account_file = 'DataSources/notweets_test.txt'
    output_directory = "DataSets"
    begin = dt.date(2010, 1, 1)
    end = dt.date(2017, 12, 31)

    #
    # CONFIG END
    #

    with open(account_file, 'r') as f:
        handles = f.readlines()

    handles = [h.rstrip('\n') for h in handles]

    timer = Timer()
    for handle in handles:
        timer.start()
        # query = TweetQuery(handle, output_directory, "weekly")
        query = TweetQuery(handle, output_directory, "monthly")
        cnt = query.download_tweets_to_csv(begin, end)
        timer.stop()
        logging.info("SUCCESS (company=%s tweets=%s duration=%s)", handle, cnt, timer.elapsed())
