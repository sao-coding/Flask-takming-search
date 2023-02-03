import datetime
import json
import firebase_admin
from firebase_admin import credentials, firestore, auth
cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
# 建立資料庫的實例(db)
db = firestore.client()
path = "data.txt"
title = ["country", "room", "bed", "member_class", "student_ID", "name", "ID_number", "birthday", "phone", "home_phone", "address", "emergency_contact", "emergency_contact_phone", "created_at"]
result = []
f = open(path, "r")
for item in f:
    data = {}
    try:
        line = item.split("|")
        data[title[0]] = "台灣"
        data[title[1]] = line[0].split("-")[0]
        data[title[2]] = line[0]
        data[title[3]] = line[1]
        data[title[4]] = line[2]
        data[title[5]] = line[3]
        data[title[6]] = line[4]
        line[5] = str(int(line[5].split("/")[0]) + 1911) + "/" + line[5].split("/")[1] + "/" + line[5].split("/")[2]
        data[title[7]] = datetime.datetime.strptime(line[5], "%Y/%m/%d").strftime("%Y-%m-%d")
        data[title[7]] = datetime.datetime.combine(datetime.datetime.strptime(line[5], "%Y/%m/%d"), datetime.time(0, 0, 0))
        # print(type(data[title[7]]))
        data[title[8]] = line[6]
        data[title[9]] = line[7]
        data[title[10]] = line[8]
        data[title[11]] = line[9]
        data[title[12]] = line[10]
        data[title[13]] = datetime.datetime.now()
    except:
        line = item.split("|")
        data[title[0]] = "台灣"
        data[title[1]] = line[0].split("-")[0]
        data[title[2]] = line[0]
        for i in range(3, 13):
            data[title[i]] = ""
        data[title[13]] = datetime.datetime.now()
    result.append(data)
    db.collection("student_list").add(data)
f.close()
print(result)

f = open("result.json", "w")
f.write(json.dumps(str(result)))