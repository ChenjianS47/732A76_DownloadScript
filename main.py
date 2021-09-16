import time
import pandas as pd
from datetime import datetime

from Config import *
from Core.Spider import Spider

dates = pd.date_range(start_date, final_date).strftime('%b %d %Y').to_list()
Spider = Spider(chrome_driver=chrome_driver, wayback_machine_url=Wayback_Machine_URL,
                download_directory=Download_directory)
for target_date in dates:
    if datetime.strptime(target_date, '%b %d %Y').date() < datetime.strptime('JUL 17 2020', '%b %d %Y').date():
        Target_URL_N = Target_URL[0]
        pass
    else:
        Target_URL_N = Target_URL[1]
        pass
    Spider.open_browser()
    Spider.open_website(target_url=Target_URL_N)
    time.sleep(10)
    Spider.open_select_date_time_page_and_download(target_date=target_date)
    pass

