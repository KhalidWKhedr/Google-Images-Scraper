import base64
import io
import os
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from PIL import Image

class GoogleImages:

    def __init__(self):

        self.user_input = input("What images do you want? ")
        self.user_args = re.sub('[()!@#$,\']', "", self.user_input)
        self.finished_args = self.user_args.replace(' ', '+' )
        self.chrome_url = f"https://images.google.com/search?q={self.finished_args}z"


        # Chrome Options
        self.chrome_options = Options()
        self.chrome_options.binary_location = '/home/khalidwaleedkhedr/Projects/PycharmProjects/WebScraping/chrome-linux64/chrome'
        self.chrome_options.add_argument("--headless")  # Optional: run Chrome in headless mode
        self.chrome_options.add_argument("--no-sandbox")  # Required for some environments
        self.chrome_options.add_argument("--disable-dev-shm-usage")  # Required for some environments

        # ChromeDriver from npm
        self.chrome_driver = Service('/home/khalidwaleedkhedr/chromedriver/linux-128.0.6613.119/chromedriver-linux64/chromedriver')

        # Create WebDriver instance with the configured options
        self.web_driver = webdriver.Chrome(service=self.chrome_driver, options=self.chrome_options)

        # Open the URL
        self.web_driver.get(self.chrome_url)


        # Fetch image elements
        self.images = self.web_driver.find_elements(By.TAG_NAME, 'img')
        self.url_list = []

    # Check if url is valid
    def check_url(self):
        print(self.chrome_url)




    # Get images from <src> and terminate chromedriver
    def get_links(self):
        for image in self.images:
            url = image.get_attribute('src')
            self.url_list.append(url)
            print(self.url_list)
        self.web_driver.quit()

    # Save images by type
    def save_images(self):

        dir_name = self.user_input
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        image_counter = 0
        for url in self.url_list:
            if url is not None:
                try:
                    if url.startswith('http'):
                        url_image = url
                        print(url_image)

                    elif url.startswith('data:image/jpeg;base64,'):
                        img_data = url.replace('data:image/jpeg;base64,', "")
                        img = Image.open(io.BytesIO(base64.decodebytes(bytes(img_data, "utf-8"))))
                        img.save(os.path.join(dir_name, f'my-image{image_counter}.jpeg'))

                    elif url.startswith('data:image/png;base64,'):
                        img_data_png = url.replace('data:image/png;base64,', "")
                        img = Image.open(io.BytesIO(base64.decodebytes(bytes(img_data_png, "utf-8"))))
                        img.save(os.path.join(dir_name, f'my-image{image_counter}.png'))

                    else:
                        print(f"Process further: {url}")

                except Exception as e:
                    print(f"doesn't work ig, {url}, {e}")

            image_counter = image_counter + 1


get_images = GoogleImages()
get_images.check_url()
get_images.get_links()
get_images.save_images()