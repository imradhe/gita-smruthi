import os
import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def get_sloka(chapter, verse):
    file_path = os.path.join("slokas", f"{chapter}.{verse}.json")
    
    if os.path.isfile(file_path):
        # Sloka file already exists, so load and return the data
        with open(file_path, 'r', encoding='utf-8') as sloka_file:
            sloka_data = json.load(sloka_file)
        return sloka_data
    
    url = f"https://www.holy-bhagavad-gita.org/chapter/{chapter}/verse/{verse}"
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        sloka_data = {
            "id": f"{chapter}.{verse}",
            "chapter": chapter,
            "verse": verse,
            "text": soup.select_one("#originalVerse").get_text(strip=True, separator="\n"),
            "translation": {},
            "commentary": {}
        }
        languages = ["en", "te", "hi", "ta", "gu", "or"]
        with tqdm(total=len(languages), desc=f"Sloka {chapter}.{verse}") as pbar:
            for lang in languages:
                try:
                    lang_url = f"{url}/{lang}"
                    lang_response = requests.get(lang_url)

                    if lang_response.status_code == 200:
                        lang_soup = BeautifulSoup(lang_response.content, "html.parser")
                        translation_elem = lang_soup.select_one("#translation")
                        commentary_elem = lang_soup.select_one("#commentary")

                        translation = translation_elem.get_text(strip=True, separator="\n") if translation_elem else ""
                        commentary = commentary_elem.get_text(strip=True, separator="\n") if commentary_elem else ""

                        sloka_data["translation"][lang] = translation
                        sloka_data["commentary"][lang] = commentary

                    pbar.update(1)
                except Exception as e:
                    error_logs = []
                    error_logs.append(f"Error: Failed to download {lang} translation/commentary for Sloka {chapter}.{verse}")
                    error_logs.append(f"ID: {chapter}.{verse}")
                    error_logs.append(f"Language: {lang}")
                    error_logs.append(f"Exception: {str(e)}\n")

                    with open('logs.txt', 'a', encoding='utf-8') as logs_file:
                        logs_file.write('\n'.join(error_logs))
        
        # Create the "slokas" directory if it doesn't exist
        os.makedirs("slokas", exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as sloka_file:
            json.dump(sloka_data, sloka_file, indent=4, ensure_ascii=False)
        
        return sloka_data
    else:
        return None


def download():
    with open('stats.json', 'r') as stats_file:
        stats_data = json.load(stats_file)

    slokas_data = []
    total_slokas = sum(list(chapter.values())[0] for chapter in stats_data)
    slokas_downloaded = 0

    print("Downloading slokas...")
    error_logs = []

    with tqdm(total=total_slokas) as pbar:
        for chapter in stats_data:
            chapter_number = list(chapter.keys())[0]
            slokas_count = chapter[chapter_number]

            for verse in range(1, slokas_count + 1):
                try:
                    sloka = get_sloka(chapter_number, verse)

                    if sloka:
                        slokas_data.append(sloka)
                        slokas_downloaded += 1
                        pbar.update(1)
                except Exception as e:
                    error_logs.append(f"Error: Failed to download Sloka {chapter_number}.{verse}")
                    error_logs.append(f"ID: {chapter_number}.{verse}")
                    error_logs.append(f"Exception: {str(e)}\n")

    with open('slokas.json', 'w', encoding='utf-8') as slokas_file:
        json.dump(slokas_data, slokas_file, indent=4, ensure_ascii=False)

    with open('logs.txt', 'a', encoding='utf-8') as logs_file:
        logs_file.write('\n'.join(error_logs))

    print("Slokas downloaded successfully.")

download()
