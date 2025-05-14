import cx_Oracle
import pandas as pd
import datetime

# Lista baz LDS z IP Intranet 1
db_connections = {
 
}

# Wybór bazy danych przez użytkownika
print("\n📌 Wybierz bazę danych LDS:")
for i, db_name in enumerate(db_connections.keys(), 1):
    print(f"{i}. {db_name}")

choice = int(input("\n🔹 Podaj numer bazy: "))
selected_db = list(db_connections.keys())[choice - 1]
selected_host = db_connections[selected_db]
DB_DSN = cx_Oracle.makedsn(selected_host, 2599, sid="lds")  # Używamy SID

print(f"\n✅ Połączono z: {selected_db} ({selected_host}:2599/lds)")

# Dane logowania
DB_USER = "my_user"
DB_PASSWORD = "****"

# Pobranie zakresu dat w formacie YYMM
start_ym = input("\n📅 Podaj początek zakresu (YYMM, np. 2401 dla Stycznia 2024): ")
end_ym = input("📅 Podaj koniec zakresu (YYMM, np. 2503 dla Marca 2025): ")

# Pobranie typu alarmów
alarm_type = input("\n🔔 Wybierz typ alarmów: 'E' lub 'F': ").strip().upper()
while alarm_type not in ["E", "F"]:
    alarm_type = input("❌ Niepoprawny wybór! Wpisz 'E' lub 'F': ").strip().upper()

# Konwersja do pełnych dat (YYYY-MM-01)
start_date = f"20{start_ym[:2]}-{start_ym[2:]}-01"
end_date = f"20{end_ym[:2]}-{end_ym[2:]}-01"

# Generowanie listy miesięcy w formacie YYMM
date_list = []
current_ym = int(start_ym)
end_ym_int = int(end_ym)

while current_ym <= end_ym_int:
    date_list.append(str(current_ym))
    
    # Zwiększ miesiąc
    year = int(str(current_ym)[:2])
    month = int(str(current_ym)[2:])

    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    
    current_ym = int(f"{year:02}{month:02}")  # np. 2401 -> 2402 -> 2403 ...

# Generowanie dynamicznego SQL zgodnego z Twoją strukturą
union_queries = []
for date_code in date_list:
    sql_part = f"""
    SELECT 
        CAS_ZAHAJENI + INTERVAL '1' HOUR AS CAS_UTC,  -- Dodanie 1h do UTC
        '{alarm_type}' || TO_CHAR(ID_HLASKY - 5000) AS POVEL, 
        FUNC_CFG_HLASKY_TEXT(id, 21, '{date_code}', 'TPC', 1) AS ALARM_TEXT
    FROM tpc.d_hlasky_01_{date_code} 
    WHERE id_hlasky BETWEEN 5000 AND 7000 
      AND id_zarizeni = 39 
      AND DELTA = 1
      AND CAS_ZAHAJENI BETWEEN TO_DATE('{start_date}', 'YYYY-MM-DD') AND TO_DATE('{end_date}', 'YYYY-MM-DD')
    """
    union_queries.append(sql_part)

# Łączenie zapytań w jedno
sql_query = " UNION ALL ".join(union_queries) + " ORDER BY 1, 2"

try:
    # Połączenie z Oracle
    connection = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_DSN)
    cursor = connection.cursor()
    
    # Wymuszenie ustawienia języka angielskiego (ważne dla daty)
    cursor.execute("ALTER SESSION SET NLS_LANGUAGE = 'AMERICAN'")

    # Pobranie wyników do pandas DataFrame
    cursor.execute(sql_query)
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    
    df = pd.DataFrame(data, columns=columns)

    # Eksport do Excela (lub CSV jeśli wolisz)
    file_name = f"export_{selected_db}_{start_ym}_to_{end_ym}_{alarm_type}.xlsx"
    df.to_excel(file_name, index=False)

    print(f"\n✅ Plik zapisany: {file_name}")

except Exception as e:
    print("\n❌ Błąd:", e)

finally:
    cursor.close()
    connection.close()
    print("🔒 Połączenie zamknięte.")
