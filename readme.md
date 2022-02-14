# **Dino game playing using Q-learning**
This project uses the Q-learning algorithm of reinforcement learning to teach the computer to play the dino game built into most chromium browsers.

## Motivation
We did this project for our MCSC 102: Artificial Intelligence course taught by Dr. Punam Bedi. We chose this particular topic because it was a little intuitive and can be built easily from scatch.

## Requirements(Prerequisites)
For our project we used python as our choice of programming language. We used the following python packages:
  - numpy
  - json
  - selenium
  - matplotlib

Along with that we used chromedriver for our Chrome browser to interact with it.

## Installation
### 1. Install the required packages using `pip install package_name`
```
pip install numpy
pip install matplotlib
pip install selenium
```
`json` is a built-in module, hence `pip install` is not required for it

### 2. Download the correct chromedriver(based on your browser version)
  1. Open your chrome browser
  2. Click on 3 vertical buttons in top right corner
  3. Go to help > About Google Chrome

OR
  1. type `chrome://version/` in your browser and check the browser version.

### 3. Go to [chromedriver download link](https://chromedriver.chromium.org/downloads) and download the correct drivers for your browser.

### 4. Extract the driver from the downloaded zip file and paste it to the folder containing code files.
>:warning: If you are windows user then you might have to turn off your windows firewall and any third-party antivirus installed in your system, in order for this code to work correctly.


# **Problems faced**

* ### As this is an endless runner game, there are infinitely many number of possible states, and it's impossible to learn infinitely many `state: action` pairs.
  * #### Our solution:
  #### We discretized the states, hence decreasing the number of possible states.


* ### Not all possible states occured during learning
  * #### Our Solution:
  #### We made our program to learn in batches i.e. we executed it for a number of episodes then paused the learning, then resuming it again.


* ### Learning process is very time consuming
  * #### Our Solution:
  #### Training in batches helped us with the learning process.

> ### Our solution to these problems are not full proof, but reduces the extent of problems.

## Credits
* #### [Medium article on dino game playing using AI](https://medium.com/acing-ai/how-i-build-an-ai-to-play-dino-run-e37f37bdf153)

* #### [towardsdatascience article on Q-learning](https://towardsdatascience.com/simple-reinforcement-learning-q-learning-fcddc4b6fe56)

* #### [towardsdatascience article on Q-learning](https://towardsdatascience.com/a-beginners-guide-to-q-learning-c3e2a30a653c)

* #### [towardsdatascience article on maths behind Q-learning](https://towardsdatascience.com/math-behind-reinforcement-learning-the-easy-way-1b7ed0c030f4)
