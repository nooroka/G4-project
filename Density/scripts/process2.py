import re

def remove_cg_dinucleotides_in_fasta(input_file, output_file, bed_file, chunk_size=1000000):
    """
    Удаляет CG-динуклеотиды из последовательности генома в формате FASTA.
    Игнорирует регистр и обрабатывает перекрывающиеся CG.
    Сохраняет координаты удалённых CG-динуклеотидов в BED-файл.

    :param input_file: Путь к FASTA-файлу с последовательностью генома.
    :param output_file: Путь к файлу для сохранения очищенной последовательности.
    :param bed_file: Путь к BED-файлу для сохранения координат удалённых CG.
    :param chunk_size: Размер блока для чтения (по умолчанию 1 млн символов).
    """
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile, open(bed_file, 'w') as bedfile:
            buffer = ""  # Буфер для хранения части последовательности
            in_sequence = False  # Флаг для определения, находимся ли мы внутри последовательности
            chromosome = ""  # Имя текущей хромосомы
            position = 0  # Текущая позиция в последовательности

            while True:
                chunk = infile.read(chunk_size)  # Читаем chunk_size символов
                if not chunk:  # Если файл закончился
                    break

                for line in chunk.splitlines():  # Обрабатываем каждую строку в chunk
                    if line.startswith(">"):  # Если это заголовок FASTA
                        if buffer:  # Если в буфере есть данные, обрабатываем их
                            buffer, removed_positions = remove_cg_overlapping(buffer, position)
                            outfile.write(buffer)
                            write_bed_coordinates(bedfile, chromosome, removed_positions)
                            buffer = ""
                            position = 0
                        chromosome = line[1:].split()[0]  # Извлекаем имя хромосомы
                        outfile.write(line + "\n")  # Записываем заголовок
                        in_sequence = False
                    else:
                        buffer += line.strip()  # Добавляем последовательность в буфер
                        in_sequence = True

                # Если буфер превышает chunk_size, обрабатываем его
                if len(buffer) >= chunk_size:
                    buffer, removed_positions = remove_cg_overlapping(buffer, position)
                    outfile.write(buffer)
                    write_bed_coordinates(bedfile, chromosome, removed_positions)
                    buffer = ""
                    position += len(buffer)

            # Обрабатываем оставшиеся данные в буфере
            if buffer:
                buffer, removed_positions = remove_cg_overlapping(buffer, position)
                outfile.write(buffer)
                write_bed_coordinates(bedfile, chromosome, removed_positions)

        print(f"Очищенная последовательность сохранена в файл: {output_file}")
        print(f"Координаты удалённых CG-динуклеотидов сохранены в файл: {bed_file}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")


def remove_cg_overlapping(sequence, start_position):
    """
    Удаляет все CG-динуклеотиды, включая перекрывающиеся, с учётом игнорирования регистра.
    Возвращает очищенную последовательность и список позиций удалённых CG.

    :param sequence: Последовательность для обработки.
    :param start_position: Начальная позиция последовательности в геноме.
    :return: Очищенная последовательность и список позиций удалённых CG.
    """
    cg_pattern = re.compile(r'CG', flags=re.IGNORECASE)
    cleaned_sequence = ""
    removed_positions = []
    i = 0
    while i < len(sequence):
        match = cg_pattern.match(sequence, i)  # Ищем CG, начиная с позиции i
        if match:
            removed_positions.append(start_position + i)  # Сохраняем позицию удалённого CG
            i += 2  # Пропускаем CG
        else:
            cleaned_sequence += sequence[i]
            i += 1
    return cleaned_sequence, removed_positions


def write_bed_coordinates(bedfile, chromosome, positions):
    """
    Записывает координаты удалённых CG-динуклеотидов в BED-файл.

    :param bedfile: Файловый объект BED-файла.
    :param chromosome: Имя хромосомы.
    :param positions: Список позиций удалённых CG.
    """
    for pos in positions:
        bedfile.write(f"{chromosome}\t{pos}\t{pos + 2}\tCG\t0\t+\n")


# Точка входа в программу
if __name__ == "__main__":
    # Укажите пути к входному и выходному файлам
    input_file = "../../hg19_new.fna"  # FASTA-файл с последовательностью генома
    output_file = "../../cleaned_genome_2.fasta"  # Файл для очищенной последовательности
    bed_file = "../../removed_cg_coordinates.bed"  # Файл для координат удалённых CG

    # Запуск функции для обработки FASTA-файла
    remove_cg_dinucleotides_in_fasta(input_file, output_file, bed_file)
