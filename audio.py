import os
import requests
from tqdm import tqdm

# Function to create directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Function to download a file
def download_file(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)

# Main function to download all slokas
def download_all_slokas(base_url, chapters, slokas_per_chapter):
    create_directory(f"audio")
    for chapter in tqdm(range(1, chapters + 1), desc="Chapters"):
        chapter_str = f"{chapter}"
        for sloka in tqdm(range(1, slokas_per_chapter[chapter - 1] + 1), desc=f"Chapter {chapter_str} Slokas", leave=False):
            sloka_str = f"{sloka}"
            url = f"{base_url}/CHAP{chapter_str}/{chapter_str}-{sloka_str}.MP3"
            save_path = f"audio/{chapter_str}-{sloka_str}.MP3"
            download_file(url, save_path)

if __name__ == "__main__":
    base_url = "https://www.gitasupersite.iitk.ac.in/sites/default/files/audio"
    # Define the number of chapters and slokas per chapter (for simplicity, an example array is used)
    # Update slokas_per_chapter based on the actual number of slokas in each chapter of the Gita
    slokas_per_chapter = [47, 72, 43, 42, 29, 47, 30, 28, 34, 42, 55, 20, 35, 27, 20, 24, 28, 78]  # Example data
    
    download_all_slokas(base_url, len(slokas_per_chapter), slokas_per_chapter)
