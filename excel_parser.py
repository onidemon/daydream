
"""Module to read excel sheet, make dict from schedule"""
import datetime
from datetime import timedelta
import random
from openpyxl import load_workbook
# from pprint import pprint


class Planner:
    """gets team schedule from excel file and picks random active member"""
    def __init__(self):
        self.workbook = load_workbook(
            filename="C:\\vsprojects\\total\\g2\\May.xlsx"
        )
        self.sheet = self.workbook.active
        self.rnd = []
        self.today = datetime.datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        self.now = datetime.datetime.now()
        self.this_month = datetime.datetime(self.now.year, self.now.month, 1, hour=0, minute=0, second=0,)
        self.current_time = datetime.time(
            self.now.hour, self.now.minute, self.now.second
        )
        self.current_time2 = datetime.time(13, 30, 0)
        self.shifts = {
            "9-18": (datetime.time(9, 0, 0), datetime.time(18, 0, 0)),
            "12-21": (datetime.time(12, 0, 0), datetime.time(21, 0, 0)),
            "10-14": (datetime.time(10, 0, 0), datetime.time(14, 0, 0)),
            "15-21": (datetime.time(15, 0, 0), datetime.time(21, 0, 0)),
            "DO": (datetime.time(0, 0, 0), datetime.time(0, 0, 0)),
            "CO": (datetime.time(0, 0, 0), datetime.time(0, 0, 0)),
        }
        self.fr_team = {
            self.sheet["D9"].value: {},
            self.sheet["D10"].value: {},
            self.sheet["D11"].value: {},
            self.sheet["D12"].value: {},
            self.sheet["D13"].value: {},
            self.sheet["D14"].value: {},
        }
        self.nl_team = {
            self.sheet["D28"].value: {},
            self.sheet["D29"].value: {},
            self.sheet["D30"].value: {},
        }
        self.de_team = {
            self.sheet["D33"].value: {},
            self.sheet["D34"].value: {},
        }

    def fetch_schedule(self):
        """fill dict from excel sheet"""
        row = 9
        team = self.fr_team
        count = 0

        while True:
            if row == 35:
                break
            elif row == 15:
                row, team = 28, self.nl_team
            elif row == 31:
                row, team = 33, self.de_team

            data = self.sheet["E" + str(row):"AI" + str(row)][0]
            for i in data:
                team[self.sheet["D" + str(row)].value].update(
                    {self.this_month: i.value}
                )
                self.this_month += timedelta(days=1)
            self.this_month = datetime.datetime(self.now.year, self.now.month, 1, hour=0, minute=0, second=0,)
            row += 1
            count += 1

    def daily_schedule(self, team):
        """returns schedule for today"""
        try:
            for key in team:
                print(key, team[key][self.today])
        except KeyError:
            print('')

    def pick_random(self, team):
        """returns random member if currently has active shift"""
        for key in team:
            if (
                    self.shifts[team[key][self.today]][0]
                    <= self.current_time
                    < self.shifts[team[key][self.today]][1]
            ):
                self.rnd.append(key)
        return random.choice(self.rnd)

# P = Planner()
# P.fetch_schedule()
# P.daily_schedule(P.fr_team)
# print('-'*35)
# P.daily_schedule(P.nl_team)
# print('-'*35)
# P.daily_schedule(P.de_team)
# print('-'*35)
# print(P.pick_random())
