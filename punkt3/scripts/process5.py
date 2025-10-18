import re
import subprocess
import os

def remove_cg_dinucleotides_in_fasta(input_file, output_file, bed_file, chrom_sizes_file, subtracted_bed_file, chunk_size=1000000):
    """
    Удаляет CG-динуклеотиды из последовательности генома в формате FASTA.
    Сохраняет координаты удалённых CG в BED-файл и использует bedtools subtract для вычитания этих регионов.

    :param input_file: Путь к FASTA-файлу с последовательностью генома.
    :param output_file: Путь к файлу для сохранения очищенной последовательности.
    :param bed_file: Путь к BED-файлу для сохранения координат удалённых CG.
    :param chrom_sizes_file: Путь к файлу с размерами хромосом.
    :param subtracted_bed_file: Путь к BED-файлу для сохранения результата вычитания.
    :param chunk_size: Размер блока для чтения (по умолчанию 1 млн символов).
    """
    try:
        # Шаг 1: Удаление CG-динуклеотидов и сохранение координат
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile, open(bed_file, 'w') as bedfile:
            buffer = ""
            in_sequence = False
            chromosome = ""
            position = 0

            while True:
                chunk = infile.read(chunk_size)
                if not chunk:
                    break

                for line in chunk.splitlines():
                    if line.startswith(">"):
                        if buffer:
                            buffer, removed_positions = remove_cg_overlapping(buffer, position)
                            outfile.write(buffer)
                            write_bed_coordinates(bedfile, chromosome, removed_positions)
                            buffer = ""
                            position = 0
                        chromosome = line[1:].split()[0]
                        outfile.write(line + "\n")
                        in_sequence = False
                    else:
                        buffer += line.strip()
                        in_sequence = True

                if len(buffer) >= chunk_size:
                    buffer, removed_positions = remove_cg_overlapping(buffer, position)
                    outfile.write(buffer)
                    write_bed_coordinates(bedfile, chromosome, removed_positions)
                    buffer = ""
                    position += len(buffer)

            if buffer:
                buffer, removed_positions = remove_cg_overlapping(buffer, position)
                outfile.write(buffer)
                write_bed_coordinates(bedfile, chromosome, removed_positions)

        print(f"Очищенная последовательность сохранена в файл: {output_file}")
        print(f"Координаты удалённых CG-динуклеотидов сохранены в файл: {bed_file}")

        # Шаг 2: Создание файла с размерами хромосом (если его нет)
        if not os.path.exists(chrom_sizes_file):
            create_chrom_sizes_file(input_file, chrom_sizes_file)

        # Шаг 3: Создание BED-файла для всего генома (начиная с 1)
        genome_bed_file = "genome_regions.bed"
        create_genome_bed_file(chrom_sizes_file, genome_bed_file)

        # Шаг 4: Использование bedtools subtract
        run_bedtools_subtract(genome_bed_file, bed_file, subtracted_bed_file)
        print(f"Результат bedtools subtract сохранён в файл: {subtracted_bed_file}")

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
        match = cg_pattern.match(sequence, i)
        if match:
            removed_positions.append(start_position + i + 1)  # Корректировка на 1-базированные координаты
            i += 2
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
        bedfile.write(f"{chromosome}\t{pos - 1}\t{pos + 1}\tCG\t0\t+\n")  # Корректировка на 0-базированные координаты


def create_chrom_sizes_file(fasta_file, chrom_sizes_file):
    """
    Создаёт файл с размерами хромосом на основе FASTA-файла.

    :param fasta_file: Путь к FASTA-файлу.
    :param chrom_sizes_file: Путь к файлу для сохранения размеров хромосом.
    """
    try:
        with open(fasta_file, 'r') as infile, open(chrom_sizes_file, 'w') as outfile:
            chromosome = ""
            length = 0
            for line in infile:
                if line.startswith(">"):
                    if chromosome:
                        outfile.write(f"{chromosome}\t{length}\n")
                    chromosome = line[1:].split()[0]
                    length = 0
                else:
                    length += len(line.strip())
            if chromosome:
                outfile.write(f"{chromosome}\t{length}\n")
        print(f"Файл с размерами хромосом создан: {chrom_sizes_file}")
    except Exception as e:
        print(f"Ошибка при создании файла с размерами хромосом: {e}")


def create_genome_bed_file(chrom_sizes_file, genome_bed_file):
    """
    Создаёт BED-файл для всего генома на основе файла с размерами хромосом.

    :param chrom_sizes_file: Путь к файлу с размерами хромосом.
    :param genome_bed_file: Путь к выходному BED-файлу.
    """
    try:
        with open(chrom_sizes_file, 'r') as infile, open(genome_bed_file, 'w') as outfile:
            for line in infile:
                chromosome, length = line.strip().split()
                outfile.write(f"{chromosome}\t0\t{length}\n")  # 0-базированные координаты
        print(f"BED-файл для всего генома создан: {genome_bed_file}")
    except Exception as e:
        print(f"Ошибка при создании BED-файла для всего генома: {e}")


def run_bedtools_subtract(a_file, b_file, output_file):
    """
    Выполняет команду bedtools subtract для вычитания регионов.

    :param a_file: Путь к BED-файлу A (регионы, из которых вычитаем).
    :param b_file: Путь к BED-файлу B (регионы, которые вычитаем).
    :param output_file: Путь к выходному BED-файлу.
    """
    try:
        command = ["bedtools", "subtract", "-a", a_file, "-b", b_file]
        with open(output_file, 'w') as outfile:
            subprocess.run(command, stdout=outfile, check=True)
        print(f"Результат bedtools subtract сохранён в файл: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении bedtools subtract: {e}")


# Точка входа в программу
if __name__ == "__main__":
    # Укажите пути к файлам
    input_file = "../../hg19_new.fna"  # FASTA-файл с последовательностью генома
    output_file = "../../cleaned_genome5.fasta"  # Файл для очищенной последовательности
    bed_file = "../../removed_cg_coordinates5.bed"  # Файл для координат удалённых CG
    chrom_sizes_file = "../../hg19.chrom5.sizes"  # Файл с размерами хромосом
    subtracted_bed_file = "../../subtracted_regions5.bed"  # Файл для результата вычитания

    # Запуск функции для обработки FASTA-файла
    remove_cg_dinucleotides_in_fasta(input_file, output_file, bed_file, chrom_sizes_file, subtracted_bed_file)
