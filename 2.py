from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time, os, requests
from PIL import Image
from io import BytesIO

def bing_image_scraper(query, save_dir, num_images=5000):
    # Setup: Create directory to save images
    os.makedirs(save_dir, exist_ok=True)

    # Launch browser
    driver = webdriver.Chrome()
    driver.get("https://www.bing.com/images/")

    # Search for the emotion-related query
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    # Scroll and collect image URLs
    image_urls = set()
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(image_urls) < num_images:
        thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.mimg")
        for thumb in thumbnails[len(image_urls):]:
            try:
                thumb.click()
                time.sleep(1)
                images = driver.find_elements(By.CSS_SELECTOR, "img.nofocus")
                for img in images:
                    src = img.get_attribute("src")
                    if src and "http" in src and src not in image_urls:
                        image_urls.add(src)
                        print(f"[{len(image_urls)}] Collected: {src}")
                        if len(image_urls) >= num_images:
                            break
            except:
                continue

        # Scroll down to load more images
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Downloading images
    print(f"\n📸 Downloading {len(image_urls)} images...")
    for i, url in enumerate(image_urls):
        try:
            response = requests.get(url, timeout=5)
            img = Image.open(BytesIO(response.content))
            img = img.convert("RGB")  # Ensure it's in RGB format
            img.save(os.path.join(save_dir, f"{query.replace(' ', '_')}_{i+1}.jpg"))
        except Exception as e:
            print(f"❌ Failed to download image {i+1}: {e}")

    driver.quit()
    print("✅ Scraping completed!")

