import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor

# 设置 ChromeDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--headless")  # 无头模式，不会显示浏览器界面
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

# 创建 Chrome WebDriver 实例
driver = webdriver.Chrome(options=options)

# 修改 webdriver 值，隐藏 Selenium 的特征
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

# 读取 stock_list
with open("/stock/stock_list.json") as f:
    stock_list = json.load(f)

# 读取现有的 CSV 文件
df = pd.read_csv("/config/stocks_data.csv")
info_labels = ["今开", "昨收", "最高价", "最低价", "成交量", "成交额"]
# 开始计时
start_time = time.time()


def fetch_and_process_data(i):
    info_data = {"stock_number": i}
    driver.get(f"https://www.futunn.com/stock/{i}-US")

    for label in info_labels:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//span[text()='{label}']/preceding-sibling::span"))
            )
            text = driver.execute_script("return arguments[0].textContent;", element)
            info_data[label] = text.strip()
        except Exception as e:
            print(f"Error fetching {label} for {i}: {e}")
            info_data[label] = None

    # 将值转换为合适的类型
    for label in info_labels:
        value = info_data.get(label)
        if value is not None:
            try:
                info_data[label] = float(value.replace(',', ''))
            except ValueError:
                info_data[label] = value

    # 打印获取到的信息并显示已花费时间
    for label, value in info_data.items():
        print(f"{label}: {value}")

    elapsed_time = time.time() - start_time
    formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print(f"已花费时间: {formatted_time}")
    print("---------------------")

    return info_data


# 并行处理每个股票代码
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(fetch_and_process_data, stock_list))

# 更新 DataFrame
for info_data in results:
    stock_number = info_data['stock_number']
    if stock_number in df['stock_number'].values:
        df.loc[df['stock_number'] == stock_number, info_labels] = [info_data.get(label) for label in info_labels]
    else:
        new_row_df = pd.DataFrame([info_data])
        df = pd.concat([df, new_row_df], ignore_index=True)

# 保存更新后的 DataFrame 到 CSV 文件
df.to_csv("D:/Code/Python/pachong/config/stocks_data.csv", index=False)
