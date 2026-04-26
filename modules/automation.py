import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def search_google(query):
    """
    Automates a Google search and extracts the text from the top results.
    """
    options = uc.ChromeOptions()
    
    # Optional: Runs in the background to avoid a popup window.
    # options.add_argument('--headless') 
    
    # These flags improve stability on Windows
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = None
    try:
        # use_subprocess=True prevents "Zombie" processes on Windows
        driver = uc.Chrome(options=options, use_subprocess=True)
        
        # Navigate to Google
        driver.get(f"https://www.google.com/search?q={query}")
        
        # Wait up to 5 seconds for the search results container to appear
        wait = WebDriverWait(driver, 5)
        results_container = wait.until(EC.presence_of_element_located((By.ID, "rso")))
        
        # Extract all visible text from the results section
        search_data = results_container.text
        
        # Give the driver a moment to finish its background tasks
        time.sleep(1)
        
        return search_data if search_data else "No specific data found in archives."

    except Exception as e:
        print(f"Automation System Error: {e}")
        return f"Error during data retrieval: {str(e)}"

    finally:
        # Ensure the driver handle is released properly
        if driver:
            try:
                driver.quit()
            except Exception:
                # Catch rare handle errors during shutdown
                pass 

def play_youtube(song_name):
    """
    Opens YouTube and searches for the requested track.
    """
    options = uc.ChromeOptions()
    # For YouTube, we usually want to see the browser
    options.add_experimental_option("detach", True) 

    try:
        driver = uc.Chrome(options=options, use_subprocess=True)
        driver.get(f"https://www.youtube.com/results?search_query={song_name}")
        
        # Wait for the results to load
        time.sleep(2)
        
        # Click the first video result
        video = driver.find_element(By.CSS_SELECTOR, "ytd-video-renderer a#video-title")
        video.click()
        
    except Exception as e:
        print(f"YouTube Automation Error: {e}")