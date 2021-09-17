import time
import pandas as pd
from datetime import datetime

from Config import *
from Core.Spider import Spider

print('{}, Start to downloading files'.format(datetime.now().strftime('%b %d %Y - %H:%M:%S')))

# Generate the dates that have file to download
dates = pd.date_range(start_date, final_date).strftime('%b %d %Y').to_list()
# Initialize the Selenium
Spider = Spider(chrome_driver=chrome_driver, wayback_machine_url=Wayback_Machine_URL,
                download_directory=Download_directory)
# Start a loop for downloading the file
for target_date in dates:
    # Checking the time whether is earlier than JUL 17 2020, if it is, use the old website, if not use the new one
    if datetime.strptime(target_date, '%b %d %Y').date() < datetime.strptime('JUL 14 2020', '%b %d %Y').date():
        Target_URL_N = Target_URL[0]
        pass
    else:
        Target_URL_N = Target_URL[1]
        pass
    # Open a new browser
    Spider.open_browser()
    # Search the past data in the Wayback Machine webpage
    Spider.open_website(target_url=Target_URL_N)
    time.sleep(5)
    # Open the lasted time pages in the select date and download the file
    Spider.open_select_date_time_page_and_download(target_date=target_date)
    pass

