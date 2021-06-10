import os, json, requests, argparse

URL = "https://api.github.com/search/repositories"


def argument_parsing():
    global args
    arguments = argparse.ArgumentParser()
    arguments.add_argument('-v', '--value', type=str, help='строка для поиска')
    arguments.add_argument('-f', '--file', type=str, help='путь к выходному json файлу')
    args = arguments.parse_args()


def validation_args():
    if args.value is None or args.file is None:
        print('Check your starting arguments. That is incorrect.')
        exit()
    if os.path.exists(args.file):
        print('Файл с таким названием уже сущкствует.')
        print('Хотите его перезаписать? (y/n)')
        if input() == 'n':
            exit()


def get_query():
    items_dict = dict()
    items_dict['items'] = list()
    keyword_repositories = requests.get(URL, params={'q': args.value, 'sort': 'stars', 'order': 'desc', 'per_page': 100, 'page': 1})
    items_dict['items'].extend(keyword_repositories.json().get('items'))
    counter = 2
    while keyword_repositories.status_code == 200 and keyword_repositories.json()['items']:
        keyword_repositories = requests.get(URL, params={'q': args.value, 'sort': 'stars', 'order': 'desc', 'per_page': 100, 'page': counter})
        items_dict['items'].extend(keyword_repositories.json()['items'])
        counter += 1
    return items_dict


def write_file(data):
    with open(args.file, "w") as file:
        json.dump(data, file, indent=2)


if __name__ == "__main__":
    argument_parsing()
    validation_args()
    data = get_query()
    write_file(data)