import sys
def select_lines(file_path, target_line_numbers_path):
    with open(target_line_numbers_path, 'r') as target_file:
        target_line_numbers =list(set([int(line.strip().split()[0]) for line in target_file.readlines()])) #убираем дупликаты
 #       print("target "+str(target_line_numbers))
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    selected_lines = [line for i, line in enumerate(lines, start=1) if i in target_line_numbers]
    non_selected_lines = [line for i, line in enumerate(lines, start=1) if i not in target_line_numbers]
  #  print("non "+str(non_selected_lines))
#    with open('selected_lines.txt', 'w') as selected_file:
 #       selected_file.writelines(selected_lines)
    
    with open(sys.argv[3], 'w') as non_selected_file:
        non_selected_file.writelines(non_selected_lines)

# Использование функции
select_lines(sys.argv[1], sys.argv[2])
