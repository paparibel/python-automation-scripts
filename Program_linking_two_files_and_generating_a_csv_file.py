import os
import chardet
import re
import tkinter as tk
import csv
import sys
from tkinter import filedialog
from tkinter import messagebox

def znajdz_pliki(folder):
    pliki = os.listdir(folder)
    plik_e50 = next((plik for plik in pliki if plik.lower().endswith(".e50")), None)
    plik_efh = next((plik for plik in pliki if plik.lower().endswith(".efh")), None)
    return plik_e50, plik_efh

def odczytaj_plik(sciezka):
    try:
        with open(sciezka, 'rb') as plik:
            detector = chardet.universaldetector.UniversalDetector()
            
            for line in plik:
                detector.feed(line)
                if detector.done:
                    break
            
            detector.close()
            kodowanie = detector.result['encoding']

            with open(sciezka, 'r', encoding=kodowanie) as plik:
                zawartosc = plik.readlines()
                return zawartosc, kodowanie
    except FileNotFoundError:
        print(f"Plik {sciezka} nie został znaleziony.")
        return None, None
    except Exception as e:
        print(f"Wystąpił błąd podczas odczytu pliku {sciezka}: {e}")
        return None, None

def porownaj_i_uzupelnij(plik1, plik2, plik_wyjsciowy):
    zawartosc1, _ = odczytaj_plik(plik1)
    zawartosc2, _ = odczytaj_plik(plik2)

    if zawartosc1 is not None and zawartosc2 is not None:
        wynik = []
        indeks1, indeks2 = 0, 0

        while indeks1 < len(zawartosc1) and indeks2 < len(zawartosc2):
            klucz1 = zawartosc1[indeks1].split(None, 1)[0] if zawartosc1[indeks1].strip() else ''
            klucz2 = zawartosc2[indeks2].split(None, 1)[0] if zawartosc2[indeks2].strip() else ''

            if klucz1.startswith(('H', 'E', 'F')):
                if klucz1 == klucz2:
                    wynik.append(zawartosc1[indeks1])
                    indeks1 += 1
                    indeks2 += 1
                else:
                    wynik.append(zawartosc2[indeks2])
                    indeks2 += 1
            else:
                wynik.append(zawartosc1[indeks1])
                indeks1 += 1

        # Dodaj pozostałe linie z drugiego pliku, jeśli istnieją
        wynik.extend(zawartosc2[indeks2:])

        # Usuń puste linie między wierszami
        wynik = [linia for linia in wynik if linia.strip()]

        with open(plik_wyjsciowy, 'w', encoding='utf-8') as plik_wyjsciowy:
            # Usuń wszystkie apostrofy (')
            wynik_bez_apostrofow = [linia.replace("'", "") for linia in wynik]
            plik_wyjsciowy.writelines(wynik_bez_apostrofow)
        
        #print(f"Uzupełniono brakujące wartości, usunięto puste linie i apostrofy, zapisując wynik do pliku {plik_wyjsciowy}")
        return True
    else:
        print("Error while loading files.")
        return False

def transformuj_plik_wejsciowy(plik_wejsciowy, plik_wyjsciowy):
    try:
        if not os.path.exists(plik_wejsciowy):
            raise FileNotFoundError(f"Plik {plik_wejsciowy} nie został znaleziony.")

        with open(plik_wejsciowy, 'r', encoding='utf-8') as plik:
            zawartosc = plik.readlines()

        wynik = []

        for linia in zawartosc:
            match = re.match(r'([A-Z]\d+)\s+"([^"]+)"', linia)
            if match:
                pierwsza_czesc = match.group(1)
                tekst_z_cudzyslowem = match.group(2)
                nowa_linia = f"{pierwsza_czesc} {tekst_z_cudzyslowem}\n"
                wynik.append(nowa_linia)

        with open(plik_wyjsciowy, 'w', encoding='utf-8') as plik:
            plik.writelines(wynik)

        #print(f"Plik {plik_wejsciowy} został przekształcony i zapisany jako {plik_wyjsciowy}.")
        return True

    except FileNotFoundError as e:
        print(e)
        return False
    except Exception as e:
        print(f"An error occurred while processing the file {plik_wejsciowy}: {e}")
        return False

def dodaj_brakujace_wartosci(zawartosc):
    nowa_zawartosc = []

    for i in range(len(zawartosc) - 1):
        obecny_symbol = re.search(r'([A-Z]\d+)', zawartosc[i]).group()
        nastepny_symbol = re.search(r'([A-Z]\d+)', zawartosc[i + 1]).group()

        obecny_numer = int(re.search(r'\d+', obecny_symbol).group())
        nastepny_numer = int(re.search(r'\d+', nastepny_symbol).group())

        nowa_zawartosc.append(zawartosc[i])

        for brakujacy_numer in range(obecny_numer + 1, nastepny_numer):
            brakujacy_wiersz = f"{obecny_symbol[:1]}{brakujacy_numer}\n"
            nowa_zawartosc.append(brakujacy_wiersz)

    nowa_zawartosc.append(zawartosc[-1])

    return nowa_zawartosc

def popraw_strukture(plik_wejsciowy, plik_wyjsciowy):
    try:
        if not os.path.exists(plik_wejsciowy):
            raise FileNotFoundError(f"File {plik_wejsciowy} was not found.")

        with open(plik_wejsciowy, 'r', encoding='utf-8') as plik:
            zawartosc = plik.readlines()

        # Dodaj brakujące wartości
        nowa_zawartosc = dodaj_brakujace_wartosci(zawartosc)

        with open(plik_wyjsciowy, 'w', encoding='utf-8') as plik:
            for linia in nowa_zawartosc:
                match = re.match(r'([A-Z]\d+)', linia)
                if match:
                    symbol = match.group()
                    linia = f"{symbol};{linia[len(symbol):].strip()}\n"
                plik.write(linia)

        #print(f"Plik {plik_wejsciowy} został przekształcony i zapisany jako {plik_wyjsciowy}.")
        return True

    except FileNotFoundError as e:
        print(e)
        return False
    except Exception as e:
        print(f"An error occurred while processing the file {plik_wejsciowy}: {e}")
        return False

def modyfikuj_strukture(plik_wejsciowy, plik_wyjsciowy):
    try:
        if not os.path.exists(plik_wejsciowy):
            raise FileNotFoundError(f"File {plik_wejsciowy} was not found.")

        with open(plik_wejsciowy, 'r', encoding='utf-8') as plik:
            zawartosc = plik.readlines()

        with open(plik_wyjsciowy, 'w', encoding='utf-8') as plik:
            for linia in zawartosc:
                match = re.match(r'([A-Z]\d+);?(.*)', linia)
                if match:
                    symbol = match.group(1)
                    opis = match.group(2)
                    if opis.strip():
                        if symbol.startswith(('H', 'E')):
                            plik.write(f"{symbol};#02 - {opis.strip()} - #022\n")
                        elif symbol.startswith('F'):
                            plik.write(f"{symbol};#02 - #04 - {opis.strip()} - #022\n")
                        else:
                            plik.write(linia)  # Dodaj linię bez zmian dla innych przypadków
                    else:
                        if symbol.startswith(('H', 'E')):
                            plik.write(f"{symbol};#02 - {symbol} - #022\n")
                        elif symbol.startswith('F'):
                            plik.write(f"{symbol};#02 - #04 - {symbol} - #022\n")
                        else:
                            plik.write(linia)  # Dodaj linię bez zmian, gdy brak tekstu

        print(f"Plik {plik_wejsciowy} został przekształcony i zapisany jako {plik_wyjsciowy}.")
        return True

    except FileNotFoundError as e:
        print(e)
        return False
    except Exception as e:
        print(f"An error occurred while processing the file {plik_wejsciowy}: {e}")
        return False
            
def zapisz_csv(plik_wejsciowy, plik_csv, separator=';'):
    try:
        with open(plik_wejsciowy, 'r', encoding='utf-8') as plik_wej:
            zawartosc = plik_wej.readlines()

        with open(plik_csv, 'w', encoding='utf-8-sig', newline='') as plik_csv:
            csv_writer = csv.writer(plik_csv, delimiter=separator)

            for linia in zawartosc:
                # Zastąp spację separatorem tylko w przypadku, gdy jest przed cudzysłowem (")
                linia = re.sub(r' (?=")', separator, linia)
                csv_writer.writerow([pole.strip() for pole in linia.split(separator)])

        print(f"File {plik_wejsciowy} has been recorded as {plik_csv}.")
        return True
    except FileNotFoundError as e:
        print(e)
        return False
    except Exception as e:
        print(f"An error occurred while saving the file {plik_csv}: {e}")
        return False
    
def znajdz_pliki(folder):
    pliki = os.listdir(folder)
    plik_e50 = next((plik for plik in pliki if plik.lower().endswith(".e50")), None)
    plik_efh = next((plik for plik in pliki if plik.lower().endswith(".efh")), None)
    return plik_e50, plik_efh

def uruchom_skrypt():
    # Uzyskanie ścieżki bieżącego katalogu, w którym znajduje się program
    #folder = os.path.dirname(os.path.abspath(__file__))
    sciezka_do_pliku_wykonwalnego = sys.argv[0]
    folder = os.path.dirname(sciezka_do_pliku_wykonwalnego)
    # Otwórz okno dialogowe do wyboru folderu, ustawiając bieżącą ścieżkę jako ścieżkę startową
    folder = filedialog.askdirectory(initialdir=folder, title="Specify the path to the folder where the files are located, and an e50_efh.txt and e50_efh.csv file will be created:")  
    if folder:
        nazwa_pliku1, nazwa_pliku2 = znajdz_pliki(folder)
    else:
        messagebox.showerror("Error", "No folder selected. The script cannot be continued.")

    # Use the znajdz_pliki function to find relevant files in the folder
    #nazwa_pliku1, nazwa_pliku2 = znajdz_pliki(folder)
    
    if nazwa_pliku1 is not None and nazwa_pliku2 is not None:
        nazwa_pliku_wyjsciowego_porownania = "wynik_porownania.txt"
        nazwa_pliku_wyjsciowego_transformacji = "output.txt"

        sciezba_pliku1 = os.path.join(folder, nazwa_pliku1)
        sciezba_pliku2 = os.path.join(folder, nazwa_pliku2)
        sciezba_pliku_wyjsciowego_porownania = os.path.join(folder, nazwa_pliku_wyjsciowego_porownania)
        sciezba_pliku_wyjsciowego_transformacji = os.path.join(folder, nazwa_pliku_wyjsciowego_transformacji)

        if porownaj_i_uzupelnij(sciezba_pliku1, sciezba_pliku2, sciezba_pliku_wyjsciowego_porownania):
            messagebox.showinfo("Information", f"Files {nazwa_pliku1} and {nazwa_pliku2} have been loaded.")

            if transformuj_plik_wejsciowy(sciezba_pliku_wyjsciowego_porownania, sciezba_pliku_wyjsciowego_transformacji):
                popraw_strukture(sciezba_pliku_wyjsciowego_transformacji, os.path.join(folder, "result.txt"))
                modyfikuj_strukture(os.path.join(folder, "result.txt"), os.path.join(folder, "e50_efh.txt"))
                
                # Zapisz e50_efh.txt również jako e50_efh.csv
                zapisz_csv(os.path.join(folder, "e50_efh.txt"), os.path.join(folder, "e50_efh.csv"))
                
                messagebox.showinfo("Information", "The files e50_efh.txt and e50_efh.csv have been created.")
                try:
                    # Usuń plik wynik_porownania
                    os.remove(sciezba_pliku_wyjsciowego_porownania)

                    # Usuń plik output
                    os.remove(sciezba_pliku_wyjsciowego_transformacji)

                    # Usuń plik result.txt
                    os.remove(os.path.join(folder, "result.txt"))

                except FileNotFoundError as e:
                    print(e)
                except Exception as e:
                    print(f"Wystąpił błąd podczas usuwania plików: {e}")

            else:
                messagebox.showerror("Error", "Error while processing the file result_comparison.txt.")
        else:
            messagebox.showerror("Error", f"Error while loading files {nazwa_pliku1} i {nazwa_pliku2}.")
    else:
        messagebox.showerror("Error", "The e50 and efh files were not found in the selected folder.")

def zakoncz():
    root.destroy()

# GUI
root = tk.Tk()
root.title("Application for File Processing")

# Ustawienie rozmiaru okna i ustawienie na środku ekranu
window_width = 500
window_height = 300
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

button_uruchom = tk.Button(root, text="Select files", command=uruchom_skrypt)
button_uruchom.pack()

button_zakoncz = tk.Button(root, text="Exit", command=zakoncz)
button_zakoncz.pack()

# Dodaj napis Author na dole okna
author_label = tk.Label(root, text="Author: Michał Cyba\n AŽD Praha s.r.o.", anchor="e")
author_label.pack(side="bottom", fill="x")


root.mainloop()