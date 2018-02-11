# -*- coding: utf-8 -*-


from DateUtils import DateUtils
import csv
import datetime as dt
import logging
import re

from twitterscraper import query_tweets


class TweetQuery(object):
    """A simple class that handles the tweet querying with twitterscraper"""

    def __init__(self, account_name, output_dir, mode):
        self.accountName = account_name
        self.output_directory = output_dir

        self.mode = mode
        self.__validate_mode__()

        # pre-compiled regular expression to extract hashtags from a string.
        self.regexHashTag = re.compile('#[a-zA-Z0-9]+', re.IGNORECASE)

    def download_tweets_to_csv(self, date_begin, date_end):
        logging.debug("Getting tweets for %s from %s till %s", self.accountName, date_begin, date_end)

        # we'll query the api per month.
        # we calculated the start and end dates
        # of each month between begin and end
        util = DateUtils()

        if self.mode == "monthly":
            date_ranges = util.get_date_ranges(date_begin, date_end)
        else:
            date_ranges = util.get_date_ranges_week(date_begin, date_end)

        # create the file name
        file_name = self.__get_output_file_name__()

        # initialize counter
        tweet_count = 0

        # open the csv file
        with open(file_name, 'a') as fw:
            writer = csv.writer(fw, dialect='excel')

            # write header
            writer.writerow(
                ["fullname", "id", "likes", "replies", "retweets", "text", "timestamp", "url", "user", "hashtags"])

            # for each range:
            #   query tweets
            #   write them to csv
            for date_start, date_end in date_ranges:
                retry = 1
                retry_max = 3

                while retry <= retry_max:
                    try:
                        tweet_query = query_tweets("from:" + self.accountName,
                                                   limit=100000,
                                                   begindate=date_start,
                                                   enddate=date_end,
                                                   poolsize=20,
                                                   lang='')

                        # if we reach here, everything is
                        # all right and we want to leave the loop
                        retry = retry_max + 1
                    except Exception as err:
                        logging.warning(
                            "Query from {date_start} to {date_end} failed. Retry {retry} of {retry_max} (Error: {})",
                            date_start, date_end, retry, retry_max, str(err))
                        retry = retry + 1

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
                                         self.__extract_hash_tags__(tweet.text)])
                    except Exception as ex:
                        logging.error("Failed to process tweet. \n tweet=%s \n error=%s ", self.tweet_to_log(tweet),
                                      str(ex))

        return tweet_count

    def __validate_mode__(self):
        if self.mode == "weekly" or self.mode == "monthly":
            return

        raise ValueError('mode must be weekly or monthly')

    def __get_output_file_name__(self):
        """Create the file name which contains the account name"""
        return self.output_directory + '/tweetquery-' + self.accountName + '.csv'

    def __normalize_text__(self, text):
        """Apply proper normalization of the tweet next here"""
        return text.replace('\n', ' ').replace('\r', '')

    def __extract_hash_tags__(self, text):
        """Extracts #hashtags from a string and returns them as online, separated by slash
        :param text: tweet text
        :return: For example hashtag1/hashtag2/hashtag3
        """
        findings = self.regexHashTag.findall(text)

        if len(findings) <= 0:
            return ""

        logging.debug(findings)
        return '/'.join(str(x).replace("#", "") for x in findings)

    def tweet_to_log(self, tweet):
        return str([tweet.user, tweet.id, tweet.timestamp, tweet.url, tweet.user, len(tweet.text)])
