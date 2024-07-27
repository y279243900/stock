from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import time

# 设置 ChromeDriver
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

# 创建 Chrome WebDriver 实例
driver = webdriver.Chrome(options=options)

# 修改 webdriver 值，隐藏 Selenium 的特征
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})


def login_12306():
    driver.get('https://kyfw.12306.cn/otn/resources/login.html')

    while driver.current_url != 'https://kyfw.12306.cn/otn/view/index.html':
        time.sleep(5)
    print("login successfully!")
    driver.get("https://kyfw.12306.cn/otn/leftTicket/init")
    driver.find_element(By.ID, "fromStationText").click()
    driver.find_element(By.ID, "fromStationText").clear()
    driver.find_element(By.ID, "fromStationText").send_keys("广州南")
    driver.find_element(By.ID, "fromStationText").send_keys(Keys.ENTER)
    driver.find_element(By.ID, "toStationText").click()
    driver.find_element(By.ID, "toStationText").clear()
    driver.find_element(By.ID, "toStationText").send_keys("茂名南")
    driver.find_element(By.ID, "toStationText").send_keys(Keys.ENTER)
    driver.find_element(By.ID, "train_date").click()
    driver.find_element(By.ID, "train_date").clear()
    driver.find_element(By.ID, "train_date").send_keys("2024-07-25")
    driver.find_element(By.ID, "train_date").send_keys(Keys.ENTER)
    driver.find_element(By.ID, "query_ticket").click()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#queryLeftTable tr:nth-child(3) .btn72"))).click()
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "normalPassenger_0"))).click()
    # driver.find_element(By.ID, "normalPassenger_1").click()
    # select1 = Select(driver.find_element(By.ID, "seatType_1"))
    # select1.select_by_value("O")
    # select2 = Select(driver.find_element(By.ID, "seatType_2"))
    # select2.select_by_value("O")
    # driver.find_element(By.ID, "submitOrder_id").click()
    # seat1 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "1D")))
    # driver.execute_script("arguments[0].scrollIntoView(true);", seat1)
    # seat1.click()
    # driver.find_element(By.ID, "1F").click()
    # driver.find_element(By.ID, "qr_submit_id").click()


def main():
    login_12306()
    input("Press any key to exit...")


if __name__ == '__main__':
    main()
