import os
import json
from datetime import datetime, timedelta
import requests
import pymsteams
import pytz
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from refresh_token import get_refresh_token
from excel_parser import Planner

load_dotenv()

cred = credentials.Certificate(os.getenv("fire_key"))
firebase_admin.initialize_app(cred)


class G2SmartBot:
    """Bot that fetches alerts from G2Smart page"""

    def __init__(self,):
        self.P = Planner()
        self.location = ""
        self.dic = {}
        self.time = pytz.utc.localize(datetime.now())
        self.cpo = {
            "HPC France": "cpo=total_fr_hpc",
            "HPC Netherlands": "cpo=total_nl_hpc",
            "TE61": "cpo=te61",
        }

    def parse_url(self, loc=None):
        """Parses the url and adds specified parameters to dic"""
        self.location = loc
        headers = {
            "Host": "www.g2smart.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.g2smart.com/g2smart/alert?status=Opened",
            "Authorization": "Bearer "
            + get_refresh_token(
                os.getenv("client_id"),
                os.getenv("client_secret"),
                os.getenv("refresh_token"),
            ),
            "Connection": "keep-alive",
        }
        session = requests.session()
        resp = session.get(
            os.getenv("url") + self.cpo[loc] + "&" + "status=Opened&limit=50&page=1",
            headers=headers,
        )
        for i in resp.json()["items"]:
            if datetime.fromisoformat(
                i["openDate"].replace("Z", "+00:00")
            ).astimezone() > self.time - timedelta(days=1):
                if i["initiatorEvent"]["type"] != "STATUS_NOTIFICATION":
                    self.dic[i["_id"]] = {
                        "Location": i["locationName"],
                        "Charger": i["equipmentId"],
                        "Alert_Status": i["status"],
                        "Open_Date": datetime.fromisoformat(
                            i["openDate"].replace("Z", "+00:00")
                        ).astimezone(),
                        "Alert_Details": i["initiatorEvent"]["type"],
                    }
                else:
                    self.dic[i["_id"]] = {
                        "Location": i["locationName"],
                        "Charger": i["equipmentId"],
                        "Alert_Status": i["status"],
                        "Open_Date": datetime.fromisoformat(
                            i["openDate"].replace("Z", "+00:00")
                        ).astimezone(),
                        "Alert_Details": i["initiatorEvent"]["details"]["status"],
                    }
        print(resp)

    def write_json(self):
        """Dumps the contents of self.dic to a json file"""
        with open("alerts.json", "w+") as f:
            json.dump(self.dic, f)

    def send_to_teams(self):
        """sends retrieved alerts if any to MS Teams"""
        data_base = firestore.client()
        doc_ref = data_base.collection("Alerts").document(self.location)
        doc = doc_ref.get()
        teams_post = pymsteams.connectorcard(os.getenv("teams"))
        # create the section
        g2smart_section = pymsteams.cardsection()

        # Section Title
        self.P.fetch_schedule()
        g2smart_section.title(f"<strong>Assigned to: <a>{self.P.pick_random(self.P.fr_team)}</a></strong>")

        # Activity Elements
        g2smart_section.activityTitle("CPO:  " + self.location)
        # g2smart_section.activitySubtitle("Current open alerts")
        g2smart_section.activityImage(
            "https://emobilify.com/wp-content/uploads/company-logos/g2mobility.png"
        )
        # g2smart_section.activityText("This is my activity Text")

        # Facts are key value pairs displayed in a list.
        # g2smart_section.addFact("key", "value"')

        # Section Text
        with open("temp.txt", "w+") as tmp:
            for key in self.dic:
                if doc.to_dict() is None or key not in doc.to_dict():
                    print(
                        f'**{self.dic[key]["Location"]}** '
                        f'{str(self.dic[key]["Open_Date"])[0:19]} '
                        f'{self.dic[key]["Alert_Details"]} '
                        f'[{self.dic[key]["Charger"]}]({os.getenv("equip_url")}{self.dic[key]["Charger"]}) '
                        f'{self.dic[key]["Alert_Status"][0:4]}\n',
                        file=tmp,
                    )
                else:
                    print(f"{key} alread sent")
            tmp.seek(0)
            g2smart_section.text(tmp.read())
        g2smart_section.linkButton(
            "Open Ticket", "https://g2mobility.freshservice.com/helpdesk/tickets/new",
        )
        # Section Images
        # g2smart_section.addImage("http://i.imgur.com/c4jt321l.png")

        # Add section to the connector card object before sending
        teams_post.addSection(g2smart_section)
        teams_post.text("Open alerts")

        with open("temp.txt", "r+") as read_obj:
            one_char = read_obj.read(1)
            if not one_char:
                print("empty")
            else:
                teams_post.send()
        doc_ref.set(self.dic, merge=True)
        self.dic = {}


s = G2SmartBot()
# s.parse_url("TE61")
# s.send_to_teams()
s.parse_url("HPC France")
s.send_to_teams()
