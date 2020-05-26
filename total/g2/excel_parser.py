
"""Module to read excel sheet, make dict from schedule"""
import datetime
from datetime import timedelta
import random
from openpyxl import load_workbook
import os
from dotenv import load_dotenv
import pymsteams
# from pprint import pprint

load_dotenv()


class Planner:
    """gets team schedule from excel file and picks random active member"""
    def __init__(self):
        self.path = "C:\\vsprojects\\total\\g2\\shifts.txt"
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
            "9-13": (datetime.time(9, 0, 0), datetime.time(13, 0, 0)),
            "9-16": (datetime.time(9, 0, 0), datetime.time(16, 0, 0)),
            "10-14": (datetime.time(10, 0, 0), datetime.time(14, 0, 0)),
            "12-21": (datetime.time(12, 0, 0), datetime.time(21, 0, 0)),
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

    def schedule_all(self):
        """returns schedule for today"""
        team = self.fr_team
        tname = ""
        count = 0

        with open(self.path, 'w+') as tmp:
            while count < 3:
                if count == 0:
                    team = self.fr_team
                    tname = "**<u>FR Team**</u>"
                elif count == 1:
                    team = self.nl_team
                    tname = "<u>**NL Team**</u>"
                elif count == 2:
                    team = self.de_team
                    tname = "**<u>DE Team**</u>"
                print(f'{tname}\r', file=tmp)
                for key in team:
                    if not None:
                        print(f'**<a>{key}</a>, {team[key][self.today]}**\n', file=tmp)
                print('-' * 35 + '\n', file=tmp)
                count += 1

    def schedule_team(self, team):
        try:
            for key in team:
                if not None:
                    print(key, team[key][self.today])
        except KeyError:
            print(" ")

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

    def send_to_teams(self):
        """sends retrieved alerts if any to MS Teams"""
        teams_post = pymsteams.connectorcard(os.getenv("teams_shifts"))
        # create the section
        shifts_section = pymsteams.cardsection()

        # Section Text
        with open(self.path, 'r') as tmp:
            shifts_section.text(tmp.read())

        # shifts_section.linkButton()
        # Section Images
        # g2smart_section.addImage("http://i.imgur.com/c4jt321l.png")

        # Add section to the connector card object before sending
        teams_post.addSection(shifts_section)
        teams_post.text("**Today's shifts**")
        teams_post.send()
