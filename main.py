import Salary.salary as salary


def main():
    soft_eng = salary.H1BData()
    soft_eng.base_url = 'http://visadoor.com/h1b/index?company=&job=software+engineer&state=&year=2016&submit=Search'
    salaries = soft_eng.pull_data()
    for k, v in salaries.items():
        print('Company:', k)
        print('Title:', v[0])
        print('Salary:', v[1], '\n')


if __name__ == '__main__':
    main()
