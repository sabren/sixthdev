
from pytypes import Date


def daysInMonthPriorTo(day):
    return (day - day.d).d


def daysInLastMonth():
    return daysInMonthPriorTo(Date("today"))

