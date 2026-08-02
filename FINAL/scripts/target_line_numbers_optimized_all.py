import sys

def select_lines(file_path, target_line_numbers_path, output_path):
    # Используем set для O(1) поиска вместо O(n)
    with open(target_line_numbers_path, 'r') as target_file:
        target_line_numbers = {
            int(line.split()[0])
            for line in target_file
        }

    # Пишем построчно — не грузим весь файл в память
    with open(file_path, 'r') as file, open(output_path, 'w') as out:
        for i, line in enumerate(file, start=1):
            if i not in target_line_numbers:
                out.write(line)

select_lines(sys.argv[1], sys.argv[2], sys.argv[3])
