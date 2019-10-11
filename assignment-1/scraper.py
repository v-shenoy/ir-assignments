import string
import time
import os
import json

import requests
from bs4 import BeautifulSoup


if __name__ == "__main__":

    ARTIST_PAGE_URL = "https://genius.com/artists-index/"
    DATASET_DIRECTORY_NAME = "lyrics-dataset"


    if not os.path.isdir(os.path.join(os.getcwd(), DATASET_DIRECTORY_NAME)):
        os.mkdir(DATASET_DIRECTORY_NAME)
    os.chdir(DATASET_DIRECTORY_NAME)

    songs_scraped = 0
    for letter in string.ascii_lowercase:

        while True:
            try:
                artist_page = requests.get(ARTIST_PAGE_URL + letter)
                artist_soup = BeautifulSoup(artist_page.text, "html.parser")

                artists = artist_soup.select(".artists_index_list-popular_artist")
                for artist in artists:
                    artist_name = artist.select_one(".artists_index_list-artist_name").text.strip()

                    print(f"Scraping songs by - {artist_name}")
                    for song in artist.select(".popular_song a"):
                        song_name = song.text.strip()
                        song_link = song["href"]

                        print(f"\t{song_name}")                        
                        t_start = time.time()
                        while True:
                            try:
                                song_page = requests.get(song_link)
                                delta_t = time.time() - t_start

                                song_soup = BeautifulSoup(song_page.text, "html.parser")

                                song_info = song_soup.select(".metadata_unit")

                                produced_by = ""
                                album = ""
                                date = ""

                                if len(song_info) > 0:
                                    produced_by = song_info[0].select_one(".metadata_unit-info").text.strip()
                                if len(song_info) > 1:
                                    album = song_info[1].select_one(".metadata_unit-info").text.strip()

                                lyrics = song_soup.select_one(".lyrics").text.strip()

                                for row in song_soup.select(".metadata_unit.metadata_unit--table_row"):
                                    if "Release Date" in row.text:
                                        date = row.select("span")[1].text

                                song_json = {
                                    "artist_name": artist_name,
                                    "song_name": song_name,
                                    "album": album,
                                    "produced_by": produced_by,
                                    "date": date,
                                    "lyrics": lyrics,
                                    "song_link": song_link,

                                }

                                file_name = song_json["song_name"].lower()
                                file_name = ''.join(file_name.split())
                                file_name = file_name.replace("/", "")
                                with open(file_name + ".json", "w") as output_file:
                                    json.dump(song_json, output_file, indent = 2, ensure_ascii = False)

                                time.sleep(2*delta_t)
                                songs_scraped += 1
                                break
                            except requests.exceptions.RequestException:
                                pass
                break
            except requests.exceptions.RequestException:
                pass
    
    print(f"Songs scraped - {songs_scraped}")
