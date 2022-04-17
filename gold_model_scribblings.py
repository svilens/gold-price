import itertools
from datetime import datetime
import pandas as pd

prices = [
    3771, 3771, 3771, 3771, 3771,
    3782, 3782, 3782, 3782, 3782, 
    3790, 3790, 3790, 3790, 3790,
    6044, 6044, 6044, 
    12019,
    732, 732, 732, 732, 732,
    2502, 2502, 2502, 2502, 2502,
    3725, 3725, 3725, 3725, 3725, 
    1280, 1280, 1280, 1280, 1280
]

coins_dict = {
    3771: {'name': 'cang', 'weight': 31.1, 'buy': 3671},
    3782: {'name': 'filh', 'weight': 31.1, 'buy': 3671},
    3790: {'name': 'maple', 'weight': 31.1, 'buy': 3671},
    6044: {'name': 'v_50', 'weight': 50, 'buy': 5815},
    12019: {'name': 'v_100', 'weight': 100, 'buy': 11572},
    732: {'name': 'napoleon', 'weight': 5.805, 'buy': 695},
    2502: {'name': 'v_20', 'weight': 20, 'buy': 2326},
    3725: {'name': '100_cor', 'weight': 30.483, 'buy': 3465},
    1280: {'name': 'v_10', 'weight': 10, 'buy': 1163}
}

coins_dict = {
    3771: {'name': 'v_31', 'weight': 31.1, 'buy': 3617},
    3782: {'name': 'filh', 'weight': 31.1, 'buy': 3671},
    3790: {'name': 'maple', 'weight': 31.1, 'buy': 3671},
    6044: {'name': 'v_50', 'weight': 50, 'buy': 5815},
    12019: {'name': 'v_100', 'weight': 100, 'buy': 11572},
    732: {'name': 'napoleon', 'weight': 5.805, 'buy': 695},
    2502: {'name': 'v_20', 'weight': 20, 'buy': 2326},
    3725: {'name': '100_cor', 'weight': 30.483, 'buy': 3465},
    1280: {'name': 'v_10', 'weight': 10, 'buy': 1163}
}

coins_dict_igold = {
    3771: {'name': 'v_31', 'weight': 31.1, 'buy': 3696},
    3782: {'name': 'filh', 'weight': 31.1, 'buy': 3704},
    3790: {'name': 'maple', 'weight': 31.1, 'buy': 3714},
    6044: {'name': 'v_50', 'weight': 50, 'buy': 5914},
    12019: {'name': 'v_100', 'weight': 100, 'buy': 11599},
    732: {'name': 'napoleon', 'weight': 5.805, 'buy': 706},
    2502: {'name': 'v_20', 'weight': 20, 'buy': 2388},
    3725: {'name': '100_cor', 'weight': 30.483, 'buy': 3613},
    1280: {'name': 'v_10', 'weight': 10, 'buy': 1206}
}

target_max = 19910
target_min = 19000
items_max = 8

start = datetime.now()
results = [seq for i in range(items_max + 1)
          for seq in itertools.combinations(prices, i)
          if sum(seq) <= target_max and sum(seq) >= target_min]
print(datetime.now() - start)
res_set = set(results)
res_set_list = list(res_set)
len(res_set_list)

df = pd.DataFrame()
for comb in res_set_list:
    inner = pd.DataFrame({
        #'combination': [comb],
        'labels': [", ".join([coins_dict_igold[x]['name'] for x in comb])],
        'total cost': [sum(comb)],
        'total weight': [sum([coins_dict_igold[x]['weight'] for x in comb])],
        'total buy': [sum([coins_dict_igold[x]['buy'] for x in comb])],
        'residual': [target_max - sum(comb)],
        'loss': [sum([coins_dict_igold[x]['buy'] for x in comb]) - sum(comb)]
    })
    df = pd.concat([df, inner])

df = df.sort_values(by='loss', ascending=False).reset_index(drop=True)
df.head(50)

df.sort_values(by=['total weight', 'loss', 'residual'], ascending=[False, False, False]).head(20)

df.loc[df['labels'].str.contains('v_50', case=False)].head(20)