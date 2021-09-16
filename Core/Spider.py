import re
from datetime import datetime
import time
import os

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Spider(object):
    def __init__(self, chrome_driver, wayback_machine_url, download_directory):
        self.chrome_driver = chrome_driver
        self.Wayback_Machine_URL = wayback_machine_url
        self.driver = None
        self.JAN_1ST_location = None
        self.last_time = None
        self.month_calender = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
                               'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
        self.day_calender = {'Monday': 2, 'Tuesday': 3, 'Wednesday': 4, 'Thursday': 5, 'Friday': 6, 'Saturday': 7,
                             'Sunday': 1}
        self.last_time = None
        self.xpath_last_time = None
        self.Download_directory = download_directory
        pass

    def open_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_experimental_option('detach', True)
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.Download_directory}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path=self.chrome_driver)
        self.driver.get(self.Wayback_Machine_URL)
        pass

    def open_website(self, target_url):
        self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/form/div/div/input[1]'). \
            send_keys(target_url)
        self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/form/div/div/input[1]').send_keys(Keys.ENTER)
        pass

    def choose_year_2020(self):
        self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/span[25]').click()
        pass

    def choose_year_2021(self):
        self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/span[26]').click()
        pass

    def locate_jan_1st(self):
        for i in range(1, 8):
            xpath = '/html/body/div[4]/div[4]/div[2]/div[1]/div[2]/div[1]/div[' + str(i) + ']'
            if self.driver.find_element_by_xpath(xpath).get_attribute('class') == 'month-blank-day-container':
                continue
                pass
            else:
                self.JAN_1ST_location = xpath
                break
                pass
            pass
        matchobj = re.search(r'/html/body/div\[4]/div\[4]/div\[2]/div\[1]/div\[2]/div\[1]/div\[(.*)]',
                             self.JAN_1ST_location)
        start = int(matchobj.group(1)) - 1
        return start

    def choose_time(self):
        xpath_last = None
        for i in range(1, 9):
            if i == 1:
                try:
                    xpath = '/html/body/div[4]/div[4]/div[3]/div/div[2]/ul/div/div/li/a'
                    try:
                        if self.driver.find_element_by_xpath(xpath).get_attribute('class') is not None:
                            xpath_last = xpath
                        pass
                    except:
                        pass
                except:
                    xpath = '/html/body/div[4]/div[4]/div[3]/div/div[2]/ul/div/div/li[' + str(i) + ']/a'
                    try:
                        if self.driver.find_element_by_xpath(xpath).get_attribute('class') is not None:
                            xpath_last = xpath
                        pass
                    except:
                        pass
                else:
                    continue
                    pass
                pass
            else:
                xpath = '/html/body/div[4]/div[4]/div[3]/div/div[2]/ul/div/div/li[' + str(i) + ']/a'
                try:
                    if self.driver.find_element_by_xpath(xpath).get_attribute('class') is not None:
                        xpath_last = xpath
                        pass
                    pass
                except:
                    break
                pass
            pass
        if xpath_last is not None:
            self.last_time = self.driver.find_element_by_xpath(xpath_last).get_attribute('text')
            pass
        else:
            pass
        return xpath_last, self.last_time

    def xpath_for_target_date(self, target_date, year):
        start = self.locate_jan_1st()
        month = datetime.strptime(target_date, '%b %d %Y').strftime('%b')
        day = datetime.strptime(target_date, '%b %d %Y').strftime('%A')
        days = int((datetime.strptime(target_date, '%b %d %Y') -
                    datetime.strptime(month + ' 1 ' + str(year), '%b %d %Y')).days) + start
        weeks = int(days / 7) + 1
        xpath = '/html/body/div[4]/div[4]/div[2]/div[' + str(self.month_calender[month]) + ']/div[2]/div[' + \
                str(weeks) + ']/div[' + str(self.day_calender[day]) + ']'
        return xpath
        pass

    def download_file(self):
        self.driver.find_element_by_link_text('Data som statistiken ovan bygger på kan laddas ner här (Excel)').click()
        pass

    def click_cookie_button(self):
        self.driver.find_element_by_id('cookies-button').click()
        pass

    def open_select_date_time_page_and_download(self, target_date):
        year = datetime.strptime(target_date, '%b %d %Y').strftime('%Y')
        if year == '2020':
            self.choose_year_2020()
            pass
        elif year == '2021':
            self.choose_year_2020()
            pass
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_xpath(self.xpath_for_target_date(target_date, year)).click()
        self.driver.implicitly_wait(1)
        self.xpath_last_time, self.last_time = self.choose_time()
        if self.xpath_last_time is not None:
            self.driver.find_element_by_xpath(self.xpath_last_time).click()
            self.driver.implicitly_wait(1)
            try:
                self.click_cookie_button()
                self.download_file()
                time.sleep(30)
                os.rename(self.Download_directory + '\\Folkhalsomyndigheten_Covid19.xlsx',
                          self.Download_directory + '\\Folkhalsomyndigheten_Covid19' + '_' + target_date + '.xlsx')
                print('Finished downloading of the file in {}'.format(target_date))
                pass
            except:
                print('failed to download the file in {}'.format(target_date))
            pass
        else:
            print('No file could be download in {}'.format(target_date))
            pass
        self.driver.quit()

        pass

    pass
