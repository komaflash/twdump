# -*- coding: utf-8 -*-

import datetime as dt


class Timer(object):
    """A simple timer class"""

    def __init__(self):
        pass

    def start(self):
        """Starts the timer"""
        self.start = dt.datetime.now()
        return self.start

    def stop(self):
        """Stops the timer.  Returns the time elapsed"""
        self.stop = dt.datetime.now()
        return self.stop

    def elapsed(self):
        """Time elapsed since start was called"""
        return self.stop - self.start
