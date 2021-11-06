import pandas as pd


def find_name_with_usage(usage_over, usage_under):
    df = pd.read_csv("name_count_final.csv")

    new_df = df.loc[(df['2021'] >= usage_over) & (df['2021'] <= usage_under)]
    pd.set_option('max_rows', None)
    print(new_df)


def main():
    find_name_with_usage(600, 650)


if __name__ == '__main__':
    main()
