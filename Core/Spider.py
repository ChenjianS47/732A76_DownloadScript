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

    # Initialize the settings of browser and open the Wayback Machine website.
    def open_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('window-size=1920x1080')
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        chrome_options.add_experimental_option('detach', True)
        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': self.Download_directory}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path=self.chrome_driver)
        self.driver.get(self.Wayback_Machine_URL)
        pass

    # Input the website of the target webpage and press the enter for search.
    def open_website(self, target_url):
        self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/form/div/div/input[1]'). \
            send_keys(target_url)
        self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/form/div/div/input[1]').send_keys(Keys.ENTER)

        pass

    # Choose the year of 2020
    def choose_year_2020(self):
        self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/span[25]').click()
        pass

    # Choose the year of 2021
    def choose_year_2021(self):
        self.driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[2]/span[26]').click()
        pass

    # This function is used for generate the xpath date for the target date.
    def xpath_for_target_date(self, target_date, year):
        # Check the month of the target day
        month = datetime.strptime(target_date, '%b %d %Y').strftime('%b')
        # Check the start day of this month(Monday, etc.)
        start_day = self.day_calender[datetime.strptime(month + ' 1 ' + str(year), '%b %d %Y').strftime('%A')] - 1
        # Check the day(Monday,etc) of the target day
        day = datetime.strptime(target_date, '%b %d %Y').strftime('%A')
        # Calculates the days between the target day and the start of that month, like target_day is JUN 16, then
        # calculate the days between JUN 16 and JUN 1, then plus with the start day that make the start from the first
        # Sunday of the year, which is the start day in the Wayback Machine
        days = int((datetime.strptime(target_date, '%b %d %Y') -
                    datetime.strptime(month + ' 1 ' + str(year), '%b %d %Y')).days) + start_day

        # Calculates the weeks that shows in the Wayback Machine
        weeks = int(days / 7) + 1
        # Generate the xpath data for target day
        xpath = '/html/body/div[4]/div[4]/div[2]/div[' + str(self.month_calender[month]) + ']/div[2]/div[' + \
                str(weeks) + ']/div[' + str(self.day_calender[day]) + ']'
        return xpath
        pass

    # This function is used for scroll the scroller
    def scroll_the_page(self):
        new_height = int(self.driver.execute_script("return document.body.scrollHeight")) * 0.32
        js_script = 'window.scrollBy(0,' + str(new_height) + ')'
        self.driver.execute_script(js_script)
        pass

    # This function is used for checking the xpath for latest time page of the target dates, if there is no time could
    # be selected, this function would return the xpath as None
    def choose_time(self):
        xpath_last = None
        for i in range(1, 9):
            # If there is only one time page could be selected in the target dates, the xpath would be like
            # '/html/body/div[4]/div[4]/div[3]/div/div[2]/ul/div/div/li/a'.
            # If there are multiple time(more than 1) could be choose, the xpath would be
            # '/html/body/div[4]/div[4]/div[3]/div/div[2]/ul/div/div/li[i]/a', this i is depends on how many time could
            # be choose.
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

    # Download the excel file for swedish COVID-19 in Folkhalsomyndigheten
    def download_file(self):
        self.driver.find_element_by_link_text('Data som statistiken ovan bygger på kan laddas ner här (Excel)').click()
        pass

    # This function is only used for click the accept button of cookies, so that it would not shade the download link
    def click_cookie_button(self):
        self.driver.find_element_by_id('cookies-button').click()
        pass

    # Do the open select date time page and download the file, at last, close the browser
    def open_select_date_time_page_and_download(self, target_date):
        year = datetime.strptime(target_date, '%b %d %Y').strftime('%Y')
        time.sleep(2)
        if year == '2020':
            self.choose_year_2020()
            pass
        elif year == '2021':
            self.choose_year_2020()
            pass
        time.sleep(2)
        self.scroll_the_page()
        time.sleep(2)
        self.driver.implicitly_wait(1)
        self.driver.find_element_by_id('react-wayback-search').click()
        time.sleep(1)
        self.driver.find_element_by_xpath(self.xpath_for_target_date(target_date, year)).click()
        time.sleep(2)
        self.xpath_last_time, self.last_time = self.choose_time()
        if self.xpath_last_time is not None:
            time.sleep(1)
            self.driver.find_element_by_xpath(self.xpath_last_time).click()
            self.driver.implicitly_wait(1)
            try:
                time.sleep(1)
                self.click_cookie_button()
                self.download_file()
                time.sleep(30)
                os.rename(self.Download_directory + '\\Folkhalsomyndigheten_Covid19.xlsx',
                          self.Download_directory + '\\Folkhalsomyndigheten_Covid19' + '_' + target_date + '.xlsx')
                print('{}, Finished downloading of the file in {}'.format(datetime.now().strftime('%b %d %Y - %H:%M:%S')
                                                                          , target_date))
                pass
            except:
                print('{}, failed to download the file in {}'.format(datetime.now().strftime('%b %d %Y - %H:%M:%S'),
                                                                     target_date))
            pass
        else:
            print('{}, No file could be download in {}'.format(datetime.now().strftime('%b %d %Y - %H:%M:%S'),
                                                               target_date))
            pass
        self.driver.quit()

        pass

    pass
