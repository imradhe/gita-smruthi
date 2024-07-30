import json
import requests
from tqdm import tqdm

api_endpoint = "https://bhagavadgitaapi.in/slok/{chapter}/{sloka}/"
logs_file = "logs.txt"
stats_file = "stats.json"

def check_slok_character(chapter, sloka):
    api_url = api_endpoint.format(chapter=chapter, sloka=sloka)
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        last_sloka = data["slok"]
        if not last_sloka.startswith("ॐ"):
            with open(logs_file, "a", encoding="utf-8") as f:
                f.write(f"Chapter {chapter}: Last sloka does not start with 'ॐ'\n")
    else:
        with open(logs_file, "a", encoding="utf-8") as f:
            f.write(f"Chapter {chapter}: API request failed\n")

def check_stats():
    with open(stats_file, "r") as f:
        stats = json.load(f)
    
    progress_bar = tqdm(stats, desc="Checking stats", unit="chapter")
    for chapter_stat in progress_bar:
        chapter = int(list(chapter_stat.keys())[0])
        sloka_count = chapter_stat[str(chapter)]
        check_slok_character(chapter, sloka_count)

check_stats()