import json

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from PIL import Image
from helper.ana_img import ana_img
import time

# 设置 ChromeDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
# options.add_argument("--headless")  # 无头模式，不会显示浏览器界面
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")

# 创建 Chrome WebDriver 实例
driver = webdriver.Chrome(options=options)

# 修改 webdriver 值，隐藏 Selenium 的特征
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})


def get_img(stock: str = ""):
    driver.get(f"https://www.futunn.com/stock/{stock}-US")
    try:
        menu = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'select-component.minute-select.triangle-style'))
        )
        menu.click()
        pre_market_item = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '盘前分时')]"))
        )
        pre_market_item.click()
        # 使用显式等待确保Canvas元素加载完成
        canvas = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas[data-zr-dom-id="zr_0"]'))
        )

        # 确保Canvas元素的尺寸非零
        WebDriverWait(driver, 10).until(
            lambda driver: canvas.size['width'] > 0 and canvas.size['height'] > 0
        )

        # 获取Canvas元素的位置和大小
        location = canvas.location
        size = canvas.size

        # 打印位置和大小
        print(f"Canvas位置: {location}")
        print(f"Canvas大小: {size}")

        # 截取整个页面的截图
        driver.save_screenshot('full_screenshot.png')

        # 打开整个页面的截图并裁剪出Canvas元素部分
        full_screenshot = Image.open('full_screenshot.png')
        left = int(location['x'])
        top = int(location['y'])
        right = left + int(size['width'])
        bottom = top + int(size['height'])

        # 只保留截图上面的68%
        bottom = top + int(0.68 * size['height'])

        # 确保裁剪区域在图像的边界内
        right = min(right, full_screenshot.width)
        bottom = min(bottom, full_screenshot.height)

        # 裁剪并保存Canvas元素的截图
        if left < full_screenshot.width and top < full_screenshot.height:
            canvas_screenshot = full_screenshot.crop((left, top, right, bottom))
            canvas_screenshot.save(f"D:\\stock_img\\{stock}\\{stock}.png")
            print(f"Canvas元素的截图已保存为 {stock}.png")
        else:
            print("裁剪区域超出图像边界，无法截取截图。")

    except TimeoutException:
        print("Canvas元素未能在指定时间内加载或尺寸为零。")


def main():
    with open("/config/filter_stocks.json") as f:
        stock_list = json.load(f)
    for i in stock_list:
        get_img(i)
        ana_img(i)
    input("Press any key to exit...")


if __name__ == '__main__':
    main()
    # get_img("MVO")
    # ana_img("MVO")
