import pandas as pd

from config import CONFIGS
from preprocessor import Crawler, MarketDataFormatting

url_gold_price = CONFIGS['url_gold_price']
url_bgn_usd = CONFIGS['url_bgn_usd']
url_market = CONFIGS['url_market']
output_path = CONFIGS['output_path']

# start crawling
crawler = Crawler()
gold_price = crawler.get_gold_price(url=url_gold_price)
bgn_usd = crawler.get_bgn_usd_rate(url=url_bgn_usd)
market_data = crawler.get_market_data(url=url_market)
#crawler.close_driver()

# create initial df
df_init = pd.DataFrame(
    [
        (market_data[x], market_data[x+1], market_data[x+2])
        for x in filter(lambda x: x%3 == 0, range(len(market_data)))
    ],
    columns=['product','buy','sell']
)

# feature engineering
df = MarketDataFormatting().add_some_cols(df_init).add_more_cols(df_init, gold_price, bgn_usd)

# get the latest recorded update
df_history = (
    pd.read_csv(
        f'{output_path}/gold_price.csv', parse_dates=['timestamp'], float_precision='high'
    )
)
df_prev = df_history.loc[df_history['timestamp'] == df_history['timestamp'].max()]


# if the data has been updated, save it
try:
    if len(
           df_prev.drop('timestamp', axis=1).reset_index(drop=True)
           .compare(df.drop('timestamp', axis=1).reset_index(drop=True))
        ) > 0:
        df_full = pd.concat([df_history, df])
        df_full.to_csv(f'{output_path}/gold_price.csv', index=False, float_format='%.4f')
        print('Updated the latest data')
    else:
        # if the data has not been updated, then just update the timestamp
        df_history.loc[df_history['timestamp'] == df_history['timestamp'].max, 'timestamp'] = pd.Timestamp.now(tz='Europe/Sofia')
        df_history.to_csv(f'{output_path}/gold_price.csv', index=False, float_format='%.4f')
        print('Updated the latest timestamp')
except:
    df_full = pd.concat([df_history, df])
    df_full.to_csv(f'{output_path}/gold_price.csv', index=False, float_format='%.4f')
    print('Exception when comparing, data updated')

print('Done!')