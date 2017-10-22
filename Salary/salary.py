import requests
from collections import defaultdict
import pandas as pd
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

    # Pulls the data as an HTML page and cleans it up. Returns it as a dictionary with the employers
    # as keys, and list of a tuples with (title, salary).
    def pull_data(self):
        employer, title, wage = [], [], []
        url = self.form_search()
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        tables = soup.find_all('table')
        i = 0
        for item in tables[0].stripped_strings:
            if i < 5:
                if i == 2:
                    employer.append(item)
                    i += 1
                elif i == 4:
                    title.append(item)
                    i += 1
                else:
                    i += 1
            else:
                i = 0
                wage.append(item)
        raw_data = [employer, title, wage]
        data = self.clean_data(raw_data)
        return data

    # Takes the raw data and turns in into a defaultdict(list) with the
    # form {employer: [[title,salary], [title, salary]].
    def clean_data(self, raw_data):
        data_dict = defaultdict(list)
        emp, title, salary = raw_data[0], raw_data[1], raw_data[2]
        # Don't start at 0, so you can remove the data titles.
        for i in range(1, len(emp)):
            current_job = [title[i], salary[i]]
            if emp[i] in data_dict:
                data_dict[emp[i]].append(current_job)
            else:
                data_dict[emp[i]] = current_job
        return data_dict


    def data_to_json(self):
        # 0: ID, 1: Decision Date, 2: Employer, 3: Status, 4: Job Title, 5: Wage Offer
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
