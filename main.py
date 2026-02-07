from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from tqdm import tqdm



service = Service(executable_path="chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://user.tungee.com/users/sign-in")
driver.implicitly_wait(40)
results = []

# 1. 点击账号登录
account_login_tab = driver.find_element(By.XPATH, '//div[text()="账号登录"]')
account_login_tab.click()

# 2. 输入手机号
phone_input = driver.find_element(By.XPATH, '//input[@placeholder="请输入手机号码"]')
phone_input.send_keys("")  # <-- 在这里填你的手机号

# 3. 输入密码
password_input = driver.find_element(By.XPATH, '//input[@placeholder="请输入密码"]')
password_input.send_keys("")  # <-- 在这里填你的密码

# 4. 点击登录按钮
login_button = driver.find_element(By.XPATH, '//button[contains(@class, "ant-btn-primary")]')
login_button.click()

# 5. 点击探迹CRM
button = driver.find_element(By.XPATH, '//a[@pointid="AA0000-AA0E00"]')
button.click()

# 6. 点击客户管理
customer_manage = driver.find_element(By.XPATH, '//span[text()="客户管理"]')
customer_manage.click()

# 7. 点击收起
button = driver.find_element(By.XPATH, '//i[@aria-label="图标: up"]/parent::div')
button.click()

time.sleep(20)

print("munual op")


# # 定位并点击“下一页”按钮
# next_button = driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-next a.ant-pagination-item-link")
# next_button.click()

while(True):
    # 找出所有数据行
    rows = driver.find_elements(By.CSS_SELECTOR, 'tr.ant-table-row')
    print(len(rows))



    # 记录当前窗口
    main_window = driver.current_window_handle

    for row in tqdm(rows, desc="正在提取每一行数据"):
        tds = row.find_elements(By.TAG_NAME, 'td')
        if len(tds) >= 4:
            try:
                # 点击第4列的<a>
                a_tag = tds[3].find_element(By.TAG_NAME, 'a')
                driver.execute_script("arguments[0].click();", a_tag)
                
                # 等待新窗口出现
                WebDriverWait(driver, 60).until(lambda d: len(d.window_handles) > 1)

                new_windows = driver.window_handles
                for handle in new_windows:
                    if handle != main_window:
                        driver.switch_to.window(handle)

                        company = driver.find_element(By.CLASS_NAME, "_3Puo8")
                        print(company.text)

                        telephone = driver.find_element(By.CLASS_NAME, "_1Helv")
                        print(telephone.text)

                        name = driver.find_element(By.CLASS_NAME, "_11d6y")
                        print(name.text)

                        results.append({
                            "company": company.text,
                            "telephone": telephone.text,
                            "name": name.text
                        })
                                            
                        driver.close()  # 关闭新窗口
                        driver.switch_to.window(main_window)  # 回到主窗口

            except Exception as e:
                print("跳过该行，原因：", e)



    next_button_li = driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-next")

    # 检查是否禁用
    if next_button_li.get_attribute("aria-disabled") == "true":
        print("已经是最后一页，停止翻页。")
        break  # 退出循环
    else:
        # 点击下一页按钮
        next_button = next_button_li.find_element(By.CSS_SELECTOR, "a.ant-pagination-item-link")
        next_button.click()

        time.sleep(60)

    df = pd.DataFrame(results)
    df.to_excel("温州.xlsx", index=False)
    


driver.quit()
print(results)

df = pd.DataFrame(results)
df.to_excel("温州.xlsx", index=False)

