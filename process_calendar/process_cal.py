from datetime import datetime
import sys
from typing import Dict, List
import re
from Event import *

events = []
days = {}

def main():
    # boundary dates
    t1 = sys.argv[1]
    t2 = sys.argv[2]
    
    # open xml file
    filename = sys.argv[3]
    fp = open(filename, "r")
    parse_file(fp)
    
    # create date objects
    d1 = parse_date(t1)
    d2 = parse_date(t2)
    compare_dates(d1, d2)
    output()


def parse_file(fp):
    global events
    line = True
    curEvent = {}

    while line:
        # read line and split into token and value
        line = fp.readline()
        cur = re.split("[/<>\n]", line)[1:3]
        if len(cur) == 0:
            return

        token = cur[0]
        value = cur[1]

        if len(token) == 0 and len(curEvent) != 0:
            # create an event using the information
            event = Event(curEvent)
            events.append(event)
            curEvent = {}

        elif token != 'calendar' and token != 'event':
            # add token to the existing event
            curEvent[token] = value


def parse_date(date):
    # create a date object
    dateArr = date.split('/')
    return datetime.date(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]))


def compare_dates(d1, d2):
    # checks for events within the date range
    global events
    global days

    # if the dates are in the date range, add to days
    for event in events:
        date = event.format_date()
        if date <= d2 and date >= d1:
            if date not in days:
                days[date] = [event]
            else:
                days[date].append(event)

def output():
    global days

    # if there are no more days, return
    if len(days) == 0:
        return

    while len(days) != 0:
        # find the earliest date
        curEvents = min(days)
        curDays = days[curEvents]
        days.pop(curEvents)

        # print this date
        d = datetime.datetime.strptime(f'{curDays[0].format_date()}',"%Y-%m-%d")
        print(d.strftime(f"%B %d, %Y ({curDays[0].dweek})"))

        times = {}
        # create an array of the times on this day
        for event in curDays:
            time = event.start
            if time not in times:
                # create new time block
                times[time] = [event]
            else:
                # add to existing time block
                times[time].append(event)
        compare_times(curDays, times)
        print("")


def compare_times(curEvents, times):
    global events

    while len(times) != 0:
        # find the lowest time
        low = min(times)
        event = times[low] 
        # print all events at this time
        for e in event:
            print_date(e)
            curEvents.remove(e)
            events.remove(e)
            
        # remove time
        del times[low]
        

        


def print_date(event):
    # format and print the given event
    startTime = convert(event.start)
    endTime = convert(event.end)
    print(f'{startTime} to {endTime}: {event.description} {{{{{event.location}}}}} | {event.timezone}')


def convert(time):
    # converts the time from 24 to 12 hour
    twelve = datetime.datetime.strptime(time, "%H:%M")
    return twelve.strftime("%I:%M %p")

if __name__ == '__main__':
    main()
