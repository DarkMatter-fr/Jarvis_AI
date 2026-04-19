# modules/automation.py
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def search_google(query):
    options = uc.ChromeOptions()
    # use_subprocess=True prevents the 'Invalid Handle' error on Windows
    driver = uc.Chrome(options=options, use_subprocess=True)
    try:
        driver.get(f"https://www.google.com/search?q={query}")
        wait = WebDriverWait(driver, 15)
        # 2026 selector for the main search content
        result = wait.until(EC.presence_of_element_located((By.ID, "search")))
        return result.text[:3000] # Return text for the Brain to summarize
    except:
        return "Search failed."
    finally:
        driver.quit()

def play_youtube(song):
    driver = uc.Chrome(use_subprocess=True)
    driver.get(f"https://www.youtube.com/results?search_query={song}")
    try:
        wait = WebDriverWait(driver, 15)
        video = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "ytd-video-renderer a#video-title")))
        time.sleep(random.uniform(1, 2))
        video.click()
        return True
    except:
        return False