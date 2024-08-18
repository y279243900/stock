import json
import os

with open("/stock/stock_list.json") as f:
    stock_list = json.load(f)
print(stock_list)

for i in stock_list:
    if not os.path.exists(f"D:/stock_img/{i}"):
        os.mkdir(f"D:/stock_img/{i}")
