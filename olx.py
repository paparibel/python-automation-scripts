import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from plyer import notification
import winsound

# === KONFIGURACJA ===
URL = "https://www.olx.pl/sport-hobby/rowery/akcesoria-rowerowe/q-garmin-edge-530/"
CHECK_INTERVAL = 180  # 3 minuty


def get_offer_links(driver):
    offers = driver.find_elements(By.CSS_SELECTOR, 'div[data-cy="l-card"] a')
    return [offer.get_attribute('href') for offer in offers if offer.get_attribute('href')]


def notify(title, message):
    # Windows notyfikacja
    notification.notify(
        title=title,
        message=message,
        timeout=10  # sekundy
    )
    # Dźwiękowy alarm
    for _ in range(3):
        winsound.Beep(1000, 300)
        time.sleep(0.1)


def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # nie zamykaj przeglądarki po zakończeniu

    service = Service()  # Zakłada, że chromedriver jest w PATH
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get(URL)

    print("Monitoring ogłoszeń OLX rozpoczęty...")
    previous_links = set(get_offer_links(driver))

    while True:
        time.sleep(CHECK_INTERVAL)
        driver.refresh()
        current_links = set(get_offer_links(driver))

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_links = current_links - previous_links

        if new_links:
            for link in new_links:
                notify("Nowe ogłoszenie OLX", link)
                print(f"[{now}] [NOWE] {link}")
        else:
            print(f"[{now}] Brak nowych ogłoszeń. Odświeżenie wykonane.")

        previous_links = current_links


if __name__ == "__main__":
    main()
