# TWSE equities = 上市證券
# TPEx equities = 上櫃證券

import os
import time
import logging
from datetime import datetime
from collections import namedtuple

import twstock
import requests
from lxml import etree


PACKAGE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
TWSE_EQUITIES_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'
TPEX_EQUITIES_URL = 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=4'
ROW = namedtuple('Row', ['type', 'code', 'name', 'ISIN', 'start', 'market', 'group', 'CFI'])


class WStock:
    codes = {}
    tpex = {}
    twse = {}
    open_state = False

    def __init__(self):
        self.__twse_data = self.fetch_data(TWSE_EQUITIES_URL)
        self.__tpex_data = self.fetch_data(TPEX_EQUITIES_URL)
        self.generate_stock_data()
        self.open_state = self.is_twse_open()

    @staticmethod
    def fetch_data(url):
        r = requests.get(url)
        root = etree.HTML(r.text)
        trs = root.xpath('//tr')[1:]

        result = []
        typ = ''
        for tr in trs:
            tr = list(map(lambda x: x.text, tr.iter()))
            if len(tr) == 4:
                # This is type
                typ = tr[2].strip(' ')
            else:
                # This is the row data
                result.append(_make_row_tuple(typ, tr))
        return result

    def generate_stock_data(self):
        for raw_data in [self.__tpex_data, self.__twse_data]:
            for row in raw_data:
                row = ROW(*row)
                self.codes[row.code] = row
                if row.market == "上櫃":
                    self.tpex[row.code] = row
                else:
                    self.twse[row.code] = row

    @staticmethod
    def is_twse_open():
        for _ in range(10):
            stock_0050 = twstock.realtime.get('0050')
            logging.debug(stock_0050)
            if 'info' in stock_0050:
                break
            else:
                logging.debug('Retry to get stock info')
                time.sleep(10)
        stock_info = stock_0050['info']
        stock_time = stock_info['time'].split(' ')[0]
        todays_datetime = datetime.today().strftime("%Y-%m-%d")
        return stock_time == todays_datetime


def _make_row_tuple(typ, row):
    code, name = row[1].split('\u3000')
    return ROW(typ, code, name, *row[2: -1])
