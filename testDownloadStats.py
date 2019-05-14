import json
from time import sleep

from pymongo import MongoClient

# if __name__ == '__main__':
#     with open("config.json", "r") as read_file:
#         config = json.load(read_file)
#
#     client = MongoClient(config['mongo_uri'])
#     db = client.republic.dummy

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestingThis(object):
    upload_to_mongo = False

    def test_download_weekly_matchup(self):
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
        sleep(3)
        element('//span[text()="{}"]'.format(config['team'])).click()

        sleep(2)
        element('//*[@id="espn-analytics"]/div/div[2]/nav/ul/li[8]/a/span/span').click()
        names = element('//*[@id="espn-analytics"]/div/div[2]/nav/ul/li[8]/div').text.split('\n')

        # Need to add this since, if me or dave run it opp teams doesnt show yourself
        names.append('The Captain (CAP)')
        names.append('Dex Robinson')
        names.append('Bryzzo Souvenir Co. (BRYZ)')
        names.append('David Shaffer')

        element('//span[text()="Scoreboard"]').click()

        def return_name(team_abbv):
            name = '({})'.format(team_abbv)
            for n in range(len(names)):
                if name in names[n]:
                    return names[n+1]

            assert False, 'No team name found.'

        weeks = 7
        client = MongoClient(config['mongo_uri']).republic

        for w in range(1, weeks):
            element('//select[@class="dropdown__select"]/option[contains(text(), "Matchup {}")]'.format(w)).click()
            sleep(2)
            for x in range(1, 6):
                text = element('//div[contains(@class, "matchup-score")][{}]'.format(x)).text
                split = text.split('\n')

                client.dummy.update({'team': return_name(split[27]), 'year': '2019', 'week': w},
                                    {'$set': {'week': w, 'year': '2019', 'team': return_name(split[27]), 'opponent': return_name(split[48]),
                                              'wins': int(split[2].split('-')[0]),
                                              'loses': int(split[2].split('-')[1]),
                                              'ties': int(split[2].split('-')[2]),
                                              split[7]: int(split[28]),
                                              split[8]: int(split[29]),
                                              split[9]: int(split[30]),
                                              split[10]: int(split[31]),
                                              split[11]: int(split[32]),
                                              split[12]: int(split[33]),
                                              split[13]: int(split[34]),
                                              split[14]: int(split[35]),
                                              split[15]: float(split[36]),
                                              split[16]: float(split[37]),
                                              split[17]: float(split[38]),
                                              'HRA': float(split[39]),
                                              split[19]: float(split[40]),
                                              split[20]: float(split[41]),
                                              split[21]: float(split[42]),
                                              split[22]: float(split[43]),
                                              split[23]: float(split[44]),
                                              split[24]: float(split[45]),
                                              split[25]: float(split[46]),
                                              split[26]: float(split[47])
                                              }},
                                    upsert=True)

                client.dummy.update({'team': return_name(split[48]), 'year': '2019', 'week': w},
                                    {'$set': {'week': w, 'year': '2019', 'team': return_name(split[48]), 'opponent': return_name(split[27]),
                                              'wins': int(split[5].split('-')[0]),
                                              'loses': int(split[5].split('-')[1]),
                                              'ties': int(split[5].split('-')[2]),
                                              split[7]: int(split[49]),
                                              split[8]: int(split[50]),
                                              split[9]: int(split[51]),
                                              split[10]: int(split[52]),
                                              split[11]: int(split[53]),
                                              split[12]: int(split[54]),
                                              split[13]: int(split[55]),
                                              split[14]: int(split[56]),
                                              split[15]: float(split[57]),
                                              split[16]: float(split[58]),
                                              split[17]: float(split[59]),
                                              'HRA': float(split[60]),
                                              split[19]: float(split[61]),
                                              split[20]: float(split[42]),
                                              split[21]: float(split[63]),
                                              split[22]: float(split[64]),
                                              split[23]: float(split[65]),
                                              split[24]: float(split[66]),
                                              split[25]: float(split[67]),
                                              split[26]: float(split[68])
                                              }}, upsert=True)

    def test_delete_dummy_collection(self):
        with open("config.json", "r") as read_file:
            config = json.load(read_file)

        client = MongoClient(config['mongo_uri']).republic
        client.dummy.delete_many({'year': '2019'})

