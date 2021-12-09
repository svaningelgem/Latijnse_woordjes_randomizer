import csv
import random
from pathlib import Path
from typing import List

CSV_DIR = Path(__file__).parent / '../csvs'


def _load_data(dir) -> List:
    data = []

    for filename in dir.rglob('*.csv'):
        if filename.name == 'output.csv':
            continue

        with open(filename, encoding='utf8') as fp:
            reader = csv.reader(fp)

            data.extend(
                [filename.stem] + line
                for line in reader
                if line[0] != 'Latijn'
            )

    return data


def start_test():
    data = _load_data(CSV_DIR)

    while True:
        r = random.choice(data)
        print(f'{r[1]} (q = quit)> ', end='')
        v = input()
        if v.lower() in ['q', 'quit']:
            break

        show = f' --> {r[0]}: {r[1]}'
        if r[2]:
            show += f' ({r[2]})'
        show += f' = {r[3]}'
        if r[4]:
            show += f' ({r[4]})'

        print(show)

        print('')
        print('')

    print("That's all folks!")


if __name__ == '__main__':
    start_test()
