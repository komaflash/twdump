# -*- coding: utf-8 -*-

# import datetime as dt
from datetime import date, timedelta, datetime
import calendar


class DateUtils:
    def __init__(self):
        pass

    def get_date_ranges(self, a, b):
        """Get a list of begin and end dates per month"""
        ranges = []

        for x in range(0, self.diff_month(a, b) + 1):
            start_date = self.add_months(a, x)
            last_day_in_month = calendar.monthrange(start_date.year, start_date.month)
            end_date = date(start_date.year, start_date.month, last_day_in_month[1])
            ranges.append(tuple((start_date, end_date)))

        return ranges

    def get_date_ranges_week(self, a, b):
        weeks = []

        for each in self.get_delta(a, b, timedelta(days=1)):
            d = self.week_range(each)
            if d not in weeks:
                weeks.append(d)

        return weeks

    @staticmethod
    def add_months(start, months):
        """Adds n months to start date"""
        month = start.month - 1 + months
        year = start.year + month // 12
        month = month % 12 + 1
        day = min(start.day, calendar.monthrange(year, month)[1])
        return date(year, month, day)

    @staticmethod
    def diff_month(d1, d2):
        """Get the total number of months between d1 and d2"""
        return abs((d1.year - d2.year) * 12 + d1.month - d2.month)

    @staticmethod
    def week_range(d):
        """
        Find the first/last day of the week for the given day.
        Assuming weeks start on Sunday and end on Saturday.
        Returns a tuple of ``(start_date, end_date)``.
        """
        year, week, dow = d.isocalendar()
        if dow == 7:
            start_date = d
        else:
            start_date = d - timedelta(dow)

        end_date = start_date + timedelta(6)
        return start_date, end_date

    def get_delta(self, a, b, delta):
        curr = a
        while curr < b:
            yield curr
            curr += delta