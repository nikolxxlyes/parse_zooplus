from selenium import webdriver
from bs4 import BeautifulSoup
from bs4.element import Comment
import pandas
import csv

from datetime import datetime


class ZooplusScraper():
    def __init__(self, url, columns_class, query_params: dict = {},
                 page_end: int = 1, filter_ad: bool = True, ad_class: str = 'dr-sam'):
        self.url = url
        self.query_params = query_params
        self.page_end = page_end
        self.use_pages = page_end != 1
        self.filter_ad = filter_ad
        self.ad_class = ad_class
        self.columns_class = columns_class
        self.csv_data = {name: [] for name in self.columns_class.keys()}

    def collect_data(self, driver_file, webdriver_=webdriver.Chrome):
        driver = webdriver_(executable_path=driver_file)
        self.driver = driver

        driver.maximize_window()

        driver.get(self.format_url(page=1))
        driver.implicitly_wait(10)

        self.deny_cookies()

        if self.use_pages:
            self.open_new_windows()
        driver.implicitly_wait(10)

        for window in driver.window_handles:
            self.parse_window_data(window)
        driver.quit()

    def format_url(self, page: int) -> str:
        if self.query_params:
            query_list = []
            for key, value in self.query_params.items():
                if key == 'page':
                    value = page
                query_list.append(f'{key}={value}')

            params = '&'.join(query_list)
            return f'{self.url}?{params}'
        return self.url

    def deny_cookies(self):
        accept_btn = self.driver.find_element_by_xpath('//*[@id="onetrust-reject-all-handler"]')
        accept_btn.click()

    def open_new_windows(self):
        for page_num in range(2, self.page_end + 1):
            self.driver.execute_script("window.open('{}')".format(self.format_url(page=page_num)))

            last_window = self.driver.window_handles[-1]
            self.driver.switch_to.window(last_window)

    def parse_window_data(self, window):
        self.driver.switch_to.window(window)
        self.driver.implicitly_wait(10)

        posts_div = self.driver.find_element_by_class_name('search-results').get_attribute('innerHTML')
        posts = BeautifulSoup(posts_div, "html.parser").children

        for post in posts:
            if isinstance(post, Comment):
                continue
            if self.filter_ad and self.ad_class in post['class']:
                continue
            for col_name, col_class in self.columns_class.items():
                try:
                    elem = post.find(attrs={'class': col_class})
                    if hasattr(self, f'get_{col_name}'):
                        col_handler = getattr(self, f'get_{col_name}')
                        text = col_handler(elem)
                    else:
                        text = self.clean_parse_text(elem.text)
                except:
                    text = ''
                finally:
                    self.csv_data[col_name].append(text)

    def clean_parse_text(self, text: str) -> str:
        return text.strip().replace('\n', ' ')

    def get_star_rate(self, stars_box) -> int:
        rate = 0
        for star in stars_box.children:
            star_class = star['class']
            if 'star-rating__half-star' in star_class:
                rate += 0.5
            elif 'u-text-xxlight' in star_class:
                rate += 0
            else:
                rate += 1
        return rate

    def create_csv(self, path_to_csv: str = 'example.csv'):
        df = pandas.DataFrame(self.csv_data, columns=self.csv_data.keys())
        df.to_csv(path_to_csv, index=False, header=True, sep=',', quotechar='"',
                  quoting=csv.QUOTE_MINIMAL)


if __name__ == '__main__':
    # now = datetime.now()

    # Change variables
    driver_file = r'D:\chromedriver.exe'
    webdriver_ = webdriver.Chrome
    path_to_csv = 'example.csv'

    url = "https://www.zooplus.de/tierarzt/results"
    query_params = {
        'animal_99': 'true',
        'page': '',
    }
    columns_class = {
        'name': 'result-intro__title',
        'job': 'result-intro__subtitle',
        'work_time': 'daily-hours__range',
        'work_status': 'daily-hours__note',
        'address': 'result-intro__address',
        'star_rate': 'star-rating',
        'recommendation': 'result-intro__rating__note',
    }

    parser = ZooplusScraper(url, query_params=query_params, columns_class=columns_class, page_end=3)
    parser.collect_data(driver_file=driver_file, webdriver_=webdriver_)
    parser.create_csv(path_to_csv=path_to_csv)

    # print('done with {} sec'.format(datetime.now() - now))
