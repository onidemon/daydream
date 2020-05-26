import os
import requests
import datetime
import pytz
import pymsteams
import columnize
from dotenv import load_dotenv

load_dotenv()

path = "C:\\vsprojects\\total\\g2\\tickets.txt"

time = pytz.utc.localize(datetime.datetime.now())

headers = {
    "Content-Type": "application/json",
}

response = requests.get(
    "https://g2mobility.freshservice.com/helpdesk/tickets/view/8950.json",
    headers=headers,
    auth=("3ShHmQ9ELyqcs20dMdR", "X"),
)


def fetch_tickets():
    """fetch tickets from freshservice"""
    count = 0
    cpo = ""
    cpo_name = ""
    by = '<a style="color:#3498db">**BY:**</a>'

    with open(path, "w+") as tmp:
        while count < 2:
            if count == 0:
                cpo, cpo_name = "TE 61", "<u>**TE61**</u>"
            elif count == 1:
                cpo, cpo_name = "HPC", "<u>**HPC**</u>"
            print(f"{cpo_name}\r", file=tmp)
            for i in response.json():
                if datetime.datetime.fromisoformat(i["created_at"]).astimezone() < time:
                    if i["custom_field"]["projet_151764"] == cpo:
                        print(
                            '<u style="color:#3498db">**[INC-{}]({})**</u>  **{}**  <a style="color:#3498db">**SUBJECT:**</a> **{}** {}**{:>}**\n'.format(
                                i["display_id"],
                                os.getenv("tickets_url") + str(i["display_id"]),
                                i["created_at"][5:10] + " " + i["created_at"][11:16],
                                i["subject"].strip(),
                                by,
                                str(i["custom_field"]["dupont_et_dupond_151764"]),
                            ),
                            file=tmp,
                        )
            print("-" * 35 + "\n", file=tmp)
            count += 1


def send_to_teams():
    """sends retrieved tickets to MS Teams"""
    teams_post = pymsteams.connectorcard(os.getenv("teams_fs"))
    # create the section
    shifts_section = pymsteams.cardsection()

    # Section Text
    with open(path, "r") as tmp:
        shifts_section.text(tmp.read())

    shifts_section.linkButton(
        "Open Freshservice", "https://g2mobility.freshservice.com/helpdesk/tickets"
    )
    # Section Images
    # g2smart_section.addImage("http://i.imgur.com/c4jt321l.png")

    # Add section to the connector card object before sending
    teams_post.addSection(shifts_section)
    teams_post.text("**Open & Pending**")
    teams_post.send()


fetch_tickets()
send_to_teams()
