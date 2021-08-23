from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.set_window_position(x=50, y=60)
    driver.set_window_size(width=1000, height=700)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
        Object.defineProperty(navigator, 'webdriver', {
          get: () => undefined
        })
      """
    })
    driver.get("https://passport.hupu.com/pc/login?project=www&from=pc")
    time.sleep(3)
    print(driver.title)
    username = driver.find_element_by_id("J_username")
    username.send_keys("13625283399")
    time.sleep(2)
    password = driver.find_element_by_id("J_pwd")
    password.send_keys("delta113420")
    time.sleep(2)
    ActionChains(driver).move_by_offset(330, 380).click().perform()
    time.sleep(10)
    #submit = driver.find_element_by_id("J_submit")
    #submit.click()
    driver.close()



