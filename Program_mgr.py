import tkinter as tk
from tkinter import ttk
import csv
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
import random

def main_program():
    global simulated_faults, confirmed_faults, repair_stats, opened_windows, repair_options_dict, LOG_FILE, custom_repair_options

    simulated_faults = set()
    confirmed_faults = defaultdict(int)
    repair_stats = defaultdict(lambda: defaultdict(int))
    opened_windows = {}
    custom_repair_options = defaultdict(list)

    repair_options_dict = {
        "Opóźnione zamykanie rogatek": ["Uszkodzenie mechanizmu napędowego rogatek", "Niewłaściwe ustawienie czujników", "Usterka układu sterowania"],
        "Awaria mechanizmu rogatek": ["Zwarcie w obwodach elektrycznych", "Uszkodzenie silnika napędowego", "Usterka przekaźników"],
        "Awaria sygnalizacji świetlnej": ["Przepalenie żarówek", "Uszkodzenie przewodów zasilających", "Usterka modułu sterującego"],
        "Awaria sygnalizacji dźwiękowej": ["Uszkodzenie głośnika", "Zwarcie w obwodach akustycznych", "Usterka modułu dźwiękowego"]
    }

    repair_options = {
    "Uszkodzenie mechanizmu napędowego rogatek": [
        "Wymiana mechanizmu napędowego. Sprawdzenie działania mechanizmu, wymiana uszkodzonych części, testy funkcjonalności po wymianie.",
        "Regulacja mechanizmu napędowego. Diagnoza problemu, dostosowanie ustawień mechanizmu, testowanie poprawności działania.",
        "Smarowanie i konserwacja mechanizmu. Czyszczenie mechanizmu, smarowanie ruchomych części, testy działania po konserwacji."
    ],
    "Niewłaściwe ustawienie czujników": [
        "Kalibracja czujników. Sprawdzenie obecnych ustawień, kalibracja do odpowiednich wartości, testy poprawności działania.",
        "Wymiana uszkodzonych czujników. Diagnoza uszkodzeń, demontaż uszkodzonych czujników, instalacja nowych czujników i ich kalibracja.",
        "Czyszczenie czujników. Usunięcie zanieczyszczeń, sprawdzenie poprawności działania po czyszczeniu."
    ],
    "Usterka układu sterowania": [
        "Resetowanie układu sterowania. Diagnoza awarii, restart układu, testowanie poprawności działania.",
        "Aktualizacja oprogramowania sterującego. Sprawdzenie wersji oprogramowania, aktualizacja do najnowszej wersji, testy po aktualizacji.",
        "Wymiana modułu sterującego. Diagnoza problemu, wymiana modułu na nowy, kalibracja i testy funkcjonalności."
    ],
    "Zwarcie w obwodach elektrycznych": [
        "Lokalizacja i naprawa zwarcia. Diagnoza miejsca zwarcia, naprawa uszkodzonego obwodu, testowanie poprawności działania.",
        "Wymiana uszkodzonych przewodów. Identyfikacja uszkodzonych przewodów, wymiana przewodów na nowe, testy po wymianie.",
        "Instalacja zabezpieczeń przeciążeniowych. Diagnoza przyczyn zwarcia, instalacja odpowiednich zabezpieczeń, testy po instalacji."
    ],
    "Uszkodzenie silnika napędowego": [
        "Wymiana silnika napędowego. Diagnoza uszkodzenia, demontaż uszkodzonego silnika, instalacja nowego silnika i testy.",
        "Naprawa wewnętrznych części silnika. Identyfikacja uszkodzeń wewnętrznych, naprawa lub wymiana uszkodzonych części, testy po naprawie.",
        "Kalibracja silnika. Sprawdzenie ustawień silnika, dostosowanie parametrów pracy, testy poprawności działania."
    ],
    "Usterka przekaźników": [
        "Wymiana uszkodzonych przekaźników. Diagnoza uszkodzeń, demontaż uszkodzonych przekaźników, instalacja nowych przekaźników i testy.",
        "Czyszczenie styków przekaźników. Czyszczenie i konserwacja styków, sprawdzenie poprawności działania po czyszczeniu.",
        "Testowanie i kalibracja przekaźników. Testy funkcjonalności, kalibracja do odpowiednich parametrów."
    ],
    "Przepalenie żarówek": [
        "Wymiana przepalonych żarówek. Identyfikacja przepalonych żarówek, demontaż i instalacja nowych żarówek, testy po wymianie.",
        "Sprawdzenie i naprawa obwodów zasilających. Diagnoza problemu, naprawa lub wymiana uszkodzonych elementów, testy po naprawie.",
        "Instalacja żarówek o wyższej trwałości. Dobór odpowiednich żarówek, instalacja i testy po wymianie."
    ],
    "Uszkodzenie przewodów zasilających": [
        "Wymiana uszkodzonych przewodów. Identyfikacja uszkodzonych przewodów, wymiana na nowe przewody, testy poprawności działania.",
        "Naprawa uszkodzeń izolacji przewodów. Diagnoza uszkodzeń, naprawa izolacji, testy po naprawie.",
        "Instalacja zabezpieczeń przewodów. Diagnoza przyczyn uszkodzeń, instalacja odpowiednich zabezpieczeń, testy po instalacji."
    ],
    "Usterka modułu sterującego": [
        "Wymiana modułu sterującego. Diagnoza uszkodzenia, demontaż uszkodzonego modułu, instalacja nowego modułu i testy.",
        "Aktualizacja oprogramowania modułu. Sprawdzenie wersji oprogramowania, aktualizacja do najnowszej wersji, testy po aktualizacji.",
        "Kalibracja modułu sterującego. Sprawdzenie ustawień modułu, dostosowanie parametrów pracy, testy poprawności działania."
    ],
    "Uszkodzenie głośnika": [
        "Wymiana uszkodzonego głośnika. Diagnoza uszkodzenia, demontaż uszkodzonego głośnika, instalacja nowego głośnika i testy.",
        "Naprawa membrany głośnika. Diagnoza uszkodzeń membrany, naprawa lub wymiana membrany, testy po naprawie.",
        "Kalibracja dźwięku. Sprawdzenie ustawień dźwięku, kalibracja do odpowiednich parametrów, testy poprawności działania."
    ],
    "Zwarcie w obwodach akustycznych": [
        "Lokalizacja i naprawa zwarcia. Diagnoza miejsca zwarcia, naprawa uszkodzonego obwodu, testowanie poprawności działania.",
        "Wymiana uszkodzonych przewodów. Identyfikacja uszkodzonych przewodów, wymiana przewodów na nowe, testy po wymianie.",
        "Instalacja zabezpieczeń przeciążeniowych. Diagnoza przyczyn zwarcia, instalacja odpowiednich zabezpieczeń, testy po instalacji."
    ],
    "Usterka modułu dźwiękowego": [
        "Wymiana modułu dźwiękowego. Diagnoza uszkodzenia, demontaż uszkodzonego modułu, instalacja nowego modułu i testy.",
        "Aktualizacja oprogramowania modułu. Sprawdzenie wersji oprogramowania, aktualizacja do najnowszej wersji, testy po aktualizacji.",
        "Kalibracja modułu dźwiękowego. Sprawdzenie ustawień modułu, dostosowanie parametrów pracy, testy poprawności działania."
    ]
}



    LOG_FILE = "log.csv"

    def load_log_data():
        """
        Wczytuje dane z pliku log i aktualizuje globalne słowniki.
        """
        global confirmed_faults, repair_stats
        try:
            with open(LOG_FILE, newline='') as csvfile:
                logreader = csv.reader(csvfile)
                for row in logreader:
                    if row[1] == "Confirmed":
                        confirmed_faults[row[2]] += 1
                    elif row[1] == "Repaired":
                        repair_stats[row[2]][row[3]] += 1
        except FileNotFoundError:
            pass

    def write_log_entry(entry_type, fault, option=None):
        """
        Zapisuje wpis do pliku log.
        """
        with open(LOG_FILE, "a", newline='') as csvfile:
            logwriter = csv.writer(csvfile)
            logwriter.writerow([datetime.now().strftime('%Y-%m-%d %H:%M:%S'), entry_type, fault, option])

    def create_tab(tab_control, tab_name, simulation_function, diagnostics_function):
        """
        Tworzy nową zakładkę w kontrolce tab_control i dodaje do niej kolumny.
        """
        tab = ttk.Frame(tab_control)
        tab_control.add(tab, text=tab_name)
        simulation_frame, diagnostics_frame = create_columns(tab)
        simulation_function(simulation_frame, diagnostics_frame)
        diagnostics_function(diagnostics_frame)
        return tab

    def create_columns(parent):
        """
        Tworzy dwie kolumny w podanym elemencie nadrzędnym.
        """
        simulation_frame = ttk.Frame(parent)
        simulation_frame.pack(side="left", fill="both", expand=True)
        diagnostics_frame = ttk.Frame(parent)
        diagnostics_frame.pack(side="right", fill="both", expand=True)
        return simulation_frame, diagnostics_frame

    def start_simulation_log(date_time, time, options):
        """
        Generuje komunikat logu na podstawie czasu i wybranych opcji.
        """
        log_message = f"Data i godzina symulacji: {date_time}\n"
        if time and int(time) > 15:
            log_message += "Ostrzeżenie: Opóźnione zamykanie rogatek!\n"
        if options:
            for option in options:
                log_message += f"Ostrzeżenie: {option}!\n"
        if time and int(time) <= 15 and not options:
            log_message += "Wszystko w porządku\n"
        return log_message

    def start_simulation(entry_time, listbox, diagnostics_frame):
        """
        Rozpoczyna symulację na podstawie podanych danych wejściowych.
        """
        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time = entry_time.get()
        options_idx = listbox.curselection()
        options = [listbox.get(idx) for idx in options_idx]
        diagnostics_text = diagnostics_frame.winfo_children()[1]

        # Usunięcie poprzedniego komunikatu
        diagnostics_text.delete('1.0', tk.END)

        global simulated_faults
        simulated_faults = set(options)  # Aktualizacja zbioru zasymulowanych usterek

        if time and int(time) > 15:
            simulated_faults.add("Opóźnione zamykanie rogatek")

        log_message = start_simulation_log(date_time, time, options)

        # Dodanie komunikatu do widżetu Text
        if time and int(time) > 15:
            diagnostics_text.tag_configure("warning", foreground="red")
            diagnostics_text.insert(tk.END, f"Ostrzeżenie: Opóźnione zamykanie rogatek! ({date_time})\n", "warning")
        if options:
            for option in options:
                diagnostics_text.tag_configure("warning", foreground="red")
                diagnostics_text.insert(tk.END, f"Ostrzeżenie: {option}! ({date_time})\n", "warning")
        if time and int(time) <= 15 and not options:
            diagnostics_text.insert(tk.END, f"Wszystko w porządku ({date_time})\n")

        # Zapisanie komunikatu do pliku log.csv
        if time and int(time) > 15:
            write_log_entry("Simulated", "Opóźnione zamykanie rogatek")
        for option in options:
            write_log_entry("Simulated", option)

    def function_for_tab_A_simulation(frame, diagnostics_frame):
        """
        Funkcja tworząca elementy interfejsu dla symulacji w zakładce A.
        """
        style = ttk.Style()
        style.configure("Title.TLabel", font=("Helvetica", 15, "bold"))

        # Dodanie tytułu "X"
        ttk.Label(frame, text="Symulacja Awarii na przejeżdzie w km. 36.420", style="Title.TLabel").pack(padx=10, pady=10)

        ttk.Label(frame, text="Czas zamknięcia przejazdu (sekundy):").pack(padx=10, pady=10)
        entry_time = ttk.Entry(frame)
        entry_time.pack(padx=10, pady=5)

        options = ["Awaria mechanizmu rogatek", "Awaria sygnalizacji świetlnej", "Awaria sygnalizacji dźwiękowej"]
        listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=36)  # Zwiększenie szerokości listy
        for option in options:
            listbox.insert(tk.END, option)
        listbox.pack(padx=10, pady=5)

        start_button = ttk.Button(frame, text="Start Symulacji", command=lambda: start_simulation(entry_time, listbox, diagnostics_frame))
        start_button.pack(pady=10)
        
        # Dodanie obrazka "kata.jpg"
        image = Image.open("kata.jpg")
        image = image.resize((400, 300), Image.Resampling.LANCZOS)  # Zmiana rozmiaru obrazu
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(frame, image=photo)
        image_label.image = photo  # Przypisanie referencji do obrazka, aby nie został usunięty przez garbage collector
        image_label.pack(padx=10, pady=10)

    def submit_fault(diagnostics_text, simulated_faults):
        """
        Zatwierdza usterkę i aktualizuje log.
        """
        global confirmed_faults

        confirmation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for option in simulated_faults:
            confirmed_faults[option] += 1

            diagnostics_text.tag_configure("confirmation", foreground="blue")
            diagnostics_text.insert(tk.END, f"Potwierdzono: {option} ({confirmed_faults[option]} raz(y))! ({confirmation_time})\n", "confirmation")
            write_log_entry("Confirmed", option)

        # Usunięcie ostrzeżeń
        diagnostics_text.tag_remove("warning", "1.0", tk.END)

        # Aktualizacja widżetu Text
        text_content = diagnostics_text.get("1.0", "end-1c").split('\n')
        new_text_content = [line for line in text_content if not line.startswith("Ostrzeżenie:")]
        diagnostics_text.delete('1.0', tk.END)
        for line in new_text_content:
            diagnostics_text.insert(tk.END, line + '\n')

        # Wywołanie okna dialogowego do zatwierdzenia naprawy usterki
        show_repair_options(diagnostics_text, simulated_faults)

    def show_repair_options(diagnostics_text, simulated_faults):
        """
        Wyświetla okno z opcjami naprawy usterek.
        """
        def show_repair_options_for_fault():
            selected_fault = fault_var.get()
            if selected_fault:
                repair_options_window = tk.Toplevel()
                repair_options_window.title(f"Opcje naprawy dla {selected_fault}")
                repair_options_window.geometry("800x600")

                ttk.Label(repair_options_window, text=f"Opcje naprawy dla {selected_fault}:").pack(padx=10, pady=10)

                repair_var = tk.StringVar()
                other_entry = ttk.Entry(repair_options_window)
                other_entry.pack_forget()

                options_combobox = ttk.Combobox(repair_options_window, textvariable=repair_var, width=50)
                options_combobox.pack(padx=10, pady=5)

                options = repair_options.get(selected_fault, ["Inna"]) + custom_repair_options[selected_fault]
                options_combobox['values'] = options

                def on_combobox_change(event):
                    if repair_var.get() == "Inna":
                        other_entry.pack(padx=10, pady=5)
                    else:
                        other_entry.pack_forget()

                options_combobox.bind("<<ComboboxSelected>>", on_combobox_change)

                def confirm_repair():
                    selected_option = repair_var.get()
                    if selected_option == "Inna":
                        selected_option = other_entry.get()
                        if selected_option and selected_option not in custom_repair_options[selected_fault]:
                            custom_repair_options[selected_fault].append(selected_option)

                    repair_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    repair_stats[selected_fault][selected_option] += 1
                    diagnostics_text.insert(tk.END, f"Naprawiono: {selected_fault} ({selected_option}) ({repair_time})\n", "confirmation")
                    write_log_entry("Repaired", selected_fault, selected_option)
                    repair_options_window.destroy()

                ttk.Button(repair_options_window, text="Zatwierdź naprawę usterki", command=confirm_repair).pack(pady=10)

            repair_window.destroy()

        repair_window = tk.Toplevel()
        repair_window.title("Opcje usterek dla poszczególnej awarii")
        repair_window.geometry("800x600")

        ttk.Label(repair_window, text="Wybierz usterkę:").pack(padx=10, pady=10)

        fault_var = tk.StringVar()
        fault_combobox = ttk.Combobox(repair_window, textvariable=fault_var, width=50)
        fault_combobox.pack(padx=10, pady=5)

        detailed_faults = []
        for fault in simulated_faults:
            if fault in repair_options_dict:
                detailed_faults.extend(repair_options_dict[fault])

        fault_combobox['values'] = detailed_faults

        ttk.Button(repair_window, text="Zatwierdź awarie dla urządzenia", command=show_repair_options_for_fault).pack(pady=10)

    def choose_repair_option(diagnostics_text):
        """
        Wyświetla okno wyboru opcji naprawy.
        """
        repair_window = tk.Toplevel()
        repair_window.title("Wybierz opcję naprawy")
        repair_window.geometry("800x600")

        ttk.Label(repair_window, text="Wybierz rodzaj naprawy:").pack(padx=10, pady=10)

        fault_var = tk.StringVar()
        fault_combobox = ttk.Combobox(repair_window, textvariable=fault_var, width=50)
        fault_combobox.pack(padx=10, pady=5)

        fault_combobox['values'] = list(repair_options.keys())

        def show_repair_options_for_fault():
            selected_fault = fault_var.get()
            if selected_fault:
                repair_options_window = tk.Toplevel()
                repair_options_window.title(f"Opcje naprawy dla {selected_fault}")
                repair_options_window.geometry("800x600")

                ttk.Label(repair_options_window, text=f"Opcje naprawy dla {selected_fault}:").pack(padx=10, pady=10)

                repair_var = tk.StringVar()
                other_entry = ttk.Entry(repair_options_window)
                other_entry.pack_forget()

                options_combobox = ttk.Combobox(repair_options_window, textvariable=repair_var, width=50)
                options_combobox.pack(padx=10, pady=5)

                options = repair_options.get(selected_fault, ["Inna"]) + custom_repair_options[selected_fault]
                options_combobox['values'] = options

                def on_combobox_change(event):
                    if repair_var.get() == "Inna":
                        other_entry.pack(padx=10, pady=5)
                    else:
                        other_entry.pack_forget()

                options_combobox.bind("<<ComboboxSelected>>", on_combobox_change)

                def confirm_repair():
                    selected_option = repair_var.get()
                    if selected_option == "Inna":
                        selected_option = other_entry.get()
                        if selected_option and selected_option not in custom_repair_options[selected_fault]:
                            custom_repair_options[selected_fault].append(selected_option)

                    repair_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    repair_stats[selected_fault][selected_option] += 1
                    diagnostics_text.insert(tk.END, f"Naprawiono: {selected_fault} ({selected_option}) ({repair_time})\n", "confirmation")
                    write_log_entry("Repaired", selected_fault, selected_option)
                    repair_options_window.destroy()

                ttk.Button(repair_options_window, text="Zatwierdź naprawę usterki", command=confirm_repair).pack(pady=10)

        ttk.Button(repair_window, text="Zatwierdz opcje naprawy", command=show_repair_options_for_fault).pack(pady=10)

    def show_statistics():
        """
        Wyświetla okno ze statystykami usterek i napraw.
        """
        stats_window = tk.Toplevel()
        stats_window.title("Statystyki awarii i napraw")
        stats_window.geometry("1400x900")  # Zwiększenie szerokości okna

        frame = ttk.Frame(stats_window)
        frame.pack(fill='both', expand=True)

        tab_control = ttk.Notebook(frame)
        tab_control.pack(expand=1, fill='both')

        fault_tab = ttk.Frame(tab_control)
        repair_tab = ttk.Frame(tab_control)

        tab_control.add(fault_tab, text='Awarie')
        tab_control.add(repair_tab, text='Naprawy')

        show_fault_statistics(fault_tab)
        show_repair_statistics(repair_tab)

    def on_click_fault(event):
        """
        Obsługuje kliknięcie na wykresie usterek.
        """
        for bar in event.inaxes.patches:
            if bar.contains(event)[0]:
                fault = event.inaxes.get_yticklabels()[int(bar.get_y() + bar.get_height() / 2)].get_text()
                show_fault_details(fault)


    def show_fault_details(fault):
        """
        Wyświetla szczegóły dla wybranej awarii.
        """
        global opened_windows

        if fault in opened_windows:
            opened_windows[fault].lift()
            return

        details_window = tk.Toplevel()
        details_window.title(f"Detale dla {fault}")
        details_window.geometry("1400x900")
        details_window.protocol("WM_DELETE_WINDOW", lambda: close_window(fault))

        frame = ttk.Frame(details_window)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, text=f"Naprawy dla {fault}:").pack(padx=10, pady=10)

        fig, ax = plt.subplots(figsize=(12, 8))
        if fault in repair_stats and repair_stats[fault]:
            options = list(repair_stats[fault].keys())
            counts = list(repair_stats[fault].values())
            bars = ax.barh(options, counts, color=[(random.random(), random.random(), random.random()) for _ in options])
            ax.set_xlabel('Liczba usterek')
            ax.set_ylabel('Opcje usterek')
            ax.set_title(f'Usterki dla {fault}')
            for bar, option, count in zip(bars, options, counts):
                width = bar.get_width()
                ax.text(width, bar.get_y() + bar.get_height() / 2, f'{count}', va='center')  # przeniesienie tekstu nad słupki
            fig.tight_layout()
        else:
            ttk.Label(frame, text="Brak danych o naprawach").pack(padx=10, pady=5)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.draw()

        opened_windows[fault] = details_window


    def close_window(fault):
        """
        Zamknięcie okna i usunięcie go ze słownika otwartych okien.
        """
        if fault in opened_windows:
            opened_windows[fault].destroy()
            del opened_windows[fault]

    def show_fault_statistics(frame):
        """
        Wyświetla statystyki usterek w podanym ramce.
        """
        ttk.Label(frame, text="Statystyki Awarii").pack(padx=10, pady=10)
        fig, ax = plt.subplots(figsize=(12, 8))
        faults = list(confirmed_faults.keys())
        counts = list(confirmed_faults.values())
        bars = ax.barh(faults, counts, color=[(random.random(), random.random(), random.random()) for _ in faults])
        ax.set_xlabel('Liczba wystąpień')
        ax.set_ylabel('Awarie')
        ax.set_title('Statystyka dla przejazdu 36.420')
        for bar, fault, count in zip(bars, faults, counts):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height() / 2, f'{width}', va='center')  # przeniesienie tekstu nad słupki
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.draw()

        fig.canvas.mpl_connect('button_press_event', on_click_fault)


    def show_repair_statistics(frame):
        """
        Wyświetla statystyki napraw w podanej ramce.
        """
        ttk.Label(frame, text="Statystyki napraw").pack(padx=10, pady=10)
        fig, ax = plt.subplots(figsize=(12, 8))
        for fault, repairs in repair_stats.items():
            options = list(repairs.keys())
            counts = list(repairs.values())
            bars = ax.barh(options, counts, label=fault, color=[(random.random(), random.random(), random.random()) for _ in options])
            for bar, option, count in zip(bars, options, counts):
                width = bar.get_width()
                ax.text(width + 0.1, bar.get_y() + bar.get_height() / 2, f'{count}', va='center')  # przeniesienie tekstu nad słupki
        ax.set_xlabel('Liczba napraw')
        ax.set_ylabel('Opcje napraw')
        ax.set_title('Statystyki napraw')
        ax.legend()
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(fill='both', expand=True)
        canvas.draw()


    def show_statistics_summary():
        """
        Wyświetla okno z podsumowaniem statystyk i obliczeniami prawdopodobieństwa usterek.
        """
        summary_window = tk.Toplevel()
        summary_window.title("Podsumowanie statystyk")

        frame = ttk.Frame(summary_window)
        frame.pack(fill='both', expand=True, padx=10, pady=10)

        total_faults = sum(confirmed_faults.values())
        summary_text = f"Całkowita liczba potwierdzonych usterek: {total_faults}\n\n"

        for fault, count in confirmed_faults.items():
            probability = count / total_faults if total_faults > 0 else 0
            summary_text += f"{fault}:\n - Liczba wystąpień: {count}\n - Prawdopodobieństwo: {probability:.2%}\n\n"

        summary_label = ttk.Label(frame, text=summary_text, justify=tk.LEFT)
        summary_label.pack()

    def function_for_tab_A_diagnostics(frame):
        """
        Funkcja tworząca elementy interfejsu dla diagnostyki w zakładce A.
        """
        ttk.Label(frame, text="Komunikat:").pack(padx=10, pady=10)
        diagnostics_text = tk.Text(frame, height=15, width=60)
        diagnostics_text.pack(padx=10, pady=5)
        diagnostics_text.insert(tk.END, "Rozpocznij symulację")

        ttk.Button(frame, text="Zatwierdź usterkę", command=lambda: submit_fault(diagnostics_text, simulated_faults)).pack(pady=10)
        ttk.Button(frame, text="Wybierz opcję naprawy", command=lambda: choose_repair_option(diagnostics_text)).pack(pady=10)
        ttk.Button(frame, text="Pokaż statystyki", command=show_statistics).pack(pady=10)

    def main():
        """
        Główna funkcja uruchamiająca program.
        """
        def exit_program():
            root.destroy()

        root = tk.Tk()
        root.title("Diagnostyka usterek")

        window_width = root.winfo_screenwidth()
        window_height = root.winfo_screenheight()
        root.geometry(f"{window_width}x{window_height}")

        tab_control = ttk.Notebook(root)

        # Zwiększony tytuł na górze tabeli
        title_label = ttk.Label(root, text="Sektor: Śląsk, Sekcja: LCS Katowice, Stacja: Mysłowice, Systemy: Przejazdy kolejowo-drogowe", font=("Helvetica", 18, "bold"))
        title_label.pack(pady=20)

        tabs = [("Przejazd w km. 36.420", function_for_tab_A_simulation, function_for_tab_A_diagnostics)]

        for tab_name, simulation_function, diagnostics_function in tabs:
            create_tab(tab_control, tab_name, simulation_function, diagnostics_function)

        tab_control.pack(expand=1, fill="both")

        summary_button = ttk.Button(root, text="Pokaż prawdopodobieństwo zdarzeń", command=show_statistics_summary)
        summary_button.pack(pady=10)

        exit_button = tk.Button(root, text="Zakończ", command=exit_program)
        exit_button.pack(pady=10)

        load_log_data()
        root.mainloop()

    main()

def choose_option(level, root):
    def next_choice(choice):
        if choice == 'Sektor: Śląsk':
            choose_option('Sektor: Śląsk', root)
        elif choice == 'Sekcja: LCS Katowice':
            choose_option('Sekcja: LCS Katowice', root)
        elif choice == 'Stacja: Mysłowice':
            choose_option('Stacja: Mysłowice', root)
        elif choice == 'Przejazdy kolejowo-drogowe':
            root.destroy()
            main_program()
        elif choice in ['Sektor: Mazowieckie', 'LCS Gliwice', 'LCS Częstochowa', 'Stacja: Katowice-Szopienice', 'Stacja: Katowice-Ligota', 'Napędy zwrotnicowe:', 'Semafory']:
            # Placeholder for other options if needed
            pass

    for widget in root.winfo_children():
        widget.destroy()

    if level == 'start':
        options = ['Sektor: Śląsk', 'Sektor: Mazowieckie', 'Sektor: Pomorskie']
    elif level == 'Sektor: Śląsk':
        options = ['Sekcja: LCS Katowice', 'LCS Gliwice', 'LCS Częstochowa']
    elif level == 'Sekcja: LCS Katowice':
        options = ['Stacja: Mysłowice', 'Stacja: Katowice-Szopienice', 'Stacja: Katowice-Ligota']
    elif level == 'Stacja: Mysłowice':
        options = ['Przejazdy kolejowo-drogowe', 'Napędy zwrotnicowe:', 'Semafory']

    for option in options:
        button = ttk.Button(root, text=option, command=lambda opt=option: next_choice(opt))
        button.pack(pady=10)

def initial_screen():
    root = tk.Tk()
    root.title("Wybór opcji")
    root.geometry("300x200")
    choose_option('start', root)
    root.mainloop()

if __name__ == "__main__":
    initial_screen()
