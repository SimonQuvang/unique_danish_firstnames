import pandas as pd


def main():
    # load dataframe from csv
    df = pd.read_csv("names_count.csv")

    new_df = df.loc[(df['2021'] == 0) & (df['2021'] == 0)]
    # print dataframe
    print(new_df)


if __name__ == '__main__':
    main()