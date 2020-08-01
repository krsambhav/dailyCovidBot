import time
import json
import requests
import random

# def send_wish(msg):
#     token = '1308060193:AAFkI1FAWd5k_Wf7Vk6sSzAgXVCdEg7lIeY'
#     chat_id = '954226967'

#     send_text = 'https://api.telegram.org/bot' + token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + msg

#     response = requests.get(send_text)

def check_users():
    url = 'https://api.telegram.org/bot1308060193:AAFkI1FAWd5k_Wf7Vk6sSzAgXVCdEg7lIeY/getUpdates'
    response = requests.get(url)
    dec_resp = response.json()
    lenId = len(dec_resp['result'])
    userArr = []
    for x in range(0,lenId):
        id = dec_resp['result'][x]['message']['chat']['id']
        userArr.append(id)
    userArr = list(dict.fromkeys(userArr))
    return userArr

def send_wish(msg, userList):
    token = '1308060193:AAFkI1FAWd5k_Wf7Vk6sSzAgXVCdEg7lIeY'
    userList = userList
    for user in userList:
        send_text = 'https://api.telegram.org/bot' + token + \
        '/sendMessage?chat_id=' + str(user) + '&parse_mode=Markdown&text=' + msg
        response = requests.get(send_text)


def get_covid_data():
    url = 'https://api.covid19india.org/data.json'
    response = requests.get(url)
    dec_resp = response.json()
    total_confirmed = dec_resp['statewise'][0]['confirmed']
    total_active = dec_resp['statewise'][0]['active']
    total_recovered = dec_resp['statewise'][0]['recovered']
    total_deaths = dec_resp['statewise'][0]['deaths']

    daily_confirmed = dec_resp['cases_time_series'][-1]['dailyconfirmed']
    daily_deceased = dec_resp['cases_time_series'][-1]['dailydeceased']
    daily_recovered = dec_resp['cases_time_series'][-1]['dailyrecovered']

    msg = f"CoViD Updates:\n" \
          f"Yesterday Confirmed: {daily_confirmed}\nYesterday Deceased: {daily_deceased}\nYesterday Recovered: {daily_recovered}\n\n" \
          f"Total Cofirmed: {total_confirmed}\nTotal Active: {total_active}\nTotal Recovered: {total_recovered}\nTotal Deaths: {total_deaths}" \
          f"\n\nStay Home, Stay Safe!"
    return msg


def get_quote():
    url = 'https://type.fit/api/quotes'
    response = requests.get(url)
    dec_resp = response.json()
    rand = random.randint(0, 1600)
    quote = dec_resp[rand]['text']
    author = dec_resp[rand]['author']

    msg = f"Good Morning!\n\n{quote} ~ {author}\n\n"
    return msg


def create_wish():
    quote = get_quote()
    covid = get_covid_data()
    userList = check_users()
    msg = f'{quote}{covid}'
    send_wish(msg, userList)


create_wish()