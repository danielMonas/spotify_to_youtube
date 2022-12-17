from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from log import logger


class SpotifyFetcher:
    def __init__(self, playlist_url: str, expected_songs_count: int):
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)
        self.expected_songs_count = expected_songs_count
        self.driver.get(playlist_url)
        # Remove the Cookies popup
        try:
            WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="onetrust-close-btn-container"]/button'))).click()
            logger.debug("accepted cookies")
        except Exception as e:
            logger.debug('no cookie button')

    def destroy_driver(self) -> None:
        self.driver.quit()

    def _load_available_entries(self) -> list:
        '''
        Loads the currently available songs - this is only part of the whole playlist
        '''
        table = self.driver.find_element(By.CSS_SELECTOR, 'div[data-testid="playlist-tracklist"]')
        raw_entries = table.find_elements(By.CSS_SELECTOR, 'div[role="row"]')[1:]
        songs = []
        for entry in raw_entries:
            song_name_element = entry.find_element(By.CSS_SELECTOR, 'a[data-testid="internal-track-link"]')
            band_name_element = song_name_element.find_elements(By.XPATH, './../span')[-1]
            song_name = song_name_element.text
            band_name = band_name_element.text
            logger.debug(f'Got: {song_name}, by: {band_name}')
            songs.append((song_name, band_name))
        return songs

    def load_all_entries(self) -> list:
        songs = []
        unique_songs = set()
        # Accessing the bottom sentinel will load the next entities
        bottom_sentinel = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-testid='bottom-sentinel']")))
        while len(unique_songs) < self.expected_songs_count:
            songs += self._load_available_entries()
            # While loading more songs, some of the previously loaded ones might
            # still appear and be loaded again
            unique_songs = set(songs)
            bottom_sentinel.location_once_scrolled_into_view
            self.driver.implicitly_wait(3)
        return list(unique_songs)
