import os
import pymongo
from bson.objectid import ObjectId


MOSCOW = 'Europe/Moscow'

COOKIES = [
                {
                        "name" : "AMCV_14215E3D5995C57C0A495C55%40AdobeOrg",
                        "value" : "-408604571%7CMCIDTS%7C18439%7CMCMID%7C10669762163279621713109375077689942807%7CMCAAMLH-1593719226%7C6%7CMCAAMB-1593719226%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1593121626s%7CNONE%7CvVersion%7C4.6.0",
                        "domain" : ".linkedin.com",
                        "path" : "/",
                        "expires" : 1608666426,
                        "size" : 265,
                        "httpOnly" : False,
                        "secure" : False,
                        "session" : False
                },
                {
                        "name" : "lang",
                        "value" : "v=2&lang=en-us",
                        "domain" : ".linkedin.com",
                        "path" : "/",
                        "expires" : -1,
                        "size" : 18,
                        "httpOnly" : False,
                        "secure" : True,
                        "session" : True,
                        "sameSite" : "None"
                },
                {
                        "name" : "chp_token",
                        "value" : "AgFgos_2ZK7ytgAAAXLspJas4Wfc_oWOFhft-sKmdm9FZlZR4r_Mst3tew3zHdd1J6QM15BLUMhaMzkl1GjWrNdt7A",
                        "domain" : ".www.linkedin.com",
                        "path" : "/",
                        "expires" : 1593194508.614162,
                        "size" : 99,
                        "httpOnly" : False,
                        "secure" : True,
                        "session" : False,
                        "sameSite" : "None"
                },
                {
                        "name" : "lidc",
                        "value" : "\"b=VGST02:g=2097:u=1:i=1593108107:t=1593194507:s=AQFCt9nb6GQ8rFskMNZfUjaEBeowAFMK\"",
                        "domain" : ".linkedin.com",
                        "path" : "/",
                        "expires" : 1593194507.95136,
                        "size" : 86,
                        "httpOnly" : False,
                        "secure" : True,
                        "session" : False,
                        "sameSite" : "None"
                },
                {
                        "name" : "_gat",
                        "value" : "1",
                        "domain" : ".linkedin.com",
                        "path" : "/",
                        "expires" : 1593115020,
                        "size" : 5,
                        "httpOnly" : False,
                        "secure" : False,
                        "session" : False
                },
                {
                        "name" : "aam_uuid",
                        "value" : "10092351756418616163164226325625671900",
                        "domain" : ".linkedin.com",
                        "path" : "/",
                        "expires" : 1595706427,
                        "size" : 46,
                        "httpOnly" : False,
                        "secure" : False,
                        "session" : False
                },
                {
                        "name" : "JSESSIONID",
                        "value" : "\"ajax:2789611773855419891\"",
                        "domain" : ".www.linkedin.com",
                        "path" : "/",
                        "expires" : -1,
                        "size" : 36,
                        "httpOnly" : False,
                        "secure" : True,
                        "session" : True,
                        "sameSite" : "None"
                },
                {
                        "name" : "lissc",
                        "value" : "1",
                        "domain" : ".linkedin.com",
                        "path" : "/",
                        "expires" : 1624644107.951341,
                        "size" : 6,
                        "httpOnly" : False,
                        "secure" : True,
                        "session" : False,
                        "sameSite" : "None"
                },
                {
                        "name" : "_ga",
                        "value" : "GA1.2.1351285498.1593108108",
                        "domain" : ".linkedin.com",
                        "path" : "/",
                        "expires" : 1656186420,
                        "size" : 30,
                        "httpOnly" : False,
                        "secure" : False,
                        "session" : False
                },
                {
                        "name" : "bcookie",
                        "value" : "\"v=2&e474d8ea-1aa1-417f-8b20-efcedf134436\"",
                        "domain" : ".linkedin.com",
                        "path" : "/",
                        "expires" : 1656221959.951287,
                        "size" : 49,
                        "httpOnly" : False,
                        "secure" : True,
                        "session" : False,
                        "sameSite" : "None"
                },
                {
                        "name" : "AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg",
                        "value" : "1",
                        "domain" : ".linkedin.com",
                        "path" : "/",
                        "expires" : -1,
                        "size" : 42,
                        "httpOnly" : False,
                        "secure" : False,
                        "session" : True
                },
                {
                        "name" : "bscookie",
                        "value" : "\"v=1&202006251801471a838c78-5948-4d0f-8d62-2c613332518eAQHhpfLBdQTnZfr0dgpgcULJTU75-8Hb\"",
                        "domain" : ".www.linkedin.com",
                        "path" : "/",
                        "expires" : 1656221959.951317,
                        "size" : 96,
                        "httpOnly" : True,
                        "secure" : True,
                        "session" : False,
                        "sameSite" : "None"
                },
                {
                        "name" : "li_rm",
                        "value" : "AQGey3d83lk2uQAAAXLspJArh-1r_b18C8BgUOFOqwDJ3dxGMApXC96-QmgBBLE7TJ0rGfLHDBN36AxQe4IuYp0Pzh3zoXVdMiC1U_3rnAGOtp6AzKGwOytP",
                        "domain" : ".www.linkedin.com",
                        "path" : "/",
                        "expires" : 1624644106.951178,
                        "size" : 125,
                        "httpOnly" : True,
                        "secure" : True,
                        "session" : False,
                        "sameSite" : "None"
                }
]

COOKIE_META = {
        "expires" : 1624477493.695649,
        "task_id" : None
}

def put_cookie():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = client["O24Mc-prod"]
    accounts = mydb["accounts"]

    myquery = { "_id": ObjectId("5ef4e028aefabad2d4ed24f0") }
    newvalues = { "$set": { "cookies": COOKIES } }

    meta = {"$set": {'expires': COOKIE_META['expires'], 'status' : 0, 'blocking_data' : {} }}

    accounts.update_one(myquery, newvalues)

    accounts.update_one(myquery, meta)


if __name__ == '__main__':
    print("\n\n.......put_cookie started")
    put_cookie()

# python -m o24.monitoring.add_accounts_cookie