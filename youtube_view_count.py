from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import re


class YoutubeViewCount:
    def __init__(self, video_url):
        self.options = Options()
        self.options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.options)
        self.video_url = video_url

    def get_views(self):
        data = []
        self.driver.get(self.video_url)
        wait = WebDriverWait(self.driver, 20)
        self.driver.maximize_window()

        reject_cookies = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[6]/div[1]'
                                                                              '/ytd-button-renderer[1]/yt-button-shape/'
                                                                              'button/yt-touch-feedback-shape/'
                                                                              'div/div[2]')))
        reject_cookies.click()

        click_description = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="expand"]')))
        click_description.click()

        video_name = self.driver.find_element(By.XPATH, '//*[@id="title"]/h1/yt-formatted-string')
        data.append(video_name)

        raw_extracted_data = self.driver.find_element(By.XPATH, '//*[@id="info"]/span[1]')
        extracted_data = raw_extracted_data.text
        date_pattern = r"\d{1,2} \w{3} \d{4}"

        if re.match(date_pattern, extracted_data):
            raw_view_count = self.driver.find_element(By.XPATH, '//*[@id="view-count"]')
            view_count = raw_view_count.get_attribute("aria-label")
            data.append(view_count)
        else:
            view_count = extracted_data
            data.append(view_count)

        return data

    def close(self):
        self.driver.quit()
