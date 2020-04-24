import requests
import json


def scrape_url():
    headers = {
        "Host": "www.****.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:76.0) Gecko/20100101 Firefox/76.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.*******.com/******/data?after=2019-10-23T21:00:00.000Z",
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJlZmEyYzFmZ",
        "Connection": "keep-alive",
    }

    counter = 1
    while counter < 112:
        resp = requests.get(
            "https://www.********.com/api/data?after=2019-10-23T21:00:00.000Z&limit=10&page="
            + str(counter),
            headers=headers,
        )
        with open("AT" + str(counter) + ".json", "w") as my_file:
            my_file.write(resp.text)
            counter += 1


def dic_from_json():
    dic = {}
    counter = 1
    dic_counter = 1
    while counter < 112:
        with open("AT" + str(counter) + ".json", "r+") as json_file:
            data = json.load(json_file)
            for i in data["items"]:
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


def write_to_cvs():
    with open("test.csv", "w") as f:
        for key in dic_from_json().keys():
            f.write("%s,%s\n" % (key, dic_from_json()[key]))
