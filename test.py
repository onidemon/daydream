import requests
import json
from pprint import pprint
import csv


class G2smart:
    def __init__(self):
        pass

    def scrape_url(self):
        dic = {}
        headers = {
            "Host": "www.g2smart.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.g2smart.com/g2smart/alert?cpo=total_fr_hpc&after=2019-10-23T21:00:00.000Z",
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCIW5FWXg",
            "Connection": "keep-alive",
        }

        counter = 1
        dic_counter = 1
        while counter < 10:
            resp = requests.get(
                "https://www.g2smart.com/g2smart/api/alert?cpo=total_fr_hpc&after=2019-10-23T21:00:00.000Z&limit=10&page="
                + str(counter),
                headers=headers,
            )
            for i in resp.json()['items']:
                try:
                    dic["alert" + str(dic_counter) + ": "] = {
                        "Location": i["locationName"],
                        "Charger": i["equipmentId"],
                        "Alert_Status": i["status"],
                        "Open_Date": i["openDate"],
                        "Alert_Details": i["initiatorEvent"]["details"]["status"],
                    }
                except KeyError:
                    dic["alert" + str(dic_counter) + ": "] = {
                        "Location": i["locationName"],
                        "Charger": i["equipmentId"],
                        "Alert_Status": i["status"],
                        "Open_Date": i["openDate"],
                        "Alert_Details": i["initiatorEvent"]["type"],
                    }
                dic_counter += 1
            counter += 1
        return dic

# def write_to_cvs():
#     with open("test.csv", "w") as f:
#         for key in dic_from_json().keys():
#             f.write("%s,%s\n" % (key, dic_from_json()[key]))
# pprint(scrape_url())

s = G2smart()
