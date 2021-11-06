# get the name lists from https://familieretshuset.dk/navne/navne/godkendte-fornavne

# data class for name with the name, the sex, and amount of people with that name.

# Dansk statstik have a list of how many have the name. Use that to get the amount of people with the name
# Probably need to use an API or so, so find it.

# Maybe save the data to an sql table
import time
import urllib.parse
import requests
import pandas as pd

list_of_names_objects = []


def get_website_data(name):
    url = "https://www.dst.dk/da/Statistik/emner/borgere/navne/HvorMange?ajax=1"
    # urllib.parse.quote replaces special char in the names to something that can be read in a url
    payload = f'firstName={urllib.parse.quote(name)}&lastName='
    headers = {
            'sec-ch-ua': '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
            'Accept': 'text/html, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"'
    }
    # Printing out the name, so you can see stuff is happening.
    print(f'{name=}')
    response = requests.request("POST", url, headers=headers, data=payload)

    list_of_dfs = pd.read_html(response.text, decimal=',', thousands='.')
    df = list_of_dfs[0]

    return name, int(df['2020'].sum()), int(df['2021'].sum())


def get_firstname_usage(name):
    time.sleep(1)
    try:
        return get_website_data(name)
    except:
        # Write a better except clause
        print("In the expection")
        time.sleep(5)
        return get_website_data(name)


def main():
    df = pd.read_excel('all_names.xls')

    for index, row in df.iterrows():
        row = get_firstname_usage(row['Name'])
        print(row)


if __name__ == '__main__':
    main()
