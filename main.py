import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import difflib

def utwory_z_folderu(dis):
    try:
        if not os.path.isdir(dis):
            print(f"Ścieżka {dis} nie jest katalogiem.")
            return []
        pliki = os.listdir(dis)
        pliki_bez_mp3 = [os.path.splitext(plik)[0].lower() for plik in pliki]  # TO CO W TABLICY NA MALE LITERKI
        pliki_bez_mp3.sort()  # SORTUJE LISTE
        print(f"Pliki w katalogu '{dis}': {pliki_bez_mp3}")
        return pliki_bez_mp3

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return []

def utwory_z_soundclouda(playlist_url):
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(playlist_url)
        time.sleep(10)  # Poczekaj na załadowanie strony

        # Użyj WebDriverWait, aby upewnić się, że elementy są załadowane
        track_elements = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "trackItem__trackTitle"))
        )

        titles = [element.text.lower() for element in track_elements]  # ELEMENTY W TABLICY NA MALE LITERY
        driver.quit()  # ZAMYKANIE PRZEGLADARKI
        return titles

    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return []

def znajdz_podobne(tytul, lista):
    wyniki = difflib.get_close_matches(tytul, lista, n=1, cutoff=0.6)
    if wyniki:
        return wyniki[0]
    else:
        return None

dis = 'D:\\HARDTECHNOJAKCHUJ'
playlist_url = 'https://on.soundcloud.com/4m9pzRz1mp42gCFr5'
folder_songs = utwory_z_folderu(dis)
soundcloud_songs = utwory_z_soundclouda(playlist_url)

niepasujace_piosenki = []

for soundcloud_title in soundcloud_songs:
    dopasowanie = znajdz_podobne(soundcloud_title, folder_songs)
    if dopasowanie is None:
        niepasujace_piosenki.append(soundcloud_title) # DODAJE DO LISTY TYTULY KTORE NIE ZNALAZY DOPASOWANIA W CALEJ TAB

# Wyświetl niepasujące piosenki
if niepasujace_piosenki:
    print("Brakujące piosenki:")
    for i, song in enumerate(niepasujace_piosenki, start=1):
        print(f"{i}. {song}")
else:
    print("Nie znaleziono brakujących piosenek.")
