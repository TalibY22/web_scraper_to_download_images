from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

PATH = "C:\\Users\\Diag\\Documents\\selenium\\chromedriver_win32\\chromedriver.exe"


#function to get images from google
def img_from_google(path,wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)
    # code to enable the person to search on google
    search_url = "https://www.google.com/search?safe=off&site=&tbm=isch&source=hp&q={q}&oq={q}&gs_l=img"
    wd.get(search_url.format(q=path))


    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                max_images += 1




            images = wd.find_elements_by_css_selector('img.n3VNCb')

            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")
                    break


        if len(image_urls) == max_images:
                     wd.quit()

        return image_urls

#Function to download images
def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file).convert('RGB')
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)




path = input("what pictures do u want")
max_images = int(input("how many pics u want"))
wd = webdriver.Chrome(PATH)

urls = img_from_google(path,wd, 1, max_images)

for i, url in enumerate(urls):
    download_image("C:\\Users\\Diag\\Documents\\tet\\New folder", url, str(i) + ".jpg")
# quit when the downloads are complete
wd.quit()
