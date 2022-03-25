import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from config import CONFIGS

url_gold_price = CONFIGS['url_gold_price']
url_bgn_usd = CONFIGS['url_bgn_usd']
url_market = CONFIGS['url_market']


class Crawler():
    options = webdriver.ChromeOptions()
    options.add_argument("browser.download.folderList=2");
    options.add_argument("browser.helperApps.alwaysAsk.force=False");
    options.add_argument("browser.download.manager.showWhenStarting=False");
    options.add_argument("browser.download.manager.showAlertOnComplete=False");
    options.add_argument("browser.helperApps.neverAsk.saveToDisk=True");
    options.add_argument('--no-proxy-server');
    options.add_argument("--proxy-server='direct://'");
    options.add_argument("--proxy-bypass-list=*");
    options.headless = True
    
    driver = webdriver.Chrome(options=options)
    
    # gold price
    def get_gold_price(self, url):
        self.driver.get(url)
        gold_price = self.driver.find_element(By.ID, "metal-priceask").text
        gold_price = float(gold_price[1:].split(' ')[0].replace(',', ''))
        return gold_price

    # BGN/USD exchange rate
    def get_bgn_usd_rate(self, url):
        self.driver.get(url)
        bgn_usd = self.driver.find_element_by_xpath("//span[@class='DFlfde SwHCTb']").text
        bgn_usd = float(bgn_usd.replace(',','.'))
        return bgn_usd

    # gold market
    def get_market_data(self, url):
        self.driver.get(url)
        lines_raw = self.driver.find_element_by_xpath("//div[@class='table-flex table-flex--inverse m-products__table']")
        lines = lines_raw.text.split('\n')
        lines = [i for i in lines if '-' not in i and i not in ['Всички продукти', 'Филтри', 'Продайте', 'Купете', 'Купуваме', 'Продаваме']]
        return lines
    
    def close_driver(self):
        self.driver.close()


class MarketDataFormatting():
    def add_some_cols(self, df):
        df['buy'] = df['buy'].str.replace(' лв.', '').astype(int)
        df['sell'] = df['sell'].str.replace(' лв.', '').astype(int)
        df['quantity'] = df['product'].apply(lambda x: x.split(' ')[0])
        df['quantity'] = df['quantity'].apply(lambda x: int(x.split('/')[0]) / int(x.split('/')[1]) if '/' in x else x).astype(float)
        df['unit'] = df['product'].apply(lambda x: 'gr' if 'грам' in x else 'oz' if 'унция' in x else 'fr' if 'франк' in x else 'other')
        return self

    def _convert_to_gr(self, quantity, unit):
        if unit == 'gr':
            result = quantity
        elif unit == 'oz':
            result = quantity * 31.103
        elif unit == 'fr':
            result = 5.805
        else:
            result = 0
        return result
    
    def add_more_cols(self, df, bgn_usd, gold_price):
        df['gr_pure'] = df.apply(lambda x: self._convert_to_gr(x['quantity'], x['unit']), axis=1)
        #df['product'] = df['product'].apply(lambda x: ' '.join([word for word in x.split(' ')[2:]]) if 'франк' not in x else x)
        df['buy_gr'] = (df['buy'] / df['gr_pure']).round(2)
        df['sell_gr'] = (df['sell'] / df['gr_pure']).round(2)
        df['price_diff_gr'] = ((df['sell_gr'] - df['buy_gr']) / df['buy_gr']).round(4)
        df['sell_gr_premium'] = (df['sell_gr'] / (gold_price * bgn_usd / 31.103) - 1).round(4)
        df.insert(0, 'timestamp', pd.Timestamp.now(tz='Europe/Sofia'))
        return df
