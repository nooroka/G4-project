import re

def remove_cg_dinucleotides_in_fasta(input_file, output_file, chunk_size=1000000):
    """
    Удаляет CG-динуклеотиды из последовательности генома в формате FASTA.
    Игнорирует регистр и обрабатывает перекрывающиеся CG.

    :param input_file: Путь к FASTA-файлу с последовательностью генома.
    :param output_file: Путь к файлу для сохранения очищенной последовательности.
    :param chunk_size: Размер блока для чтения (по умолчанию 1 млн символов).
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            buffer = ""  # Буфер для хранения части последовательности
            in_sequence = False  # Флаг для определения, находимся ли мы внутри последовательности

            while True:
                chunk = infile.read(chunk_size)  # Читаем chunk_size символов
                if not chunk:  # Если файл закончился
                    break

                for line in chunk.splitlines():  # Обрабатываем каждую строку в chunk
                    if line.startswith(">"):  # Если это заголовок FASTA
                        if buffer:  # Если в буфере есть данные, обрабатываем их
                            buffer = remove_cg_overlapping(buffer)
                            outfile.write(buffer)
                            buffer = ""
                        outfile.write(line + "\n")  # Записываем заголовок
                        in_sequence = False
                    else:
                        buffer += line.strip()  # Добавляем последовательность в буфер
                        in_sequence = True

                # Если буфер превышает chunk_size, обрабатываем его
                if len(buffer) >= chunk_size:
                    buffer = remove_cg_overlapping(buffer)
                    outfile.write(buffer)
                    buffer = ""

            # Обрабатываем оставшиеся данные в буфере
            if buffer:
                buffer = remove_cg_overlapping(buffer)
                outfile.write(buffer)

        print(f"Очищенная последовательность сохранена в файл: {output_file}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


def remove_cg_overlapping(sequence):
    """
    Удаляет все CG-динуклеотиды, включая перекрывающиеся, с учётом игнорирования регистра.
    """
    # Используем регулярное выражение для поиска CG в любом регистре
    cg_pattern = re.compile(r'CG', flags=re.IGNORECASE)
    cleaned_sequence = ""
    i = 0
    while i < len(sequence):
        match = cg_pattern.match(sequence, i)  # Ищем CG, начиная с позиции i
        if match:
            i += 2  # Пропускаем CG
        else:
            cleaned_sequence += sequence[i]
            i += 1
    return cleaned_sequence


# Точка входа в программу
if __name__ == "__main__":
    # Укажите пути к входному и выходному файлам
    input_file = "../../hg19_new.fna"  # FASTA-файл с последовательностью генома
    output_file = "../../cleaned_genome.fasta"  # Файл для очищенной последовательности

    # Запуск функции для обработки FASTA-файла
    remove_cg_dinucleotides_in_fasta(input_file, output_file)
