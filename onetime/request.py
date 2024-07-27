import requests
from bs4 import BeautifulSoup

# 目标URL
url = "https://www.futunn.com/stock/COUR-US"

# 发送GET请求
response = requests.get(url)

# 确认请求成功
if response.status_code == 200:
    html_content = response.text
else:
    print(f"请求失败，状态码：{response.status_code}")
    exit()

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')
print(soup)

# 找到股票信息的容器
stock_items = soup.select('.news-item')
print(stock_items)

# 提取并打印股票信息
for item in stock_items:
    title = item.find('p', class_='news-title').text.strip()
    description = item.find('p', class_='news-des').text.strip()
    source = item.find('span', class_='news-source').text.strip()
    time = item.find('span', class_='ellipsis').text.strip()
    print(f"标题: {title}\n描述: {description}\n来源: {source}\n时间: {time}\n")

# 提取页面中某一部分
# 示例：提取股票代码和价格
stocks = soup.select('.list-item')
for stock in stocks:
    code = stock.select_one('.data-column-name .code').text.strip()
    name = stock.select_one('.data-column-name .name').text.strip()
    price = stock.select_one('.data-column-price').text.strip()
    change_ratio = stock.select_one('.data-column-changeRatio').text.strip()
    print(f"股票代码: {code}, 股票名称: {name}, 最新价: {price}, 涨跌幅: {change_ratio}")