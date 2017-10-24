import itertools
import pandas as pd
import requests
from bs4 import BeautifulSoup


class H1BData:

    def __init__(self, employer=None, title=None, location=None, year=None):
        self.base_url = 'http://h1bdata.info/index.php?'
        self.employer = self.get_employer(employer)
        self.job_title = self.get_title(title)
        self.loc = self.get_location(location)
        self.years = self.get_years(year)
        self.data = self.pull_data()

    @property
    def data(self):
        return self.data

    # Pulls the data as an HTML page and cleans it up. Returns it as a dataframe.
    def pull_data(self):
        url = self.form_search()
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        page.close()
        tables = soup.find_all('table')
        args = [iter(tables[0].stripped_strings)] * 7
        data_list = list(itertools.zip_longest(*args))
        data_list = [x for x in data_list if x[6] == 'CERTIFIED']
        data = pd.DataFrame(data_list)
        # 0: ID, 1: Decision Date, 2: Employer, 3: Status, 4: Job Title, 5: Wage Offer
        del data[4], data[6]
        data.columns = ['Employer', 'Title', 'Salary', 'Location', 'Start Date']
        data['Salary'] = data['Salary'].convert_objects(convert_numeric=True)
        data['Start Date'] = data['Start Date'].convert_objects(convert_dates=True)
        return data

    def data_to_json(self, path):
        self.data_to_json(path=path)

    @staticmethod
    def get_employer(emp):
        if emp is None:
            return 'emp=&'
        else:
            return 'emp='+emp+'&'

    @staticmethod
    def get_title(title):
        if title is None:
            return 'job=&'
        else:
            return 'job='+title+'&'

    @staticmethod
    def get_location(loc):
        if loc is None:
            return 'city=&'
        else:
            return 'city='+loc+'&'

    @staticmethod
    def get_years(years):
        if years is None:
            return 'year=All+Years'
        # We can choose: 2017, 2016, 2015, 2014, 2013, 2012
        else:
            if 2011 < years < 2018:
                return 'year='+str(years)
            else:
                return 'year=All+Years'

    def form_search(self):
        search = self.base_url+self.employer+self.job_title+self.loc+self.years
        if search == 'http://h1bdata.info/index.php?em=&job=&city=&year=All+Years':
            return 'You didn\'t enter anything'
        return search

    @property
    def highest_salaries(self, num=None):
        data = self.get_highest_salaries()
        if num is None:
            return data
        else:
            return data.ix[0:num]

    @property
    def lowest_salaries(self, num=None):
        data = self.get_lowest_salaries()
        if num is None:
            return data
        else:
            return data.ix[0:num]

    def get_highest_salaries(self):
        high = self.data.sort_values('Salary', ascending=False)
        return high

    def get_lowest_salaries(self):
        low = self.data.sort_values('Salary')
        return low
