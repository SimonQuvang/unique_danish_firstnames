import name_analysis as name_analysis


def main():
    print(f'Specify minimum amount of people with the name: ')
    minimum_persons_with_name = int(input())
    print(f'Specify maximum amount of people with name: ')
    maximum_persons_with_name = int(input())
    name_analysis.find_name_with_usage(minimum_persons_with_name, maximum_persons_with_name)


if __name__ == '__main__':
    main()
