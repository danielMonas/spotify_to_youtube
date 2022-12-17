from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class YoutubeFetcher:
    YOUTUBE_SEARCH_URL = 'https://music.youtube.com/search?q='
    def __init__(self):
        service = Service(executable_path=ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)

    def destroy_driver(self) -> None:
        self.driver.quit()

    def load_song(self, query: str) -> str:
        query = query.replace(' ', '+')
        self.driver.get(f'{self.YOUTUBE_SEARCH_URL}{query}')
        link = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='watch?v=']")))
        href = link.get_attribute('href')
        return href.split('watch?v=')[-1]
