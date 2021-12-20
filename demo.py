from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

s = Service('/home/the-techie/Desktop/chromedriver')

options = webdriver.ChromeOptions()
options.add_argument("--disable-web-security")
driver = webdriver.Chrome(service=s, options=options)

try:
	driver.get("chrome://dino/")
except:
	pass

# driver.maximize_window()
print(driver.title)	
scores = []

for i in range(10):

	driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_UP)
	WebDriverWait(driver, 1)

	isPlaying = True

	while isPlaying:
		driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_UP)
		isPlaying = driver.execute_script("return Runner.instance_.playing")

	score = driver.execute_script("return Runner.instance_.distanceMeter.digits")
	# 0000344 = ['0', '0', '0', '3', '4'] => '00034' => 34
	score = int(''.join(score))

	print("score:\t", score)
	scores.append(score)

	driver.execute_script("Runner.instance_.restart()")

print("all scores:\t", scores)
	