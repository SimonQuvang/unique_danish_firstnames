# get the name lists from https://familieretshuset.dk/navne/navne/godkendte-fornavne

# data class for name with the name, the sex, and amount of people with that name.

# Dansk statstik have a list of how many have the name. Use that to get the amount of people with the name
# Probably need to use an API or so, so find it.

# Maybe save the data to an sql table
import time
from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests
import csv
import xlrd
import pandas as pd

list_of_names_objects = []


@dataclass
class Firstname:
    name: str
    amount_2021: int
    amount_2020: int

    def get_as_row(self):
        return [self.name, self.amount_2020, self.amount_2021]


def save_to_csv(first_name):
    print(first_name)
    with open('names_count2.csv', 'a+', newline='', encoding='UTF-8') as file:
        # create the csv writer
        writer = csv.writer(file)
        # write a row to the csv file
        writer.writerow(first_name.get_as_row())
    #time.sleep(4)


def get_firstname_usage(name):
    time.sleep(1)
    url = "https://www.dst.dk/da/Statistik/emner/borgere/navne/HvorMange?ajax=1"
    payload = f'firstName={name}&lastName='
    headers = {
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'Accept': 'text/html, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"'
    }
    print(f'{name=}')
    response = requests.request("POST", url, headers=headers, data=payload)

    html = BeautifulSoup(response.text, features="html.parser")
    tr = html.select('tbody tr')
    amount_2020_total = 0
    amount_2021_total = 0
    print(tr)
    if 'Der er ingen med fornavnet' in tr[0].select_one('td').text:
        return save_to_csv(Firstname(name=name, amount_2020=amount_2020_total, amount_2021=amount_2021_total))

    # selects the 1st tr which are men with the name, and then the 3rd td which is the number for 2021.
    amount_2020_total = int(tr[0].select('td')[1].text.replace('.', ''))
    amount_2021_total = int(tr[0].select('td')[2].text.replace('.', ''))

    if len(tr) > 1:
        # selects the 2nd tr which are women with the name, and then the 3rd td which is the number for 2021.
        amount_2020_2nd = int(tr[1].select('td')[1].text.replace('.', ''))
        amount_2020_total += amount_2020_2nd
        amount_2021_2nd = int(tr[1].select('td')[2].text.replace('.', ''))
        amount_2021_total += amount_2021_2nd

    return save_to_csv(Firstname(name=name, amount_2020=amount_2020_total, amount_2021=amount_2021_total))


# Load the files, read row by row, and call the get first_name_usage function. Add the dataclass to an list, return list


def main():
    df = pd.read_excel('all_names.xls')

    df.apply(lambda x: get_firstname_usage(x['Name']), axis=1)



if __name__ == '__main__':
    main()
