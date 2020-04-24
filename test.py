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
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiJlZmEyYzFmZjI2MWFiYWZhZTMwNDgxY2I0YTFiZGQwZjUxN2U3MDUzN2EyOWJhMDE3OGFmMmIxNmRkMTFlZjlhIiwic2NvcGUiOiJhbGVydCBpbmZyYXN0cnVjdHVyZSBjcG8tdHggZW1zcC10eCB0eC1ub3RpZmljYXRpb24gdGFzayBkYXRhdml6IHJlcG9ydGluZyIsImdyb3VwcyI6WyJXRUJIRUxQIl0sInByZWZlcmVuY2VzIjp7Imxhbmd1YWdlIjoiZW4tVVMiLCJsb2dvIjoidG90YWwucG5nIiwidGhlbWUiOiJ0b3RhbC10aGVtZSJ9LCJpYXQiOjE1ODc3NDk5ODksImV4cCI6MTU4Nzc3MTU4OSwiYXVkIjoiZzJzbWFydC5jb20iLCJpc3MiOiJnMnNtYXJ0LXdlYm1nciIsInN1YiI6InVzZXIvMjI0NTIxMjE4In0.FeALh8MjkmMjRrXBm1VjzA_Y8v5d__LbfTSqO8JhAeJgSfWRn9dQqEJoWlZktP6btPKDorpL4Wr67vh4RNMywdli7WjY-kR4bqRQdbE6kMbdxN7X__CKiysVhZcEwUHO2UAEk5sDEuRRkwfzwPRMqZsrxJZ_ge3P7B248IvwEU0UBCgxpb9YEj8PbR4kjhzm0MTvgv8319m_-DkasebuK6L7GQbkS6RIN9pGTZD1X8TGsekrsu7hvPxjv5NmDEuz86K2Vv83HDLzJz-p6ykHGdPGGzTQ2A8aEFjllhcPHq6UeIM-smRECZ6PI9jwP5M1APPTykpUR5DyQ8qvH5FWXg",
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
