import time
import datetime
import json
import urllib3
import random
import locale
import tokens
locale.setlocale(locale.LC_ALL, '')

http = urllib3.PoolManager()

testBot, covidBot = tokens.tokens()

date = datetime.date.today().strftime("%d %B")


def check_users(token):
    url = f'https://api.telegram.org/bot{token}/getUpdates'
    r = http.request('GET', url)
    dec_resp = json.loads(r.data.decode('utf-8'))
    print('Getting User Data, Response ---> ', r.status)
    lenId = len(dec_resp['result'])
    userArr = []
    nameArr = []
    for x in range(0, lenId):
        id = dec_resp['result'][x]['message']['chat']['id']
        name = dec_resp['result'][x]['message']['chat']['first_name']
        userArr.append(id)
        nameArr.append(name)
    userArr = list(dict.fromkeys(userArr))
    nameArr = list(dict.fromkeys(nameArr))
    print(userArr, nameArr)
    return userArr, nameArr


def send_wish(msg, userList, nameList, token):
    userList = userList
    nameList = nameList
    listLen = len(userList)
    for x in range(0, listLen):
        send_text = 'https://api.telegram.org/bot' + token + \
            '/sendMessage?chat_id=' + \
            str(userList[x]) + '&parse_mode=markdown&text=*Good Morning ' + \
            str(nameList[x]) + '!*' + msg
        r = http.request('GET', send_text)
        print(f'Wishing {nameList[x]}, Response ---> {r.status}')


def get_covid_data():
    url = 'https://api.covid19india.org/data.json'
    r = http.request('GET', url)
    dec_resp = json.loads(r.data.decode('utf-8'))
    print('Getting CoViD Data, Response ---> ', r.status)
    total_confirmed = int(dec_resp['statewise'][0]['confirmed'])
    total_active = int(dec_resp['statewise'][0]['active'])
    total_recovered = int(dec_resp['statewise'][0]['recovered'])
    total_deaths = int(dec_resp['statewise'][0]['deaths'])

    daily_confirmed = int(dec_resp['cases_time_series'][-1]['dailyconfirmed'])
    daily_deceased = int(dec_resp['cases_time_series'][-1]['dailydeceased'])
    daily_recovered = int(dec_resp['cases_time_series'][-1]['dailyrecovered'])

    delta_confirmed = daily_confirmed-daily_recovered

    msg = f"CoViD Updates |_{date}_|:\n" \
          f"Yesterday Confirmed: *{daily_confirmed:n}*\nYesterday Recovered: *{daily_recovered:n}*\nNet Added (C - R): *{delta_confirmed:n}*\nYesterday Deceased: *{daily_deceased:n}*\n-----------------------------------------\n" \
          f"Total Confirmed: *{total_confirmed:n}*\nTotal Active: *{total_active:n}*\nTotal Recovered: *{total_recovered:n}*\nTotal Deaths: *{total_deaths:n}*" \
          f"\n\n*Stay Home, Stay Safe* \U0001f49a"
    return msg


def get_quote():
    url = 'https://type.fit/api/quotes'
    r = http.request('GET', url)
    dec_resp = json.loads(r.data.decode('utf-8'))
    print('Getting Quote, Response --->', r.status)
    rand = random.randint(0, 1600)
    quote = dec_resp[rand]['text']
    author = dec_resp[rand]['author']

    msg = f"\n\n*{quote}*\n~ {author}\n\n"

    return msg


def create_wish():
    token = testBot
    quote = get_quote()
    covid = get_covid_data()
    userList, nameList = check_users(token)
    msg = f'{quote}{covid}'
    send_wish(msg, userList, nameList, token)


create_wish()
