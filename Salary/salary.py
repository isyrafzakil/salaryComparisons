import itertools
import pandas as pd
import requests
from bs4 import BeautifulSoup


class H1BData:

    def __init__(self):
        self.base_url = 'http://visadoor.com/h1b/index?'
        # Use this URL to test it. I'll add more tests tomorrow.
        # self.base_url = 'http://visadoor.com/h1b/index?company=&job=software+engineer&state=&year=2016&submit=Search'
        self.employer = self.get_employer()
        self.job_title = self.get_title()
        self.city = self.get_city()
        self.years = self.get_years()

    # Pulls the data as an HTML page and cleans it up. Returns it as a dataframe.
    def pull_data(self):
        url = self.form_search()
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        tables = soup.find_all('table')
        args = [iter(tables[0].stripped_strings)] * 6
        data_list = list(itertools.zip_longest(*args))
        data = pd.DataFrame(data_list[1:])
        # 0: ID, 1: Decision Date, 2: Employer, 3: Status, 4: Job Title, 5: Wage Offer
        del data[0], data[1], data[3]
        data.columns = ['Employer', 'Title', 'Salary']
        return data

    def data_to_json(self):
        return None

    def get_employer(self, emp='&'):
        set_emp = 'em='+emp
        return set_emp

    def get_title(self, title='&'):
        set_title = 'job='+title
        return set_title

    def get_city(self, city='&'):
        set_city = 'city='+city
        return set_city

    def get_years(self, years='2016'):
        set_years = 'year='+years
        # We can choose: 2017, 2016, 2015, 2014, 2013, 2012
        return set_years

    def form_search(self):
        search = self.base_url+self.employer+self.job_title+self.city+self.years+'&submit=Search'
        return search
