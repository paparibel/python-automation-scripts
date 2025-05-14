import xml.etree.ElementTree as ET
import csv
import os
import re
from tkinter import Tk, filedialog

# Funkcja wyboru pliku XML przy użyciu okna dialogowego
def select_file(title, filetypes):
    Tk().withdraw()  # Ukrywa główne okno tkinter
    return filedialog.askopenfilename(title=title, filetypes=filetypes)

# Wybór pliku XML
input_file = select_file("Wybierz plik XML", [("Pliki XML", "*.xml")])
if not input_file:
    print("Nie wybrano pliku XML.")
    exit()

# Wybór lokalizacji pliku wyjściowego CSV
output_file = filedialog.asksaveasfilename(defaultextension=".csv", title="Zapisz jako", filetypes=[("Pliki CSV", "*.csv")])
if not output_file:
    print("Nie wybrano lokalizacji dla pliku CSV.")
    exit()

# Sprawdzenie istnienia pliku wejściowego
if not os.path.exists(input_file):
    print(f"Plik '{input_file}' nie istnieje.")
else:
    # Parsowanie pliku XML
    tree = ET.parse(input_file)
    root = tree.getroot()

    # Lista do przechowywania wyciągniętych danych
    data = []

    # Przetwarzanie elementów XML
    for item in root.findall('.//item'):
        alias = item.get('alias')
        text = item.get('text')
        
        # Filtruj elementy, których alias zaczyna się od 'CORE_'
        if alias and alias.startswith('CORE_'):
            # Wyodrębnij tylko numeryczny ciąg po "CORE_"
            match = re.search(r'CORE_[^\d]*(\d+)', alias)
            if match:
                core_number = match.group(1)  # Wyciągnięcie samej liczby
                data.append([core_number, text])  # Dodajemy numer i tekst do listy wynikowej

    # Sortowanie danych według numeru CORE
    data.sort(key=lambda x: int(x[0]))

    # Zapis wyników do pliku CSV
    with open(output_file, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        writer.writerow(['CORE Number', 'Text'])  # Nagłówki kolumn
        writer.writerows(data)

    print(f'Przetwarzanie zakończone. Wynik zapisano w {output_file}.')
