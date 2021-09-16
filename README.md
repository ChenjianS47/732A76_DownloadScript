# WayBackMachine_FHM_COVID-19_statistics
## Requirements for usage
First, you need to install 2 python package pandas and selenium by using the command below
pip install pandas
pip install selenium

Then you need to download the chromedriver from https://chromedriver.chromium.org/
Remember that you need to download the version that suitable for your chrome browser
Afther down loading the suitable chromedriver, add the Chrome directory to the system PATH, usually C:\Program Files (x86)\Google\Chrome\Application(For Windows user)

As for linux user, I am not sure where it is, maybe you could search this in the Internet

## About Config
### Location of chrome driver
chrome_driver = r"C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"

### Url for Wayback Machine
Wayback_Machine_URL = 'https://web.archive.org/'

### Target URL
Target_URL = ('https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/'
              'bekraftade-fall-i-sverige',
              'https://www.folkhalsomyndigheten.se/smittskydd-beredskap/utbrott/aktuella-utbrott/covid-19/' \
             'statistik-och-analyser/bekraftade-fall-i-sverige/')

### Define the start date and final date
start_date = 'APR 03 2020'
final_date = 'SEP 16 2021'

### Download directory
Download_directory = r'G:\LiU\732A76_Research_Project\data'


## License
-------

pysrcds is distributed under the MIT license. See
[LICENSE.md](https://github.com/ChenjianS47/ChenjianS47-WayBackMachine_FHM_COVID-19_statistics/blob/5a2344ecf1840d73396514fbf2e7bb89235d3fe7/LICENSE)
for more information.
