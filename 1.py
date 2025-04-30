import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO

# === Configuration ===
CHROMEDRIVER_PATH = r"D:\chromedriver-win64\chromedriver.exe"
SAVE_DIR = r"C:\Users\vaibh\Desktop\Work\stress\Collecting_dataset\savenewimg"  # Updated folder name
EMOTION = "proud"
NUM_IMAGES = 5000

# === Emotion-specific and extra queries ===
search_queries = [
    "proud human face", "confident and proud expression", "smiling proudly photo",
    "person feeling accomplished", "victorious expression", "self-satisfied look",
    "prideful gaze", "person with a proud posture", "proud and confident face photo",
    "radiating pride expression"
]

# === Setup headless Chrome browser ===
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)

def download_image(url, folder, index):
    try:
        img_data = requests.get(url, timeout=10).content
        img = Image.open(BytesIO(img_data)).convert("RGB")
        filename = os.path.join(folder, f"{index}.jpg")
        img.save(filename)
        return True
    except Exception as e:
        return False

def try_click_show_more():
    try:
        button = driver.find_element(By.CLASS_NAME, "btn_seemore")
        if button.is_displayed():
            button.click()
            time.sleep(2)
    except:
        pass

def collect_image_urls(query, collected, target):
    print(f"\n🔎 Query: {query}")
    driver.get(f"https://www.bing.com/images/search?q={query}&form=HDRSC2&first=1&tsc=ImageHoverTitle")
    time.sleep(2)
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(collected) < target:
        thumbnails = driver.find_elements(By.CLASS_NAME, "mimg")
        for img in thumbnails:
            try:
                src = img.get_attribute("src") or img.get_attribute("data-src")
                if src and src.startswith("http") and src not in collected:
                    collected.add(src)
                    if len(collected) >= target:
                        break
            except:
                continue
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try_click_show_more()
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    print(f"🧠 Collected {len(collected)} image URLs so far...")

def scrape_emotion_images(emotion, queries, target_count):
    print(f"\n🔍 Scraping images for: {emotion}")
    
    # Ensure the base directory exists before creating emotion folder
    base_folder = os.path.join(SAVE_DIR, emotion)
    
    # Create the directory if it does not exist
    os.makedirs(base_folder, exist_ok=True)
    
    image_urls = set()
    success_count = 0

    for query in queries:
        if len(image_urls) >= target_count:
            break
        collect_image_urls(query, image_urls, target_count)

    print(f"\n✅ Total collected URLs for {emotion}: {len(image_urls)}")
    print("⬇️ Starting download...")

    for idx, url in enumerate(image_urls):
        if download_image(url, base_folder, idx):
            success_count += 1
        if success_count >= target_count:
            break

    print(f"\n✅ Download complete: {success_count}/{target_count} images saved to '{base_folder}'")

# === MAIN ===
if __name__ == "__main__":
    scrape_emotion_images(EMOTION, search_queries, NUM_IMAGES)
    driver.quit()
    print("\n🎉 All tasks finished successfully!")
