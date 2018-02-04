# -*- coding: utf-8 -*-

from twitterscraper import query_tweets
from json import JSONDecodeError
import csv
import datetime as dt
import calendar
import logging
import re


class TweetQuery(object):
    """A simple class that handles the tweet querying with twitterscraper"""

    def __init__(self, account_name, output_dir):
        self.accountName = account_name
        self.output_directory = output_dir

        # pre-compiled regular expression to extract hashtags from a string.
        self.regexHashTag = re.compile('#[a-zA-Z0-9]+', re.IGNORECASE)

    def download_tweets_to_csv(self, date_begin, date_end):
        logging.debug("Getting tweets for %s from %s till %s", self.accountName, date_begin, date_end)

        # we'll query the api per month.
        # we calculated the start and end dates
        # of each month between begin and end
        ranges = self.__get_date_ranges__(date_begin, date_end)

        # create the file name
        file_name = self.__get_output_file_name__()

        # initialize counter
        tweet_count = 0

        # open the csv file
        with open(file_name, 'w') as fw:
            writer = csv.writer(fw)

            # write header
            writer.writerow(
                ["fullname", "id", "likes", "replies", "retweets", "text", "timestamp", "url", "user", "hashtags"])

            # for each range:
            #   query tweets
            #   write them to csv
            for range in ranges:
                retry = 1
                retry_max = 3

                while retry <= retry_max:
                    try:
                        tweet_query = query_tweets("from:" + self.accountName,
                                                   limit=100000,
                                                   begindate=range[0],
                                                   enddate=range[1],
                                                   poolsize=5,
                                                   lang='')

                        # if we reach here, everything is
                        # all right and we want to leave the loop
                        retry = retry_max+1
                    except JSONDecodeError as err:
                        logging.warning("Query failed, try %s/%s (%s)", retry, retry_max, str(err))
                        retry = retry+1

                tweet_count = tweet_count + len(tweet_query)

                for tweet in tweet_query:
                    try:
                        writer.writerow([tweet.fullname,
                                         tweet.id,
                                         tweet.likes,
                                         tweet.replies,
                                         tweet.retweets,
                                         self.__normalize_text__(tweet.text),
                                         tweet.timestamp,
                                         tweet.url,
                                         tweet.user,
                                         self.__extractHashTags__(tweet.text)])
                    except Exception as ex:
                        logging.error("Failed to process tweet. \n tweet_text=%s \n error=%s ", tweet.id, str(ex))

        fw.close()
        return tweet_count

    def __get_date_ranges__(self, a, b):
        """Get a list of begin and end dates per month"""
        ranges = []

        for x in range(0, self.__diff_month__(a, b) + 1):
            start_date = self.__add_months__(a, x)
            last_day_in_month = calendar.monthrange(start_date.year, start_date.month)
            end_date = dt.date(start_date.year, start_date.month, last_day_in_month[1])
            ranges.append(tuple((start_date, end_date)))

        return ranges

    def __add_months__(self, start, months):
        """Adds n months to start date"""
        month = start.month - 1 + months
        year = start.year + month // 12
        month = month % 12 + 1
        day = min(start.day, calendar.monthrange(year, month)[1])
        return dt.date(year, month, day)

    def __diff_month__(self, d1, d2):
        """Get the total number of months between d1 and d2"""
        return abs((d1.year - d2.year) * 12 + d1.month - d2.month)

    def __get_output_file_name__(self):
        """Create the file name which contains the account name"""
        return self.output_directory + '/tweetquery-' + self.accountName + '.csv'

    def __normalize_text__(self, text):
        """Apply proper normalization of the tweet next here"""
        return text.replace('\n', ' ').replace('\r', '')

    def __extractHashTags__(self, text):
        """Extracts #hashtags from a string and returns them as online, separated by slash
        :param text: tweet text
        :return: For example hashtag1/hashtag2/hashtag3
        """
        findings = self.regexHashTag.findall(text)

        if len(findings) <= 0:
            return ""

        logging.debug(findings)
        return '/'.join(str(x).replace("#", "") for x in findings)
