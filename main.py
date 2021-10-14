

# get the name lists from https://familieretshuset.dk/navne/navne/godkendte-fornavne

# data class for name with the name, the sex, and amount of people with that name.

# Dansk statstik have a list of how many have the name. Use that to get the amount of people with the name
# Probably need to use an API or so, so find it.

# Maybe save the data to an sql table

from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests

@dataclass
class Firstname:
    name: str
    amount: int


def get_firstname_usage(name):
    url = "https://www.dst.dk/da/Statistik/emner/borgere/navne/HvorMange?ajax=1"
    payload = f'firstName={name}&lastName='
    headers = {
        'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        'Accept': 'text/html, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    html = BeautifulSoup(response.text, features="html.parser")
    tr = html.select('tbody tr')
    amount_total = 0

    # selects the 1st tr which are men with the name, and then the 3rd td which is the number for 2021.
    amount_1st = int(tr[0].select('td')[2].text.replace('.', ''))
    amount_total = amount_total + amount_1st

    if tr[1]:
        # selects the 2nd tr which are women with the name, and then the 3rd td which is the number for 2021.
        amount_2nd = int(tr[1].select('td')[2].text.replace('.', ''))
        amount_total = amount_total + amount_2nd

    # creates an object using dataclasses to return
    first_name = Firstname(name=name, amount=amount_total)
    return first_name


def load_xls_data():
    # Load the files, read row by row, and call the get first_name_usage function. Add the dataclass to an list, return list

def main(name):
    list_of_names_objects = [get_firstname_usage(name)]

    # write a function to read the xls files and loop through all the names.
    print(list_of_names_objects)



if __name__ == '__main__':
    main('Simon')