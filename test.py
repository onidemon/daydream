import requests
import json
import pymsteams
from datetime import datetime, timedelta
import pytz
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
from dotenv import load_dotenv
import os
env_path = Path("C:\\Users\\DayDream\\total") / '.env'
load_dotenv(dotenv_path=env_path)

cred = credentials.Certificate("C:\\Users\\DayDream\\firestore_key.json")
firebase_admin.initialize_app(cred)


class G2SmartBot:
    """Bot that fetches alerts from G2Smart page"""

    def __init__(self):
        self.db = firestore.client()
        self.doc_ref = self.db.collection("Alerts").document("France")
        self.doc = self.doc_ref.get()
        self.dic = {}
        self.location = ""
        self.cpo = {"Location":
            {"HPC France": "cpo=total_fr_hpc",
            "HPC Netherlands": "cpo=otal_nl_hpc",
            "TE61": "cpo=te61"}
            }
        
    
        self.time = pytz.utc.localize(datetime.now())
        self.headers = {
            "Host": "www.g2smart.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Authorization": os.getenv("token"),
            "Connection": "keep-alive",
        }
        self.resp = requests.get(
            os.getenv("url")
            + "status=Opened&limit=50&page=1",
            headers=self.headers,
        )
        print(self.resp)

    def parse_url(self):
        """Parses the url and adds specified parameters to dic"""
        self.resp = requests.get(
            os.getenv("url")
            + self.cpo["Location"][self.location]
            +"&"
            + "status=Opened&limit=50&page=1",
            headers=self.headers,
        )
        for i in self.resp.json()["items"]:
            if datetime.fromisoformat(
                i["openDate"].replace('Z', '+00:00')).astimezone() > self.time - timedelta(days=1):
                if i["initiatorEvent"]["type"] != "STATUS_NOTIFICATION":
                    self.dic[i["_id"]] = {
                        "Location": i["locationName"],
                        "Charger": i["equipmentId"],
                        "Alert_Status": i["status"],
                        "Open_Date": datetime.fromisoformat(
                            i["openDate"].replace('Z', '+00:00')).astimezone(),
                        "Alert_Details": i["initiatorEvent"]["type"]
                    }
                else:
                    self.dic[i["_id"]] = {
                        "Location": i["locationName"],
                        "Charger": i["equipmentId"],
                        "Alert_Status": i["status"],
                        "Open_Date": datetime.fromisoformat(
                            i["openDate"].replace('Z', '+00:00')).astimezone(),
                        "Alert_Details": i["initiatorEvent"]["details"]["status"]
                    }
        
        # self.doc_ref.set(self.dic)


    def write_file(self):
        """Dumps the contents of self.dic to a json file"""
        with open("alerts.json", "w") as f:
            json.dump(self.dic, f)

    def send_to_teams(self):
        """sends retrieved alerts if any to MS Teams"""
        teams_post = pymsteams.connectorcard(
            os.getenv("teams")
        )
        # create the section
        g2smart_section = pymsteams.cardsection()

        # Section Title
        g2smart_section.title("G2 Open Alerts")

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
            for key in self.dic.keys():
                print(
                    f'{self.dic[key]["Location"]} '
                    f'{str(self.dic[key]["Open_Date"])[0:19]} '
                    f'{self.dic[key]["Alert_Details"]} '
                    f'{self.dic[key]["Charger"]} '
                    f'{self.dic[key]["Alert_Status"][0:4]}\n',
                    file=tmp,
                )
            tmp.seek(0)
            g2smart_section.text(tmp.read())

        # Section Images
        # g2smart_section.addImage("http://i.imgur.com/c4jt321l.png")

        # Add section to the connector card object before sending
        teams_post.addSection(g2smart_section)
        teams_post.text("Test")
        self.dic = {}

        with open("temp.txt", "r+") as read_obj:
            one_char = read_obj.read(1)
            if not one_char:
                print("empty")
            else:
                teams_post.send()


s = G2SmartBot()
s.location = "TE61"
s.parse_url()
s.send_to_teams()
s.location = "HPC France"
s.parse_url()
s.send_to_teams()

