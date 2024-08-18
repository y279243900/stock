import json
import pandas as pd
import time  # 导入time模块
from selenium import webdriver
from selenium.webdriver.common.by import By

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

# 遍历每个股票代码
for i in stock_list:
    driver.get(f"https://www.futunn.com/stock/{i}-US")
    info_data = {"stock_number": i}

    for label in info_labels:
        try:
            # 使用 XPath 定位到文本，并获取其相邻的值
            element = driver.find_element(By.XPATH, f"//span[text()='{label}']/preceding-sibling::span")
            text = driver.execute_script("return arguments[0].textContent;", element)
            info_data[label] = text.strip()  # 存储到字典中
        except Exception as e:
            print(f"Error fetching {label} for {i}: {e}")
            info_data[label] = None  # 处理异常的情况下，使用默认值

    # 将值转换为合适的类型
    for label in info_labels:
        value = info_data.get(label)
        if value is not None:
            # 尝试将字符串转换为浮点数
            try:
                info_data[label] = float(value.replace(',', ''))  # 移除千位分隔符并转换为浮点数
            except ValueError:
                # 如果转换失败，保持原值
                info_data[label] = value

    # 检查 stock_number 是否已经存在于 DataFrame 中
    if i in df['stock_number'].values:
        # 如果存在，更新对应行
        df.loc[df['stock_number'] == i, info_labels] = [info_data.get(label) for label in info_labels]
    else:
        # 如果不存在，添加新行
        new_row_df = pd.DataFrame([info_data])
        df = pd.concat([df, new_row_df], ignore_index=True)

    # 打印获取到的信息并显示已花费时间
    for label, value in info_data.items():
        print(f"{label}: {value}")
    elapsed_time = time.time() - start_time
    formatted_time = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
    print(f"已花费时间: {formatted_time}")
    print("---------------------")

# 保存更新后的 DataFrame 到 CSV 文件
df.to_csv("D:/Code/Python/pachong/config/stocks_data.csv", index=False)