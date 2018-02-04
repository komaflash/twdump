# -*- coding: utf-8 -*-

import datetime as dt


class Timer(object):
    """A simple timer class"""

    def __init__(self):
        pass

    def start(self):
        """Starts the timer"""
        self.begin = dt.datetime.now()
        return self.begin

    def stop(self):
        """Stops the timer.  Returns the time elapsed"""
        self.end = dt.datetime.now()
        return self.end

    def elapsed(self):
        """Time elapsed since start was called"""
        return self.end - self.begin
