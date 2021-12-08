import csv
from pathlib import Path

from tess import image2data

try:
    from PIL import Image
except ImportError:
    import Image

SCAN_DIR = Path(__file__).parent / '../scans'


def _cleanup_line(line):
    line = [x.replace('Mm', 'm').replace('Vv', 'v') for x in line.values()]
    if not line:
        return []

    if line[0].isnumeric():
        line.pop(0)

    return line


def _group_horizontally(paper):
    for k, v in paper.items():
        line = {x: v[x] for x in sorted(v)}

        prev_coord = None
        running_sum = 0
        new_line = {}
        for coord, entry in line.items():
            entry = entry[0]

            if prev_coord and coord < running_sum + 20:
                new_line[prev_coord] += ' ' + entry[0]
            else:
                prev_coord = coord
                new_line[prev_coord] = entry[0]

            running_sum = coord + entry[1]

        paper[k] = _cleanup_line(new_line)

    return paper


def _group_vertically(paper):
    # Sort by top
    paper = {k: paper[k] for k in sorted(paper)}

    # Group it. (max 20 difference in high)
    new_paper = {}
    prev_coord = None
    for coord, entry in paper.items():
        if prev_coord and prev_coord + 20 > coord:  # belong to previous one
            new_paper[prev_coord].update(entry)
        else:
            prev_coord = coord
            new_paper[prev_coord] = entry

    return _group_horizontally(new_paper)


def _load_data(img: Path, language: str = 'nld'):
    data_nld = image2data(img, language=language)
    data_nld = iter(data_nld.splitlines())

    headers = next(data_nld).split('\t')

    paper = {}

    for line in data_nld:
        line = dict(zip(headers, line.split('\t')))
        if line['text'].strip() == '':
            continue

        paper.setdefault(int(line['top']), {}).setdefault(int(line['left']), []).append((line['text'], int(line['width'])))

    return _group_vertically(paper)


def _load_scans_from(path):
    with open(Path(__file__).parent / '../csvs/output.csv', 'w', encoding='utf8', newline='') as fp:
        writer = csv.writer(fp)
        writer.writerow(['Latijn', 'Genitief', 'Vertaling', 'Geheugensteun'])

        for img in path.rglob('*.jpg'):
            print('Working on', img)

            paper = _load_data(img)
            for v in paper.values():
                if len(v) <= 1: continue

                writer.writerow(v)


if __name__ == '__main__':
    _load_scans_from(SCAN_DIR)
