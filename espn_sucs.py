from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

if __name__ == '__main__':
    with open("config.json", "r") as read_file:
        config = json.load(read_file)

    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(options=options, executable_path='chromedriver.exe')

    def element(value, by=By.XPATH, timeout=20):
        return WebDriverWait(driver=driver, timeout=timeout).until(EC.presence_of_element_located((by, value)))

    driver.get(config['url'])
    iframe = driver.find_element_by_id('disneyid-iframe')
    driver.switch_to_frame(iframe)

    # login
    element("//input[@type='email']").send_keys(config['email'])
    element("//input[@type='password']").send_keys(config['password'])
    element(value='btn', by=By.CLASS_NAME).click()

    # get to the fantasy site
    element(value='Fantasy', by=By.LINK_TEXT).click()
    element('//span[text()="{}"]'.format(config['team'])).click()
    element('//span[text()="Scoreboard"]').click()
