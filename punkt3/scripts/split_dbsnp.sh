#!/bin/bash

WORK_DIR="/mnt/work/nooroka"

# 1. Распаковываем основной файл
if [ ! -f "${WORK_DIR}/GCF_000001405.25" ]; then
    echo "Распаковываем GCF_000001405.25.gz..."
    gunzip "${WORK_DIR}/GCF_000001405.25.gz" || { echo "Ошибка распаковки!"; exit 1; }
fi

# 2. Создаем папку для результатов
mkdir -p "${WORK_DIR}/dbSNP_chromosomes"
cd "${WORK_DIR}/dbSNP_chromosomes" || { echo "Не могу перейти в ${WORK_DIR}/dbSNP_chromosomes!"; exit 1; }

# 3. Создаем маппинг между NC-номерами и обычными именами хромосом
declare -A CHR_MAP=(
    ["NC_000001.10"]="chr1"
    ["NC_000002.11"]="chr2"
    ["NC_000003.11"]="chr3"
    ["NC_000004.11"]="chr4"
    ["NC_000005.9"]="chr5"
    ["NC_000006.11"]="chr6"
    ["NC_000007.13"]="chr7"
    ["NC_000008.10"]="chr8"
    ["NC_000009.11"]="chr9"
    ["NC_000010.10"]="chr10"
    ["NC_000011.9"]="chr11"
    ["NC_000012.11"]="chr12"
    ["NC_000013.10"]="chr13"
    ["NC_000014.8"]="chr14"
    ["NC_000015.9"]="chr15"
    ["NC_000016.9"]="chr16"
    ["NC_000017.10"]="chr17"
    ["NC_000018.9"]="chr18"
    ["NC_000019.9"]="chr19"
    ["NC_000020.10"]="chr20"
    ["NC_000021.8"]="chr21"
    ["NC_000022.10"]="chr22"
    ["NC_000023.10"]="chrX"
    ["NC_000024.9"]="chrY"
    ["NC_012920.1"]="chrMT"
)

# 4. Обрабатываем каждую хромосому в цикле
for NC_ID in "${!CHR_MAP[@]}"; do
    CHR_NAME="${CHR_MAP[$NC_ID]}"
    echo "Обрабатываю ${NC_ID} как ${CHR_NAME}..."

    # Извлекаем данные для хромосомы
    awk -v nc="$NC_ID" '$1 == nc' "${WORK_DIR}/GCF_000001405.25" > "${CHR_NAME}.vcf"

    # Проверяем, не пустой ли файл
    if [ ! -s "${CHR_NAME}.vcf" ]; then
        echo "Нет данных для ${CHR_NAME}, пропускаем."
        rm "${CHR_NAME}.vcf"
        continue
    fi

    # Сжимаем и индексируем
    bgzip "${CHR_NAME}.vcf"
    tabix -p vcf "${CHR_NAME}.vcf.gz"

    echo "${CHR_NAME}.vcf.gz готов!"
done

echo "Готово! Все файлы сохранены в ${WORK_DIR}/dbSNP_chromosomes."
