#!/usr/bin/env python3
import sys
import gzip
import os


def smart_open(path, mode='r'):
    """
    Открывает файл, автоматически определяя:
    - '-' -> stdin/stdout
    - '.gz' по расширению -> gzip, текстовый режим
    - иначе -> обычный open
    """
    if path == '-':
        return sys.stdin if 'r' in mode else sys.stdout

    if path.endswith('.gz'):
        # 'rt'/'wt' — текстовый режим для gzip (строки, не байты)
        return gzip.open(path, mode + 't')

    return open(path, mode)


def parse_line_numbers(lines):
    return {int(line.split()[0]) for line in lines if line.strip()}


def read_lines(path):
    f = smart_open(path, 'r')
    try:
        return f.readlines()
    finally:
        # stdin закрывать не нужно
        if path != '-':
            f.close()


def select_lines(file_path, target_line_numbers_path, output_path):
    # Нельзя читать stdin дважды — проверяем конфликт
    if file_path == '-' and target_line_numbers_path == '-':
        print("Error: both inputs cannot be stdin", file=sys.stderr)
        sys.exit(1)

    target_nums = parse_line_numbers(read_lines(target_line_numbers_path))

    in_f = smart_open(file_path, 'r')
    out_f = smart_open(output_path, 'w')

    try:
        for i, line in enumerate(in_f, start=1):
            if i not in target_nums:
                out_f.write(line)
    finally:
        if file_path != '-':
            in_f.close()
        if output_path != '-':
            out_f.close()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(
            "Usage: python select_lines.py <input_file[.gz]|-> "
            "<target_numbers_file[.gz]|-> <output_file[.gz]|->",
            file=sys.stderr,
        )
        sys.exit(1)

    select_lines(sys.argv[1], sys.argv[2], sys.argv[3])
