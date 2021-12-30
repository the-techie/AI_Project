import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


scores = []
q_table = dict()
reward = 15
out = -1000
learning_rate = 0.4
discount = 0.5
episodes = 20000
driver = None

f = open("log.txt", "w")


def performAction(choice):
	if choice == 1:
		driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_UP)
	elif choice == 2:
		driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_DOWN)


# def getDiscreteState(current_values):
# 	res = []
# 	for i in current_values:
# 		res.append((i[0]//10, i[1]//4, i[2]//10))
# 	return tuple(res)


def getState():
	x_pos = 0
	y_pos = 0
	obs_pos = []
	curr_speed = float(driver.execute_script("return Runner.instance_.currentSpeed"))

	if round(curr_speed % 1, 1) >= 0.5:
		curr_speed = int(curr_speed) + 0.5
	else:
		curr_speed = float(int(curr_speed))

	x_pos = driver.execute_script("return Runner.instance_.tRex.xPos")
	y_pos = driver.execute_script("return Runner.instance_.tRex.yPos")


	# wait until first obstacle is on the screen
	# if the dino gets out during down phase of jumping and towards the end of obstacle, then punishment should be less

	num_obstacles = int(driver.execute_script("return Runner.instance_.horizon.obstacles.length"))
	if num_obstacles > 0:
		a = min(20, driver.execute_script("return Runner.instance_.horizon.obstacles[0].xPos")//10)
		b = driver.execute_script("return Runner.instance_.horizon.obstacles[0].yPos")//5
		width = driver.execute_script("return Runner.instance_.horizon.obstacles[0].width")//10

		obs_pos.append((a, b, width))

	# new_pos = tuple(obs_pos)

	res = tuple([x_pos, y_pos, round(curr_speed, 1)] + obs_pos)

	# print("state:\t", res)

	return res


def restart():
	driver.execute_script("Runner.instance_.restart()")


def startGame():
	driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)


def initialize():
	s = Service('/home/the-techie/Desktop/chromedriver')

	options = webdriver.ChromeOptions()
	options.add_argument("--disable-web-security")
	driver = webdriver.Chrome(service=s, options=options)
	# driver.maximize_window()

	try:
		driver.get("chrome://dino/")
	except:
		pass

	return driver


def addNewState(state):
	q_table[state] = np.round(np.random.rand(3), decimals = 2)

def writeToFile():
	for i in q_table.keys():
		f.write((str(i) + ":\t" + str(q_table[i]) + "\n"))

def showtable():
	for i in q_table.keys():
		print(i, ":\t", q_table[i])

if __name__ == '__main__':

	f = open("log.txt", "w")
	driver = initialize()
	startGame()


	# base_speed = float(driver.execute_script("return Runner.instance_.currentSpeed"))

	for i in range(episodes):
		f = open("log.txt", "w")
		WebDriverWait(driver, 1)

		isPlaying = True
		x_pos = 1000 
		y_pos = 1000
		width = 20
		dist = 100
		

		curr_state = getState()

		# print("q_table:\t", showtable())

		score = driver.execute_script("return Runner.instance_.distanceMeter.digits")
		score = int(''.join(score))

		while score < 35:
			score = driver.execute_script("return Runner.instance_.distanceMeter.digits")
			score = int(''.join(score))


		while isPlaying:

			# print("inside q_table:\t", showtable())

			obs_pos = []
			p = None

			try:
				p = q_table[curr_state]
				# print("curr_state:\t", curr_state)
				# print("Inside 1st try:\np:\t", p)

			except:
				addNewState(curr_state)
				p = q_table[curr_state]

			action = np.argmax(p)

			# print("Before p:\t", p)

			performAction(action)
			# updating *******************************
			isPlaying = driver.execute_script("return Runner.instance_.playing")

			if isPlaying:
				reward = 15

			else:
				reward = -1000

			current_qsa = p[action]
			next_state = getState()
			next_state_qs = None

			try:
				next_state_qs = q_table[next_state]
				# print("Inside 2nd try:\nnext_state_qs:\t", next_state_qs)

			except:
				addNewState(next_state)
				next_state_qs = q_table[next_state]
				# print("Inside 2nd except:\nnext_state_qs:\t", next_state_qs)

			max_future_q = np.max(next_state_qs)

			new_q = (1 - learning_rate ) * current_qsa + learning_rate * (reward + discount * max_future_q)

			# print("p:\t", p)
			# print("new_q:\t", new_q)

			p[action] = new_q

			# print("After p:\t", p)

			q_table[curr_state] = p

			curr_state = next_state


		score = driver.execute_script("return Runner.instance_.distanceMeter.digits")
		score = int(''.join(score))

		writeToFile()
		f.close()

		print("score:\t", score)
		scores.append(score)

		restart()

	f.write(str(scores))

	driver.close()