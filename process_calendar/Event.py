import datetime

class Event:
    def __init__(self, event):
        self.description = event["description"]
        self.timezone = event["timezone"]
        self.location = event["location"]
        self.day = int(event["day"])
        self.month = int(event["month"])
        self.year = int(event["year"])
        self.dweek = event["dweek"]
        self.start = event["start"]
        self.end = event["end"]

    def format_date(self):
        return datetime.date(self.year, self.month, self.day)
    def __str__(self):
        return f'Event: {self.description}, Timezone: {self.timezone}, Location: {self.location}, Date: {self.year}/{self.month}/{self.day}, Weekday: {self.dweek}, Time: {self.start}-{self.end}'
    def __repr__(self):
        return f'Event: {self.description}, Timezone: {self.timezone}, Location: {self.location}, Date: {self.year}/{self.month}/{self.day}, Weekday: {self.dweek}, Time: {self.start}-{self.end}
