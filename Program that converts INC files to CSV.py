import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import os
import re

# Functions to process INC files
def remove_comments(filename, output_filename):
    encodings = ['windows-1250', 'utf-8', 'latin-1']
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()
            break
        except UnicodeDecodeError:
            continue

    # Remove block comments
    pattern_block_comments = re.compile(r'/\*.*?\*/', re.DOTALL)
    lines_without_block_comments = [pattern_block_comments.sub('', line) for line in lines]

    # Remove line comments
    pattern_line_comments = re.compile(r'//.*$')
    lines_without_comments = [pattern_line_comments.sub('', line) for line in lines_without_block_comments]

    # Remove specific lines
    lines_filtered = [line for line in lines_without_comments if not any(x in line for x in ["#ifdef", "#endif", "#els", "#ifndef"])]

    with open(output_filename, 'w', encoding='windows-1250') as file:
        file.writelines(lines_filtered)

def clean_and_align(filename, output_filename):
    with open(filename, 'r', encoding='windows-1250') as file:
        lines = file.readlines()

    cleaned_lines = [line.lstrip() for line in lines if not any(x in line for x in ["#ifdef", "#endif", "#els", "#ifndef"])]

    with open(output_filename, 'w', encoding='windows-1250') as file:
        file.writelines(cleaned_lines)

def format_output_line(line):
    parts = re.split(r'\s+', line.strip(), maxsplit=4)
    while len(parts) < 5:
        parts.append('')
    if parts[0].startswith("#p") or parts[0].startswith("#ver"):
        return " ".join(parts)
    elif parts[0].startswith("#m"):
        return f"{parts[0]} {parts[1]} {parts[2]} {parts[3]} {parts[4]}"
    elif parts[0].startswith("#b") or parts[0].startswith("#bp"):
        return f"{parts[0]} {parts[1]} {parts[2]} {parts[3]} {parts[4]}"
    else:
        return " ".join(parts)

def process_input_file(input_filename):
    temp_output_filename = "temp_output.inc"
    input_basename = os.path.splitext(os.path.basename(input_filename))[0]
    final_output_filename = f"output_{input_basename}.inc"

    remove_comments(input_filename, temp_output_filename)
    clean_and_align(temp_output_filename, final_output_filename)
    os.remove(temp_output_filename)

    return final_output_filename

def convert_to_csv_from_output(output_filenames):
    for output_filename in output_filenames:
        data = []
        encodings = ['windows-1250', 'utf-8', 'latin-1']
        for encoding in encodings:
            try:
                with open(output_filename, 'r', encoding=encoding) as file:
                    lines = file.readlines()
                break
            except UnicodeDecodeError:
                continue

        lang_code = output_filename.split('_')[-1].split('.')[0].upper()  # Extract language code from filename

        for i in range(len(lines)):
            line = lines[i].strip()
            
            # Skip lines containing #ifdef, #endif, #els, #ifndef
            if any(x in line for x in ["#ifdef", "#endif", "#els", "#ifndef"]):
                continue

            if "prvky" in output_filename:
                if line.startswith("#m") or line.startswith("#ms"):
                    parts = re.split(r'\s+', line, maxsplit=4)
                    while len(parts) < 5:
                        parts.append('')
                    mask_line = parts[:4] + [parts[4], lang_code]
                    if i + 1 < len(lines) and lines[i + 1].strip().startswith("#n"):
                        n_line = lines[i + 1].strip()
                        n_parts = re.split(r'\s+', n_line, maxsplit=1)
                        mask_line.append(n_parts[1])
                    else:
                        mask_line.append('')
                    data.append(mask_line)
                elif line.startswith("#p") or line.startswith("#ver"):
                    parts = re.split(r'\s+', line, maxsplit=4)
                    while len(parts) < 6:
                        parts.append('')
                    data.append(parts[:4] + ['', lang_code] + parts[4:])
            elif "rina" in output_filename:
                parts = re.split(r'\s+', line.strip(), maxsplit=4)
                while len(parts) < 5:
                    parts.append('')
                formatted_data = []
                if len(parts) >= 5 and (parts[0].startswith("#b") or parts[0].startswith("#bp") or parts[0].startswith("#xbk")):
                    text_split = parts[4].split(' ', 1)
                    if len(text_split) == 2:
                        formatted_data = [parts[0], parts[1], parts[2], parts[3], '', lang_code, text_split[0], text_split[1], '', '']
                    else:
                        formatted_data = [parts[0], parts[1], parts[2], parts[3], '', lang_code, parts[4], '', '', '']
                elif len(parts) >= 3 and parts[0].startswith("#ms"):
                    formatted_data = [parts[0], parts[1], parts[2], parts[3], parts[4], lang_code, '', '', '']
                elif len(parts) >= 3 and parts[0].startswith("#m"):
                    formatted_data = [parts[0], parts[1], parts[2], parts[3], '', lang_code, '', '', '', '']
                elif len(parts) >= 3 and parts[0].startswith("#p"):
                    formatted_data = [parts[0], '', '', '', '', lang_code, '', '', '', '']
                elif len(parts) >= 3 and parts[0].startswith("#ss"):
                    formatted_data = [parts[0], parts[1], parts[2], parts[3], parts[4], lang_code, '', '', '', '']
                elif len(parts) >= 3 and parts[0].startswith("#ssv"):
                    formatted_data = [parts[0], parts[1], parts[2], parts[3], parts[4], lang_code, '', '', '', '']     
                elif len(parts) >= 3 and parts[0].startswith("#ver"):
                    formatted_data = [parts[0], '', '', '', '', lang_code, '', '', '', '']       
                elif len(parts) >= 3 and parts[0].startswith("#define"):
                    formatted_data = [parts[0], parts[1], parts[2], parts[3], parts[4], lang_code, '', '', '', '']
                elif len(parts) >= 3 and parts[0].startswith("#se"):
                    formatted_data = [parts[0], parts[1], parts[2], parts[3], parts[4], lang_code, '', '', '', '']                       
                elif len(parts) == 1:
                    formatted_data = [parts[0], '', '', '', '', lang_code, '', '', '', '']
                else:
                    formatted_data = parts[:3] + ['', lang_code] + parts[3:]
                    while len(formatted_data) < 10:
                        formatted_data.append('')

                data.append(formatted_data)
                
            elif "repo" in output_filename:
                parts = re.split(r'\s+', line.strip(), maxsplit=4)
                while len(parts) < 5:
                    parts.append('')
                if len(parts) >= 5 and (parts[0].startswith("#b") or parts[0].startswith("#bp")):
                    text_split = parts[4].split(' ', 1)
                    if len(text_split) == 2:
                        formatted_data = [parts[0], parts[1], parts[2], parts[3], lang_code, text_split[0], text_split[1], '', '']
                    else:
                        formatted_data = [parts[0], parts[1], parts[2], parts[3], lang_code, parts[4], '', '', '']
                elif len(parts) >= 3 and parts[0].startswith("#m"):
                    formatted_data = [parts[0], parts[1], parts[2], '', lang_code, '', '', '', '']
                elif len(parts) == 1:
                    formatted_data = [parts[0], '', '', '', lang_code, '', '', '', '']
                else:
                    formatted_data = parts[:3] + ['', lang_code] + parts[3:]
                    while len(formatted_data) < 9:
                        formatted_data.append('')
                data.append(formatted_data)

            elif "repr" in output_filename:
                parts = re.split(r'\s+', line.strip(), maxsplit=4)
                while len(parts) < 5:
                    parts.append('')
                if len(parts) >= 5 and (parts[0].startswith("#bp") or parts[0].startswith("#b")):
                    text = " ".join(parts[3:]).strip()
                    if text:
                        formatted_data = [parts[0], parts[1], parts[2], lang_code, *text.split(maxsplit=1), '', '', '']
                    else:
                        formatted_data = [parts[0], parts[1], parts[2], lang_code, '', '', '', '', '']
                elif len(parts) >= 3 and parts[0].startswith("#m"):
                    formatted_data = [parts[0], parts[1], parts[2], lang_code, '', '', '', '', '']
                elif len(parts) == 1:
                    formatted_data = [parts[0], '', '', '', lang_code, '', '', '', '']
                else:
                    formatted_data = parts[:3] + [lang_code, *parts[3:]] + [''] * (9 - len(parts) - 1)
                data.append(formatted_data)
            else:
                parts = re.split(r'\s+', line.strip(), maxsplit=4)
                while len(parts) < 5:
                    parts.append('')
                formatted_data = parts + [''] * (9 - len(parts))
                data.append(formatted_data)

        if "rina" in output_filename:
            with open("log_rina.txt", "a") as log_file:  # Otwieramy plik log_rina.txt w trybie dołączania
                for row in data:
                    log_file.write(f"Przetwarzam wiersz: {row}\n")  # Debugowanie
                    if len(row) > 3:
                        match = re.search(r'[a-z_]{4,}', row[3])  # Zmienione wyrażenie regularne, aby uwzględniało znaki specjalne
                        if match:
                            log_file.write(f"Znaleziono długi ciąg małych liter lub znaków specjalnych w kolumnie 3: {match.group()}\n")  # Debugowanie
                            if row[6] == '':
                                log_file.write(f"Przenoszę wartość '{row[3]}' do kolumny 7\n")  # Debugowanie
                                row[6] = row[3]
                                row[3] = ''
                            elif row[7] == '':
                                log_file.write(f"Przenoszę wartość '{row[6]}' do kolumny 8, a wartość '{row[3]}' do kolumny 7\n")  # Debugowanie
                                row[7] = row[6]
                                row[6] = row[3]
                                row[3] = ''
                            else:
                                log_file.write(f"Kolumna 7 i 8 są już zapełnione, łącze wartości.\n")  # Debugowanie
                                row[6] = f"{row[3]} {row[6]} {row[7]}".strip()
                                row[7] = ''
                                row[3] = ''
                        else:
                            log_file.write(f"Brak długiego ciągu małych liter lub znaków specjalnych w kolumnie 3: {row[3]}\n")  # Debugowanie
                     
        elif "repo" in output_filename:
            with open("log_repo.txt", "a") as log_file:  # Otwieramy plik log_repo.txt w trybie dołączania
                for row in data:
                    log_file.write(f"Przetwarzam wiersz: {row}\n")  # Debugowanie
                    if len(row) > 3:
                        # Sprawdzamy, czy w kolumnie 3 są co najmniej 3 małe litery i mniej niż 2 duże litery
                        match = re.search(r'(?=.*[a-z_]{3,})(?!.*[A-Z]{2,})', row[3])
                        if match:
                            log_file.write(f"Znaleziono długi ciąg małych liter lub znaków specjalnych w kolumnie 3: {row[3]}\n")  # Debugowanie
                            if row[5] == '':
                                log_file.write(f"Przenoszę wartość '{row[3]}' do kolumny 6\n")  # Debugowanie
                                row[5] = row[3]
                                row[3] = ''
                            elif row[6] == '':
                                log_file.write(f"Przenoszę wartość '{row[5]}' do kolumny 7, a wartość '{row[3]}' do kolumny 6\n")  # Debugowanie
                                row[6] = row[5]
                                row[5] = row[3]
                                row[3] = ''
                            elif row[7] == '':
                                log_file.write(f"Przenoszę wartość '{row[6]}' do kolumny 8, a wartość '{row[5]}' do kolumny 7, a wartość '{row[3]}' do kolumny 6\n")  # Debugowanie
                                row[7] = row[6]
                                row[6] = row[5]
                                row[5] = row[3]
                                row[3] = ''
                            else:
                                log_file.write(f"Kolumny 6, 7 i 8 są już zapełnione, przenoszę wartości w dół.\n")  # Debugowanie
                                row[8] = row[7]
                                row[7] = row[6]
                                row[6] = row[5]
                                row[5] = row[3]
                                row[3] = ''
                        else:
                            log_file.write(f"Brak długiego ciągu małych liter lub za dużo dużych liter w kolumnie 3: {row[3]}\n")  # Debugowanie

        if "repo" in output_filename:
            with open("log_repo.txt", "a") as log_file:  # Otwieramy plik log_repo.txt w trybie dołączania
                for row in data:
                    if len(row) > 6 and re.search(r'\)$', row[6]) and "(" not in row[6]:
                        log_file.write(f"Łączenie kolumn 6 i 7: {row[5]} + {row[6]}\n")  # Debugowanie
                        row[5] = f"{row[5]} {row[6]}".strip()
                        row[6] = ''

                    if len(row) > 2:
                        match = re.search(r'[A-Z_]{3,}', row[2])  # Zmienione wyrażenie regularne, aby uwzględniało znaki specjalne
                        if match:
                            row[3]=row[2]
                            row[2]=''

        if "rina" in output_filename:               
            with open("log_repo.txt", "a") as log_file:  # Otwieramy plik log_repo.txt w trybie dołączania
                for row in data:
                    if len(row) > 2:
                        match = re.search(r'[A-Z_]{3,}', row[2])  # Zmienione wyrażenie regularne, aby uwzględniało znaki specjalne
                        if match:
                            log_file.write(f"Znaleziono długi ciąg małych liter lub znaków specjalnych w kolumnie 3: {row[2]}\n")  # Debugowanie
                            row[3]=row[2]
                            row[2]=''
                        else:
                            log_file.write(f"Brak długiego ciągu małych liter lub za dużo dużych liter w kolumnie 3: {row[2]}\n")  # Debugowanie 

        if "repr" in output_filename:
            for row in data:
                # Sprawdzanie, czy przynajmniej jedna komórka w wierszu zawiera tekst
                match = any(cell.strip() for cell in row)
                
                if match:
                      row[7]=row[5]
                      row[6]=row[4]
                      row[5]=row[3]
                      row[3]=''
                      row[4]=''

        if "repo" in output_filename:
            for row in data:
                # Sprawdzanie, czy przynajmniej jedna komórka w wierszu zawiera tekst
                match = any(cell.strip() for cell in row)
                
                if match:
                      row[7]=row[6]
                      row[6]=''
                      row[6]=row[5]
                      row[5]=''
                      row[5]=row[4]
                      row[4]=''


        
        df = pd.DataFrame(data)
        output_csv_filename = f"{os.path.splitext(output_filename)[0]}.csv"
        df.to_csv(output_csv_filename, sep=';', index=False, header=False, encoding='windows-1250')
        messagebox.showinfo("Information", f"The CSV file was saved as: {output_csv_filename}")

        replace_underscores_in_csv(output_csv_filename, lang_code)

        # Remove extra semicolons
        if "rina" in output_filename:
            remove_extra_semicolons(output_csv_filename, 1)
        #elif "repo" in output_filename:
            #remove_extra_semicolons(output_csv_filename, 1)
        #elif "repr" in output_filename:
            #remove_extra_semicolons(output_csv_filename, 2)
            
         # Zamiana wszystkich wartości "EN" na "US" w odpowiednich plikach
        if any(x in output_filename for x in ["prvky", "repo", "rina", "repr"]):
            replace_en_with_us_in_csv(output_csv_filename)

    # Usunięcie plików logów na końcu funkcji
    log_files = ["log_repo.txt", "log_rina.txt"]
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
                print(f"Plik {log_file} został usunięty.")
            except Exception as e:
                print(f"Nie udało się usunąć pliku {log_file}. Błąd: {e}")        

def replace_en_with_us_in_csv(csv_filename):
    df = pd.read_csv(csv_filename, sep=';', header=None, encoding='windows-1250')
    df = df.applymap(lambda x: 'US' if x == 'EN' else x)
    df.to_csv(csv_filename, sep=';', index=False, header=False, encoding='windows-1250')    


def remove_extra_semicolons(csv_filename, count):
    with open(csv_filename, 'r', encoding='windows-1250') as file:
        lines = file.readlines()

    with open(csv_filename, 'w', encoding='windows-1250') as file:
        for line in lines:
            if line.endswith(';' * count + '\n'):
                file.write(line[:-count-1] + '\n')
            else:
                file.write(line)

def replace_underscores_in_csv(output_csv_filename, lang_code):
    df = pd.read_csv(output_csv_filename, sep=';', header=None, encoding='windows-1250')
    # Find the index of the column with the language code
    lang_col_index = df.columns[df.iloc[0] == lang_code].tolist()
    if lang_col_index:
        lang_col_index = lang_col_index[0] + 1  # We want to start replacing from the next column
        # Replace underscores with spaces and remove excess spaces only in columns after the language code column
        df.iloc[:, lang_col_index:] = df.iloc[:, lang_col_index:].applymap(lambda x: " ".join(x.replace('_', ' ').split()) if isinstance(x, str) else x)
    df.to_csv(output_csv_filename, sep=';', index=False, header=False, encoding='windows-1250')
    #messagebox.showinfo("Information", f"Znaki podkreślenia zostały zastąpione spacjami, a nadmiarowe spacje usunięte w pliku: {output_csv_filename}")

def choose_input_files():
    input_filenames = filedialog.askopenfilenames(title="Select input files", filetypes=[("Files INC", "*.inc")])

    if not input_filenames:
        messagebox.showinfo("Information", "Input files not selected.")
        return

    output_filenames = []
    for input_filename in input_filenames:
        output_filename = process_input_file(input_filename)
        output_filenames.append(output_filename)

    # Tworzenie outputów
    for output_filename in output_filenames:
        with open(output_filename, 'r', encoding='windows-1250') as file:
            lines = file.readlines()

        with open(output_filename, 'w', encoding='windows-1250') as file:
            for line in lines:
                formatted_line = format_output_line(line)
                file.write(formatted_line + '\n')

    convert_to_csv_from_output(output_filenames)
    
import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd
import csv

def count_p_groups(file_path, log_file):
    log_file.write(f"\nProcessing file: {file_path}\n")

    def process_file(df):
        p_group_count = 0
        group_number = 1
        inside_p_group = False
        start_line = None
        last_line_num = 0
        group_lines = []

        groups = []

        log_file.write(f"\nGroups in {file_path}:\n")

        for index, row in df.iterrows():
            last_line_num = index
            if pd.notna(row.iloc[0]) and row.iloc[0].startswith('#p'):
                if inside_p_group:
                    log_file.write(f"Group {group_number} ends at: {last_line_num - 1}\n")
                    log_file.write("\n".join(group_lines) + "\n")
                    groups.append(group_lines)
                    p_group_count += 1
                    group_number += 1

                start_line = index
                log_file.write(f"Group {group_number} starts at: {start_line}\n")
                group_lines = [";".join(map(lambda x: str(x) if pd.notna(x) else '', row))]
                inside_p_group = True
            elif inside_p_group:
                group_lines.append(";".join(map(lambda x: str(x) if pd.notna(x) else '', row)))
        
        if inside_p_group:
            log_file.write(f"Group {group_number} ends at: {last_line_num}\n")
            log_file.write("\n".join(group_lines) + "\n")
            groups.append(group_lines)
            p_group_count += 1

        return p_group_count, groups

    encodings = ['windows-1250', 'utf-8', 'latin-1']
    for encoding in encodings:
        try:
            df = pd.read_csv(file_path, encoding=encoding, sep=';')
            p_group_count, groups = process_file(df)
            return p_group_count, groups
        except UnicodeDecodeError:
            pass

    log_file.write(f"Failed to decode {file_path} with all encodings\n")
    return 0, []

def compare_groups(base_group, other_group, log_file):
    base_group_rows = [row.split(';') for row in base_group]
    other_group_rows = [row.split(';') for row in other_group]

    log_file.write("Comparing groups:\n")
    log_file.write("Base group:\n")
    log_file.write("\n".join(base_group) + "\n")
    log_file.write("Other group:\n")
    log_file.write("\n".join(other_group) + "\n")

    base_m_values = sorted([tuple(row[:5]) for row in base_group_rows if row[0] == '#m'])
    other_m_values = sorted([tuple(row[:5]) for row in other_group_rows if row[0] == '#m'])

    if base_m_values == other_m_values:
        log_file.write("Groups are the same\n")
        return True
    else:
        log_file.write("Groups are not the same: #m values differ\n")
        return False

def merge_groups(base_group, other_group, additional_columns_start):
    base_group_rows = [row.split(';') for row in base_group]
    other_group_rows = [row.split(';') for row in other_group]
    merged_group = base_group_rows.copy()

    for other_row in other_group_rows:
        matched = False
        if other_row[0] == '#m' or other_row[0] == '#bp' or other_row[0] == '#b':
            for base_row in base_group_rows:
                if base_row[:5] == other_row[:5]:
                    while len(base_row) < additional_columns_start:
                        base_row.append('')
                    base_row[additional_columns_start:additional_columns_start+3] = other_row[5:8]
                    matched = True
                    break
            if not matched:
                new_row = other_row[:5] + [''] * (additional_columns_start - 5) + other_row[5:8]
                merged_group.append(new_row)
                base_group_rows.append(new_row)
    return [";".join(row) for row in merged_group]

def add_group_without_pair(base_groups, other_group, additional_columns_start):
    other_group_rows = [row.split(';') for row in other_group]
    new_group = []
    for row in other_group_rows:
        while len(row) < additional_columns_start:
            row.append('')
        new_row = row[:5] + [''] * (additional_columns_start - 5) + row[5:8]
        new_group.append(";".join(new_row))
    base_groups.append(new_group)


def handle_repo_files(file_paths):
    print("Handling repo files:")
    with open("log_group.txt", "w", encoding='utf-8') as log_file, open("log_compare.txt", "w", encoding='utf-8') as compare_log_file:
        base_file = None
        for file in file_paths:
            if "en" in os.path.basename(file).lower():
                base_file = file
                break
        if not base_file:
            for file in file_paths:
                if "cz" in os.path.basename(file).lower():
                    base_file = file
                    break
        if not base_file:
            base_file = file_paths[0]

        print(f"Base file: {base_file}")

        base_file_p_group_count, base_groups = count_p_groups(base_file, log_file)
        log_file.write(f"\nBase file: {base_file}, #p groups count: {base_file_p_group_count}\n")
        print(f"Base file: {base_file}, #p groups count: {base_file_p_group_count}")

        unmatched_groups_all = []
        additional_columns_start = 8  # Initialize here

        for file in file_paths:
            if file != base_file:
                p_group_count, groups = count_p_groups(file, log_file)
                log_file.write(f"\nFile: {file}, #p groups count: {p_group_count}\n")
                print(f"File: {file}, #p groups count: {p_group_count}")

                unmatched_groups = []
                matched_groups = []

                for other_group in groups:
                    matched = False
                    for i, base_group in enumerate(base_groups):
                        if compare_groups(base_group, other_group, compare_log_file):
                            matched = True
                            merged_group = merge_groups(base_group, other_group, additional_columns_start)
                            base_groups[i] = merged_group
                            matched_groups.append(merged_group)
                            break
                    if not matched:
                        compare_log_file.write(f"Group from {file} does not match any group in base file\n")
                        unmatched_groups.append(other_group)

                if unmatched_groups:
                    for group in unmatched_groups:
                        add_group_without_pair(base_groups, group, additional_columns_start)
                    additional_columns_start += 3

        log_file.close()
        compare_log_file.close()

        # Save the updated base groups and unmatched groups to all_repo.csv
        encodings = ['windows-1250', 'utf-8', 'latin-1']
        for encoding in encodings:
            try:
                with open('all_repo.csv', 'w', newline='', encoding=encoding) as all_repo_csvfile:
                    writer = csv.writer(all_repo_csvfile, delimiter=';')
                    for group in base_groups:
                        for row in group:
                            writer.writerow(row.split(';'))
                break  # Break if saving is successful
            except UnicodeEncodeError:
                continue  # Try the next encoding if the current one fails

    # Example usage:
    encodings = ['windows-1250', 'utf-8', 'latin-1']
    filename = 'all_repo.csv'
    align_rows_to_longest(filename, encodings)

    encodings = ['windows-1250', 'utf-8', 'latin-1']
    filename = 'all_repo.csv'
    uzupelnienie_kolumn(filename, encodings)

    # Usunięcie plików logów na końcu funkcji
    log_files = ["log_compare.txt", "log_group.txt"]
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
                print(f"Plik {log_file} został usunięty.")
            except Exception as e:
                print(f"Nie udało się usunąć pliku {log_file}. Błąd: {e}")   

    open_file('all_repo.csv')

def handle_repr_files(file_paths):
    print("Handling repr files:")
    with open("log_group.txt", "w", encoding='utf-8') as log_file, open("log_compare.txt", "w", encoding='utf-8') as compare_log_file:
        base_file = None
        for file in file_paths:
            if "en" in os.path.basename(file).lower():
                base_file = file
                break
        if not base_file:
            for file in file_paths:
                if "cz" in os.path.basename(file).lower():
                    base_file = file
                    break
        if not base_file:
            base_file = file_paths[0]

        print(f"Base file: {base_file}")

        base_file_p_group_count, base_groups = count_p_groups(base_file, log_file)
        log_file.write(f"\nBase file: {base_file}, #p groups count: {base_file_p_group_count}\n")
        print(f"Base file: {base_file}, #p groups count: {base_file_p_group_count}")

        unmatched_groups_all = []
        additional_columns_start = 8  # Initialize here

        for file in file_paths:
            if file != base_file:
                p_group_count, groups = count_p_groups(file, log_file)
                log_file.write(f"\nFile: {file}, #p groups count: {p_group_count}\n")
                print(f"File: {file}, #p groups count: {p_group_count}")

                unmatched_groups = []
                matched_groups = []

                for other_group in groups:
                    matched = False
                    for i, base_group in enumerate(base_groups):
                        if compare_groups(base_group, other_group, compare_log_file):
                            matched = True
                            merged_group = merge_groups(base_group, other_group, additional_columns_start)
                            base_groups[i] = merged_group
                            matched_groups.append(merged_group)
                            break
                    if not matched:
                        compare_log_file.write(f"Group from {file} does not match any group in base file\n")
                        unmatched_groups.append(other_group)

                if unmatched_groups:
                    for group in unmatched_groups:
                        add_group_without_pair(base_groups, group, additional_columns_start)
                    additional_columns_start += 3

        log_file.close()
        compare_log_file.close()

        # Save the updated base groups and unmatched groups to all_repr.csv
        encodings = ['windows-1250', 'utf-8', 'latin-1']
        for encoding in encodings:
            try:
                with open('all_repr.csv', 'w', newline='', encoding=encoding) as all_repo_csvfile:
                    writer = csv.writer(all_repo_csvfile, delimiter=';')
                    for group in base_groups:
                        for row in group:
                            writer.writerow(row.split(';'))
                break  # Break if saving is successful
            except UnicodeEncodeError:
                continue  # Try the next encoding if the current one fails

    # Example usage:
    encodings = ['windows-1250', 'utf-8', 'latin-1']
    filename = 'all_repr.csv'
    align_rows_to_longest(filename, encodings)

    encodings = ['windows-1250', 'utf-8', 'latin-1']
    filename = 'all_repr.csv'
    uzupelnienie_kolumn(filename, encodings)

    # Usunięcie plików logów na końcu funkcji
    log_files = ["log_compare.txt", "log_group.txt"]
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
                print(f"Plik {log_file} został usunięty.")
            except Exception as e:
                print(f"Nie udało się usunąć pliku {log_file}. Błąd: {e}")   

    open_file('all_repr.csv')

def handle_prvky_files(file_paths):
    print("Handling repr files:")
    with open("log_group.txt", "w", encoding='utf-8') as log_file, open("log_compare.txt", "w", encoding='utf-8') as compare_log_file:
        base_file = None
        for file in file_paths:
            if "en" in os.path.basename(file).lower():
                base_file = file
                break
        if not base_file:
            for file in file_paths:
                if "cz" in os.path.basename(file).lower():
                    base_file = file
                    break
        if not base_file:
            base_file = file_paths[0]

        print(f"Base file: {base_file}")

        base_file_p_group_count, base_groups = count_p_groups(base_file, log_file)
        log_file.write(f"\nBase file: {base_file}, #p groups count: {base_file_p_group_count}\n")
        print(f"Base file: {base_file}, #p groups count: {base_file_p_group_count}")

        unmatched_groups_all = []
        additional_columns_start = 8  # Initialize here

        for file in file_paths:
            if file != base_file:
                p_group_count, groups = count_p_groups(file, log_file)
                log_file.write(f"\nFile: {file}, #p groups count: {p_group_count}\n")
                print(f"File: {file}, #p groups count: {p_group_count}")

                unmatched_groups = []
                matched_groups = []

                for other_group in groups:
                    matched = False
                    for i, base_group in enumerate(base_groups):
                        if compare_groups(base_group, other_group, compare_log_file):
                            matched = True
                            merged_group = merge_groups(base_group, other_group, additional_columns_start)
                            base_groups[i] = merged_group
                            matched_groups.append(merged_group)
                            break
                    if not matched:
                        compare_log_file.write(f"Group from {file} does not match any group in base file\n")
                        unmatched_groups.append(other_group)

                if unmatched_groups:
                    for group in unmatched_groups:
                        add_group_without_pair(base_groups, group, additional_columns_start)
                    additional_columns_start += 3

        log_file.close()
        compare_log_file.close()

        # Save the updated base groups and unmatched groups to all_repr.csv
        encodings = ['windows-1250', 'utf-8', 'latin-1']
        for encoding in encodings:
            try:
                with open('all_prvky.csv', 'w', newline='', encoding=encoding) as all_repo_csvfile:
                    writer = csv.writer(all_repo_csvfile, delimiter=';')
                    for group in base_groups:
                        for row in group:
                            writer.writerow(row.split(';'))
                break  # Break if saving is successful
            except UnicodeEncodeError:
                continue  # Try the next encoding if the current one fails

    # Example usage:
    encodings = ['windows-1250', 'utf-8', 'latin-1']
    filename = 'all_prvky.csv'
    align_rows_to_longest(filename, encodings)

    encodings = ['windows-1250', 'utf-8', 'latin-1']
    filename = 'all_prvky.csv'
    uzupelnienie_kolumn(filename, encodings)

    # Usunięcie plików logów na końcu funkcji
    log_files = ["log_compare.txt", "log_group.txt"]
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
                print(f"Plik {log_file} został usunięty.")
            except Exception as e:
                print(f"Nie udało się usunąć pliku {log_file}. Błąd: {e}")   

    open_file('all_prvky.csv')

def handle_rina_files(file_paths):
    print("Handling repr files:")
    with open("log_group.txt", "w", encoding='utf-8') as log_file, open("log_compare.txt", "w", encoding='utf-8') as compare_log_file:
        base_file = None
        for file in file_paths:
            if "en" in os.path.basename(file).lower():
                base_file = file
                break
        if not base_file:
            for file in file_paths:
                if "cz" in os.path.basename(file).lower():
                    base_file = file
                    break
        if not base_file:
            base_file = file_paths[0]

        print(f"Base file: {base_file}")

        base_file_p_group_count, base_groups = count_p_groups(base_file, log_file)
        log_file.write(f"\nBase file: {base_file}, #p groups count: {base_file_p_group_count}\n")
        print(f"Base file: {base_file}, #p groups count: {base_file_p_group_count}")

        unmatched_groups_all = []
        additional_columns_start = 8  # Initialize here

        for file in file_paths:
            if file != base_file:
                p_group_count, groups = count_p_groups(file, log_file)
                log_file.write(f"\nFile: {file}, #p groups count: {p_group_count}\n")
                print(f"File: {file}, #p groups count: {p_group_count}")

                unmatched_groups = []
                matched_groups = []

                for other_group in groups:
                    matched = False
                    for i, base_group in enumerate(base_groups):
                        if compare_groups(base_group, other_group, compare_log_file):
                            matched = True
                            merged_group = merge_groups(base_group, other_group, additional_columns_start)
                            base_groups[i] = merged_group
                            matched_groups.append(merged_group)
                            break
                    if not matched:
                        compare_log_file.write(f"Group from {file} does not match any group in base file\n")
                        unmatched_groups.append(other_group)

                if unmatched_groups:
                    for group in unmatched_groups:
                        add_group_without_pair(base_groups, group, additional_columns_start)
                    additional_columns_start += 3

        log_file.close()
        compare_log_file.close()

        # Save the updated base groups and unmatched groups to all_repr.csv
        encodings = ['windows-1250', 'utf-8', 'latin-1']
        for encoding in encodings:
            try:
                with open('all_rina.csv', 'w', newline='', encoding=encoding) as all_repo_csvfile:
                    writer = csv.writer(all_repo_csvfile, delimiter=';')
                    for group in base_groups:
                        for row in group:
                            writer.writerow(row.split(';'))
                break  # Break if saving is successful
            except UnicodeEncodeError:
                continue  # Try the next encoding if the current one fails

    # Example usage:
    encodings = ['windows-1250', 'utf-8', 'latin-1']
    filename = 'all_rina.csv'
    align_rows_to_longest(filename, encodings)

    encodings = ['windows-1250', 'utf-8', 'latin-1']
    filename = 'all_rina.csv'
    uzupelnienie_kolumn(filename, encodings)

    # Usunięcie plików logów na końcu funkcji
    log_files = ["log_compare.txt", "log_group.txt"]
    for log_file in log_files:
        if os.path.exists(log_file):
            try:
                os.remove(log_file)
                print(f"Plik {log_file} został usunięty.")
            except Exception as e:
                print(f"Nie udało się usunąć pliku {log_file}. Błąd: {e}")   

    open_file('all_rina.csv')



import csv

def find_longest_shortest_row(filename, encodings):
    longest_row = None
    shortest_row = None
    max_length = 0
    min_length = float('inf')
    longest_row_num = None
    shortest_row_num = None
    longest_row_count = 0
    shortest_row_count = 0
    encoding_used = None
    total_rows = 0

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                csv_reader = csv.reader(file, delimiter=';')
                line_number = 0
                for row in csv_reader:
                    total_rows += 1
                    row_length = len(row)
                    if row_length > max_length:
                        max_length = row_length
                        longest_row = row
                        longest_row_num = line_number + 1
                        longest_row_count = 1
                    elif row_length == max_length:
                        longest_row_count += 1

                    if row_length < min_length:
                        min_length = row_length
                        shortest_row = row
                        shortest_row_num = line_number + 1
                        shortest_row_count = 1
                    elif row_length == min_length:
                        shortest_row_count += 1

                    line_number += 1
                encoding_used = encoding
                break
        except UnicodeDecodeError:
            continue

    if longest_row is not None:
        print(f"Longest row (length {max_length}, {len(longest_row)} columns) found in line {longest_row_num} using {encoding_used} encoding:")
        print(longest_row)
        print(f"Number of rows with longest length: {longest_row_count}")
    else:
        print("No rows found in the file.")

    if shortest_row is not None:
        print(f"Shortest row (length {min_length}, {len(shortest_row)} columns) found in line {shortest_row_num} using {encoding_used} encoding:")
        print(shortest_row)
        print(f"Number of rows with shortest length: {shortest_row_count}")
    else:
        print("No rows found in the file.")

    if total_rows > 0:
        print(f"Total rows in the file '{filename}' using {encoding_used} encoding: {total_rows}")
    else:
        print(f"No rows found in the file '{filename}'.")

    return longest_row, max_length

def align_rows_to_longest(filename, encodings):
    longest_row, max_length = find_longest_shortest_row(filename, encodings)

    if longest_row is not None:
        encoding_used = None
        aligned_rows = []
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as file:
                    csv_reader = csv.reader(file, delimiter=';')
                    for row in csv_reader:
                        aligned_row = row + [''] * (max_length - len(row))
                        aligned_rows.append(aligned_row)
                encoding_used = encoding
                break
            except UnicodeDecodeError:
                continue
        
        if encoding_used:
            try:
                with open(filename, 'w', newline='', encoding=encoding_used) as file:
                    csv_writer = csv.writer(file, delimiter=';')
                    csv_writer.writerows(aligned_rows)
                
                print(f"Successfully aligned rows to longest length ({max_length} columns). Saved aligned file as '{filename}'.")
            except UnicodeDecodeError:
                print(f"Error: Unable to encode file '{filename}' with encoding '{encoding_used}'.")
        else:
            print(f"Error: Unable to decode file '{filename}' with specified encodings.")
    else:
        print("No rows found in the file.")

import csv
from collections import Counter

def find_most_common_value(rows, col_idx):
    """
    Finds the most common non-empty value in the specified column.
    """
    values = [row[col_idx] for row in rows if row[col_idx].strip() != '']
    if values:
        most_common_value = Counter(values).most_common(1)[0][0]
        return most_common_value
    return None

def uzupelnienie_kolumn(filename, encodings):
    # Read the file and get the rows
    encoding_used = None
    rows = []
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                csv_reader = csv.reader(file, delimiter=';')
                rows = [row for row in csv_reader]
            encoding_used = encoding
            break
        except UnicodeDecodeError:
            continue

    if not encoding_used:
        print(f"Error: Unable to decode file '{filename}' with specified encodings.")
        return

    # Determine the maximum number of columns
    max_cols = max(len(row) for row in rows)

    # Find the most common values for the specified columns (starting from 6th, 9th, 12th, etc.)
    columns_to_fill = list(range(5, max_cols, 3))  # Adjust for 0-based indexing
    most_common_values = {col_idx: find_most_common_value(rows, col_idx) for col_idx in columns_to_fill}

    # Fill the empty cells in the specified columns with the most common values
    for row in rows:
        for col_idx in columns_to_fill:
            if col_idx < len(row) and row[col_idx].strip() == '':
                row[col_idx] = most_common_values[col_idx]

    # Write the updated rows back to the file
    try:
        with open(filename, 'w', newline='', encoding=encoding_used) as file:
            csv_writer = csv.writer(file, delimiter=';')
            csv_writer.writerows(rows)
        print(f"Successfully filled empty cells in columns {columns_to_fill} with the most common values. Updated file '{filename}'.")
    except UnicodeDecodeError:
        print(f"Error: Unable to encode file '{filename}' with encoding '{encoding_used}'.")






def merge_csv_files():
    root = tk.Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames(title="Select CSV files", filetypes=[("CSV Files", "*.csv")])
    
    if not file_paths:
        messagebox.showinfo("No files available", "No files have been selected.")
        return
    
    file_names = [os.path.basename(file).split('.')[0] for file in file_paths]

    if all("repo" in name.lower() for name in file_names):
        handle_repo_files(file_paths)
    elif all("repr" in name.lower() for name in file_names):
        handle_repr_files(file_paths)
    elif all("prvky" in name.lower() for name in file_names):
        handle_prvky_files(file_paths)
    elif all("rina" in name.lower() for name in file_names):
        handle_rina_files(file_paths)
    else:
        #print("Wybrano pliki z różnych kategorii. Proszę wybrać pliki z jednej kategorii.")
        messagebox.showinfo("Error", "Files from different categories have been selected. Please select files from one category.")


# Wywołanie funkcji (odkomentuj, aby przetestować)
# merge_csv_files()

def open_file(file_path):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # macOS, Linux
            subprocess.call(('open', file_path))
    except Exception as e:
        print(f"Failed to open file {file_path}: {e}")






#Główne OKNO PROGRAMU 
root = tk.Tk()
root.title("Program that converts INC files to CSV")
    
# Ustawienie rozmiaru okna
root.geometry("600x600")
    
# Centralizacja okna
window_width = 450
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
    
position_top = int(screen_height/2 - window_height/2)
position_right = int(screen_width/2 - window_width/2)
    
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
# Dodaj napis Author na dole okna
author_label = tk.Label(root, text="Author: Michał Cyba\n AŽD Praha s.r.o.", anchor="e")
author_label.pack(side="bottom", fill="x")

# Function to display program information
def show_info():
    info_text = """
    Program processing INC files
    
    - Select 'Select INC files' button to process INC files to a single .csv
    - Select 'Convert to CSV' button to convert selected files to all.csv format
    """
    messagebox.showinfo("Information", info_text)



def exit_program():
    root.destroy()


# Creating the button to choose input files
choose_files_button = tk.Button(root, text="Select INC files", command=choose_input_files)
choose_files_button.pack(pady=10)

# Creating the button to convert files to CSV format
convert_to_csv_button = tk.Button(root, text="Convert to CSV", command=merge_csv_files)
convert_to_csv_button.pack(pady=10)

# Creating the button to display program information
info_button = tk.Button(root, text="Programme information", command=show_info)
info_button.pack(pady=5)



# Creating the button to exit the program
exit_button = tk.Button(root, text="Finish", command=exit_program)
exit_button.pack(pady=5)

# Running the main loop
root.mainloop()
