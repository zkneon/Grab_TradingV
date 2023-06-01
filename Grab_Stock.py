import string
import time
import pandas as pd
from numpy import random
import websocket
import re
import json
import requests
from datetime import datetime
from dotenv import dotenv_values

header = {'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
          'Cache-Control': 'no-cache',
          'Connection': 'Upgrade',
          'Host': 'data.tradingview.com',
          'Origin': 'https://ru.tradingview.com',
          'Pragma': 'no-cache',
          'Sec-WebSocket-Extensions': 'client_max_window_bits',
          'Sec-WebSocket-Key': 'LghjlgPSw9t6gKw==',
          'Sec-WebSocket-Version': '13',
          'Upgrade': 'websocket',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.0.0',
          }
uri = "wss://data.tradingview.com/socket.io/websocket?from=chart/tXsIDSry/&date=2023_03_22-11_27&type=chart"
config = dotenv_values('.env')

def get_list_Stock():
    # Function for get stock ticket list
    res = requests.get('https://scanner.tradingview.com/russia/scan')
    return [x['s'] for x in res.json()['data']]


def get_auth_token():
    # Auth-Function, get Socket-token and cookies for connection

    sign_in_url = 'https://www.tradingview.com/accounts/signin/'
    username = config['USER_NAME']
    password = config['PASSWORD']
    data = {"username": username, "password": password, "remember": "on"}
    headers = {
        'Referer': 'https://www.tradingview.com'
    }
    response = requests.post(url=sign_in_url, data=data, headers=headers)
    auth_token = response.json()['user']['auth_token']

    return auth_token, response.cookies


def on_message(wsapp, message):
    print(message)



def on_connect_message(wsapp, message):
    print('<<<<<<{}'.format(message))


def filter_raw_message(msg):
    # Parsing response from server
    try:
        pattern = re.compile(r'~m~[\d]+~m~')
        s1 = re.split(pattern, msg)

        for i in s1:
            print('SPLIT>>>>>>>>>', i)

        return s1
    except AttributeError:
        print("error")


def create_df(data_list):
    # Create DataFrame and write to it data
    col_l = ['local_description', 'full_name', 'isin',
                                  'pricescale', 'date', 'open', 'high',
                                  'low', 'close', 'volume']
    df = pd.DataFrame(data_list, columns=col_l)
    return df


def generate_data(msg):
    # extract needed data from msg
    msg_sl = filter_raw_message(msg)
    all_s = []
    for i in range(len(msg_sl)):
        if i == 4:
            out = re.findall(r'"s":\[(.+?)\}\]', msg_sl[i])
            ld = re.split(r'{', out[0])
            for l in range(len(ld)):
                if l == 0:
                    continue
                elif l == len(ld)-1:
                    ld[l] = '{'+ld[l]+'}'
                else:
                    ld[l] = '{'+ld[l][:-1]
                    # print(ld[l])
                dm = json.loads(ld[l])
                # print(dm['i'], 'v:', dm['v'])
                dm['v'][0] = datetime.fromtimestamp(dm['v'][0])
                sx_a = sx + dm['v']
                all_s.insert(dm['i'], sx_a)


        elif i == 2:
            out = re.findall(r'"sds_sym_1",(.+?)\],"t":', msg_sl[i])
            print(out)
            dm2 = json.loads(out[0])
            print(dm2['base_name'])
            # 'local_description' , 'full_name', 'isin' , 'pricescale'
            i = ['local_description', 'full_name', 'isin', 'pricescale']
            sx = []
            for p in i:
                sx.append(dm2[p])

    df = create_df(all_s)
    return df


def generateSession():
    # Generate Session for WebSocket request
    stringLength = 12
    letters = list(string.ascii_letters)
    print(letters)

    l = []
    for i in range(stringLength):
        l.append(random.choice(letters))
    random_string = ''.join(l)
    print(random_string)
    return "qs_" + random_string

def generateChartSession():
    # Generate Chart Session for WebSocket request
    stringLength = 12
    letters = list(string.ascii_letters)
    print(letters)

    l = []
    for i in range(stringLength):
        l.append(random.choice(letters))
    random_string = ''.join(l)
    print(random_string)
    return "cs_" + random_string


def sendMessage(wsapp, func, param_list):
    wsapp.send(createMessage(func, param_list))

def prependHeader(st):
    print("~m~" + str(len(st)) + "~m~" + st)
    return "~m~" + str(len(st)) + "~m~" + st

def constructMessage(func, paramList):
    #json_mylist = json.dumps(mylist, separators=(',', ':'))
    print('>>>>>Send:', json.dumps({
        "m":func,
        "p":paramList
        }, separators=(',', ':')))
    return json.dumps({
        "m":func,
        "p":paramList
        }, separators=(',', ':'))


def createMessage(func, param_list):
    # Create message for request
    return prependHeader(constructMessage(func, param_list))


df_of_all = pd.DataFrame()
token, cook = get_auth_token()
header = dict(header)

# stock_list = get_list_Stock()
# stock_list = ["MOEX:SBER","MOEX:LKOH","MOEX:GMKN","MOEX:GAZP","MOEX:SNGS","MOEX:PHOR","MOEX:SNGSP","MOEX:PLZL","MOEX:ROSN",
#               "MOEX:NVTK","MOEX:AKRN","MOEX:BRK2023","MOEX:MTSS","MOEX:MOEX","MOEX:FLOT","MOEX:POLY",
#               "MOEX:CHMF","MOEX:TATN","MOEX:RUAL","MOEX:ALRS","MOEX:MGNT","MOEX:ENPG","MOEX:FIVE"]

# List of stock name with market name
stock_list = ["MOEX:SBER", "MOEX:LKOH"]


'''"currency_id", "base_currency_id", "current_session", "language", "listed_exchange", "lp", "lp_time","minmov","minmove2",
    "original_name", "pricescale", "pro_name", "type", "typespecs", "volume", "ask", "bid", "fundamentals",
    "high_price", "is_tradable", "low_price", "open_price", "prev_close_price", "rch", "rchp", "rtc", "rtc_time",
    "status", "basic_eps_net_income", "beta_1_year", "earnings_per_share_basic_ttm", "industry", "market_cap_basic",
    "price_earnings_ttm", "sector", "volume", "dividends_yield", "timezone"]
'''

# for all stock in stock_list
for stock in stock_list:

    wsapp = websocket.create_connection(uri, header=header)
    resp_opcode, msg = wsapp.recv_data()
    print(resp_opcode, msg)
    session = generateSession()
    print("session generated {}".format(session))

    chart_session = generateChartSession()
    print("chart_session generated {}".format(chart_session))

    SYMBOL = stock
    TIME_FRAME = "1D"   # minute( 3, 5, 15, 30, 60, 120, 1D)
    CANDELS = 300
    WIDTH_FRAME = '60M'  # year(12, 60M)


    print('<<<<<<<<<<<<<<<{}>>>>>>>>>>>>>>'.format(stock))
    sendMessage(wsapp, "set_auth_token", [token])
    sendMessage(wsapp, "set_locale", ['ru', 'RU'])
    sendMessage(wsapp, "quote_create_session", [session])
    sendMessage(wsapp, "chart_create_session", [chart_session, "disable_statistics"])
    sendMessage(wsapp, "switch_timezone", [chart_session, 'Etc/UTC'])
    sendMessage(wsapp, "quote_set_fields", [session, "currency_id", "base_currency_id", "current_session", "language", "listed_exchange", "lp", "lp_time","minmov","minmove2",
        "original_name", "pricescale", "pro_name", "type", "typespecs", "volume", "ask", "bid", "fundamentals",
        "high_price", "is_tradable", "low_price", "open_price", "prev_close_price", "rch", "rchp", "rtc", "rtc_time",
        "status", "basic_eps_net_income", "beta_1_year", "earnings_per_share_basic_ttm", "industry", "market_cap_basic",
        "price_earnings_ttm", "sector", "volume", "dividends_yield", "timezone"])
    sendMessage(wsapp, "quote_add_symbols", [session, SYMBOL])
    sendMessage(wsapp, "resolve_symbol", [chart_session, "sds_sym_1", SYMBOL])
    sendMessage(wsapp, "create_series", [chart_session, "sds_1", "s1", "sds_sym_1", TIME_FRAME, CANDELS, WIDTH_FRAME])
    sendMessage(wsapp, "quote_remove_symbols", [session, SYMBOL])
    # sendMessage(wsapp, "request_more_data", [chart_session, "sds_1", WIDTH_FRAME])    # {m: "request_more_data", p:["cs_RrTrbKUDTybH", "sds_1", 49]}

    # resp_opcode, msg = wsapp.recv_data()
    stop_w = False
    while stop_w == False:
        time.sleep(5)

        try:
            result = wsapp.recv()
            pattern = re.compile("~m~\d+~m~~h~\d+$")
            if pattern.match(result):
                wsapp.recv()
                wsapp.send(result)
                print(">>>>>>" + str(result) + "\n\n")
                print('<<<<<<', str(result), '\n\n')

            df = generate_data(result)
            df_of_all = pd.concat([df_of_all, df], ignore_index=True)
            print(df_of_all.info())
            print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<END of {}>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'.format(stock))

            stop_w = True
        except Exception as e:
            print(e)
            break
df_of_all.to_csv(f'data/BLUE_{TIME_FRAME}.csv', sep=',')
# df_of_all.to_pickle(f'data/BLUE_{TIME_FRAME}.pkl')

