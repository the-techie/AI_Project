import numpy as np
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# to store the scores for all episodes
scores = []

# q_table
q_table = dict()
reward = 15

# penalty
out = -1000
learning_rate = 0.1
discount = 0.99
episodes = 20
driver = None

def initialize():

	f = open("q_table.json")
	q_table = json.load(f)
	f.close()

	# selenium.webdriver module provides all the WebDriver implementations
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

# 0: Nothing
# 1: JUMP
# 2: DUCK

# function to take action based on the choice
def performAction(choice):
	if choice == 1:
		driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_UP)
	elif choice == 2:
		driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ARROW_DOWN)


# function to return the current state of dino
def getState():

	# x and y position of dino
	x_pos = "0"
	y_pos = "0"

	# to store the x, y positions and width of first obstacle(if any)
	obs_pos = ""
	curr_speed = float(driver.execute_script("return Runner.instance_.currentSpeed"))

	# discretizing the speed of dino
	if curr_speed - (int)(curr_speed) >= 0.5:
		curr_speed = int(curr_speed) + 0.5
	else:
		curr_speed = int(curr_speed)

	# curr_speed = round(curr_speed, 1)

	# getting x and y position of dino
	x_pos = str(driver.execute_script("return Runner.instance_.tRex.xPos"))
	y_pos = str(driver.execute_script("return Runner.instance_.tRex.yPos"))

	# checking whether the dino is jumping currently or not
	isJumping = str(driver.execute_script("return Runner.instance_.tRex.jumping"))

	# to store how many obstacles are currently on screen
	num_obstacles = int(driver.execute_script("return Runner.instance_.horizon.obstacles.length"))

	# if there's at least one obstacle on screen
	if num_obstacles > 0:
		a = min(150, driver.execute_script("return Runner.instance_.horizon.obstacles[0].xPos")//3)
		b = driver.execute_script("return Runner.instance_.horizon.obstacles[0].yPos")//2
		width = driver.execute_script("return Runner.instance_.horizon.obstacles[0].width")

		obs_pos = str(a) + " " + str(b) + " " + str(width)


	# current state
	res = x_pos + " " + y_pos + " " + isJumping + " " + str(curr_speed) + " " + obs_pos

	# print("res:\t", res)

	return res

# function to restart the game
def restart():
	driver.execute_script("Runner.instance_.restart()")

# method that start the game
# executed when we are executing script initially
def startGame():
	driver.find_element(By.TAG_NAME, "body").send_keys(Keys.SPACE)

# function to add new state to q_table
def addNewState(state):
	q_table[state] = list(np.round(np.random.rand(3), decimals = 2))

# function to return the q_values for the given state
def getQvalues(curr_state):
	try:
		p = q_table[curr_state]

	except:
		addNewState(curr_state)
		p = q_table[curr_state]

	return p

# main method

if __name__ == '__main__':

	driver = initialize()
	startGame()

	for i in range(episodes):
		WebDriverWait(driver, 1)

		isPlaying = True
		x_pos = 1000 
		y_pos = 1000
		width = 20
		dist = 100
		curr_state = getState()

		score = driver.execute_script("return Runner.instance_.distanceMeter.digits")
		score = int(''.join(score))

		while score < 35:
			score = driver.execute_script("return Runner.instance_.distanceMeter.digits")
			score = int(''.join(score))


		while isPlaying:

			# getting q_values for current state
			p = getQvalues(curr_state)

			# taking action based on the action with highest q_values
			action = np.argmax(p)

			performAction(action)
			isJumping = driver.execute_script("return Runner.instance_.tRex.jumping")

			while isJumping and isPlaying:
				isJumping = driver.execute_script("return Runner.instance_.tRex.jumping")
				isPlaying = driver.execute_script("return Runner.instance_.playing")


			# after taking action, checking whether dino is still running
			isPlaying = driver.execute_script("return Runner.instance_.playing")

			# if alive reward
			if isPlaying:
				reward = 15

			# else penalty
			else:
				reward = -1000

			# updating the q_values for current [state][action]

			# q_value of action taken
			current_qsa = p[action]

			# getting the state dino is in after taking action
			next_state = getState()
			next_state_qs = getQvalues(next_state)

			max_future_q = np.max(next_state_qs)

			# calculating new q_value for [curr_state][action]

			new_q = (1 - learning_rate ) * current_qsa + learning_rate * (reward + discount * max_future_q)

			p[action] = round(new_q, 2)

			q_table[curr_state] = p

			curr_state = next_state


		score = driver.execute_script("return Runner.instance_.distanceMeter.digits")
		score = int(''.join(score))

		print("score:\t", score)
		scores.append(score)

		restart()

	driver.close()

	f = open("q_table.json", "w")
	json.dump(q_table, f)
	f.close()
