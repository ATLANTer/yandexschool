import os, json, requests, argparse

url = "https://api.github.com/search/repositories"

arguments = argparse.ArgumentParser()
arguments.add_argument('-v', '--value', type=str, help='строка для поиска')
arguments.add_argument('-f', '--file', type=str, help='путь к выходному json файлу')
args = arguments.parse_args()

if os.path.exists(args.file):
    print('Файл с таким названием уже сущкствует.')
    print('Хотите его перезаписать? (y/n)')
    if input() == 'n':
        exit()

keyword_repositories = requests.get(url, params={'q': args.value, 'sort': 'stars', 'order': 'desc'})
keyword_repositories_json = json.dumps(keyword_repositories.json(), indent=2)
with open(args.file, "w") as file:
    file.write(keyword_repositories_json)
