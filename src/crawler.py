import requests
import math
import time
import datetime

Gw2APIKey = ""
API_PRE = 'https://api.guildwars2.com/v2/'
API_END = '?access_token=' + Gw2APIKey


def sec_to_hours(sec):
    min = sec / 60
    hours = min / 60
    return math.floor(hours)


def getDyeValue():
    query = requests.get(API_PRE + 'account/dyes' + API_END)

    query = query.json()

    dict = {}
    queryList = []

    i = 0
    ID_String = ''
    for index in query:
        i += 1;

        ID_String += str(index) + ","

        if i >= 150:
            i = 0
            ID_String = ID_String[:-1]
            addr = API_PRE + 'colors?ids=' + ID_String

            item_query = requests.get(addr)

            queryList.append(item_query)


            ID_String = ''


    if i <= 150 and i > 0:
        ID_String = ID_String[:-1]
        addr = API_PRE + 'colors?ids=' + ID_String

        item_query = requests.get(addr)


        queryList.append(item_query)


    for j in queryList:
        j = j.json()

        for x in j:
            if x:
                if 'item' in x:
                   ID = x['item']
                   dict[ID] = 1


    return getItemPrize(dict)


def saveValues(name, val):
    save = open(name + ".txt", 'a', encoding="utf-8")
    save.write(str(datetime.datetime.now()) + "\n")
    save.write(str(val) + "\n")
    save.close()


def getPlayTime():
    query = requests.get(API_PRE + 'account' + API_END)
    query = query.json()

    return query['age']


def getItemPrize(dict):
    # print(len(Counts))
    ID_String = ""
    queryList = []

    i = 0
    j = 0
    for x in dict:
        i += 1
        j += 1
        ID_String += str(x)

        if not i == len(dict):
            ID_String += ","

        if j == 199:
            j = 0
            query = requests.get(API_PRE + 'commerce/prices?ids=' + ID_String)
            # print(API_PRE + 'commerce/prices?ids=' + ID_String)
            queryList.append(query)
            ID_String = ''

    if j < 199:
        query = requests.get(API_PRE + 'commerce/prices?ids=' + ID_String)
        # print(API_PRE + 'commerce/prices?ids=' + ID_String)
        queryList.append(query)

    end_price = 0

    for q in queryList:

        q_json = q.json()

        for resp in q_json:
            if resp:
                if 'id' in resp:
                    ID = resp['id']
                    price = resp['sells']['unit_price']
                    item_count = dict[ID]

                    if price and item_count:
                        end_price += price * item_count

    return end_price


def coins_to_string(coins):
    c = coins

    gold = c / 10000
    gold = math.floor(gold)

    c -= gold * 10000

    silver = c / 100
    silver = math.floor(silver)

    c -= silver * 100

    copper = c

    return str(gold) + "G  " + str(silver) + "S  " + str(copper) + "C  "


def getBankWorth():
    query = requests.get(API_PRE + '/account/bank' + API_END)
    query = query.json()
    data = query_to_dict(query)
    return getItemPrize(data)


def query_to_dict(q):
    dic = {}

    i = 0
    for item in q:
        if item:
            i += 1
            ID = item['id']
            COUNT = item['count']
            dic[ID] = COUNT
    return dic


def getMatBankWorth():
    query = requests.get(API_PRE + '/account/materials' + API_END)
    query_json = query.json()

    ItemDict = query_to_dict(query_json)

    return getItemPrize(ItemDict)

    # print(len(ItemDict))


if __name__ == '__main__':
    try:
        while True:
            bank_worth = getBankWorth()
            mat_worth = getMatBankWorth()
            playtime = getPlayTime()
            dyeValue = getDyeValue()

            saveValues("Material-Worth", mat_worth)
            saveValues("Bank-Worth", bank_worth)
            saveValues("Playtime", playtime)
            saveValues("DyeValue", dyeValue)

            print("matw: " + str(coins_to_string(mat_worth)))
            print("bankw: " + str(coins_to_string(bank_worth)))
            print("playtime: " + str(sec_to_hours(playtime)) + "h")
            print('Dye Val: ' + str(coins_to_string(dyeValue)))

            time.sleep(60)
    except:
        pass
