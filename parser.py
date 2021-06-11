import os, json, requests, argparse

URL = "https://api.github.com/search/repositories"


def argument_parsing(): # python parser.py --help
    arguments = argparse.ArgumentParser()
    arguments.add_argument('-v', '--value', type=str, help='строка для поиска')
    arguments.add_argument('-f', '--file', type=str, help='путь к выходному json файлу')
    args = arguments.parse_args()
    return args


def validation_args(args):
    if args.value is None or args.file is None:
        print('Check your starting arguments. That is incorrect.')
        exit()
    if os.path.exists(args.file):
        print('Файл с таким названием уже сущкствует.')
        print('Хотите его перезаписать? (y/n)')
        if input() == 'n':
            exit()


def get_query(args):
    items_list = list()
    keyword_repositories = requests.get(URL, params={'q': args.value, 'sort': 'stars', 'order': 'desc', 'per_page': 100, 'page': 1})
    counter = 2
    while keyword_repositories.status_code == 200 and keyword_repositories.json().get('items') is not None:
        items_list.extend(keyword_repositories.json().get('items'))
        keyword_repositories = requests.get(URL, params={'q': args.value, 'sort': 'stars', 'order': 'desc', 'per_page': 100, 'page': counter})
        counter += 1
    return items_list


def write_file(data, saved_file):
    with open(saved_file, "w") as file:
        json.dump(data, file, indent=2)


if __name__ == "__main__":
    arguments = argument_parsing()
    validation_args(arguments)
    data = get_query(arguments)
    write_file(data, arguments.file)