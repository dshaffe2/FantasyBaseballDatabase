from time import sleep

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
    sleep(3)
    iframe = driver.find_element_by_id('disneyid-iframe')
    driver.switch_to.frame(iframe)

    # login
    element("//input[@type='email']").send_keys(config['email'])
    element("//input[@type='password']").send_keys(config['password'])
    element(value='btn', by=By.CLASS_NAME).click()

    # get to the fantasy site
    element(value='Fantasy', by=By.LINK_TEXT).click()
    sleep(1)
    element('//span[text()="{}"]'.format(config['team'])).click()
    element('//span[text()="Scoreboard"]').click()

    data = {}

    weeks = 6
    for w in range(1, weeks):
        element('//select[@class="dropdown__select"]/option[contains(text(), "Matchup {}")]'.format(w)).click()
        sleep(2)
        for x in range(1, 6):
            text = element('//div[contains(@class, "matchup-score")][{}]'.format(x)).text
            split = text.split('\n')

            try:
                data
                data[split[27]].update({'week_{}'.format(w): {'opponent': split[48], split[7]: split[28],
                                                              split[8]: split[29], split[9]: split[30],
                                                              split[10]: split[31], split[11]: split[32],
                                                              split[12]: split[33], split[13]: split[34],
                                                              split[14]: split[35], split[15]: split[36]}})


                data[split[48]].update({'week_{}'.format(w): {'opponent': split[27], split[7]: split[49],
                                                              split[8]: split[50], split[9]: split[51]}})
            except KeyError:
                data.update({split[27]: {'week_{}'.format(w): {'opponent': split[48], split[7]: split[28],
                                                               split[8]: split[29], split[9]: split[30]}}})
                data.update({split[48]: {'week_{}'.format(w): {'opponent': split[27], split[7]: split[49],
                                                               split[8]: split[50], split[9]: split[51]}}})

        with open('data.json', 'w') as fp:
            json.dump(data, fp, indent=4, sort_keys=True)
