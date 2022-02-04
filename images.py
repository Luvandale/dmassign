# Install
# 1. Pillow
# 2. selenium - automate browser
# 3. requests
from selenium import webdriver # Chrome webdriver
from selenium.webdriver.common.by import By
import requests
import io
from PIL import Image
import time

# webdriver local path
PATH = "C:\\Users\\Joyce\\Documents\\Clustering images\\chromedriver.exe"
wd = webdriver.Chrome(PATH)

def get_images_from_google(wd, delay, max_images):
	def scroll_down(wd):
		wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(delay)

    # link to google product images
	url = "https://www.google.com/search?q=product+images&rlz=1C1CHBF_enRW948RW948&sxsrf=APq-WBtjXlwozq_qyMv3Q7nBCRZzJBxglQ:1643713422041&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj3jojVrd71AhVwMewKHQ9YB70Q_AUoAXoECAEQAw&biw=762&bih=738&dpr=1.25"
	wd.get(url)

	image_urls = set()
	skips = 0

	while len(image_urls) + skips < max_images:
		scroll_down(wd)

        # find all elements with classname ...
		thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

		for img in thumbnails[len(image_urls) + skips:max_images]:
			try:
				img.click()
				time.sleep(delay)
			except:
				continue
            
            # find specific image with classname ...
			images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
			for image in images:
				if image.get_attribute('src') in image_urls:
					max_images += 1
					skips += 1
					break

				if image.get_attribute('src') and 'http' in image.get_attribute('src'):
					image_urls.add(image.get_attribute('src'))
					print(f"Found {len(image_urls)}")

	return image_urls


def download_image(download_path, url, file_name):
	try:
		image_content = requests.get(url).content
		image_file = io.BytesIO(image_content)
		image = Image.open(image_file)
		file_path = download_path + file_name

		with open(file_path, "wb") as f:
			image.save(f, "JPEG")

		print("Success")
	except Exception as e:
		print('FAILED -', e)

urls = get_images_from_google(wd, 1, 100)

for i, url in enumerate(urls):
	download_image("images/", url, str(i) + ".jpg")

wd.quit()

