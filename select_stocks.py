import json
import numpy as np
import pandas as pd


# pd.set_option('display.max_rows', None)  # 显示所有行
def convert_volume(volume_str):
    if isinstance(volume_str, str):
        volume_str = volume_str.replace('股', '')
        if '万' in volume_str:
            return float(volume_str.replace('万', '')) * 10000
        elif '亿' in volume_str:
            return float(volume_str.replace('亿', '')) * 100000000
        elif '-' in volume_str:
            return 0
        return float(volume_str)
    elif isinstance(volume_str, (int, float)):
        return volume_str
    else:
        return 0  # 对于无法识别的数据，返回0


df = pd.read_csv("/config/stocks_data.csv")
df['stock_number'] = df['stock_number'].replace(np.nan, 'NA')
df['成交量'] = df['成交量'].apply(convert_volume)
filtered_df = df[(df['昨收'] >= 0.04) & (df['昨收'] <= 2.5) & (df['成交量'] >= 7000)]
stock_number_list = filtered_df['stock_number'].tolist()
with open("/config/filter_stocks.json", 'w') as json_file:
    json.dump(stock_number_list, json_file, ensure_ascii=False, indent=4)
print(filtered_df)
