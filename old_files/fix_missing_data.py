import urllib.parse
import pandas as pd
import requests
import numpy as np


def get_data(name):

    url = "https://www.dst.dk/da/Statistik/emner/borgere/navne/HvorMange?ajax=1"

    payload = f'firstName={urllib.parse.quote(name)}&lastName='

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

    list_of_dfs = pd.read_html(response.text,  decimal=',', thousands='.')
    df = list_of_dfs[0]


def load_df_and_find_missing_values():
    # load dataframe from csv
    df = pd.read_csv("names_count.csv")

    new_df = df.loc[(df['2020'] == 0) & (df['2021'] == 0)]
    # print dataframe
    print(new_df.shape)
    new_df.apply(lambda x: get_data(x['Name']), axis=1)


def load_df():
    df = pd.read_csv("names_count.csv")
    df2 = pd.read_csv("../names_count3.csv")
    new_df = df.loc[(df['2020'] != 0) & (df['2021'] != 0)]
    # print dataframe
    merged_df = pd.merge(df2, new_df, how='outer')
    print(merged_df)
    merged_df.to_csv('name_count_final.csv', index=False)


def main():
    load_df()


if __name__ == '__main__':
    main()
