# robo_advisor.py

## Setup

### Repo Setup

Navigate to https://github.com/ebjacoby/Robo-adviser and clone the repository to your desktop.


After cloning the repo (make sure to save it in a directory similar to that shown below), navigate there from the command-line:

```sh
cd ~/Desktop/Github/robo-advisor
```

### Environment Setup

Create and activate a new Anaconda virtual environment:

```sh
conda create -n robo-env python=3.7 # (first time only)
conda activate robo-env
```

From within the virtual environment, install the required packages specified in the "requirements.txt" file, included in the cloned repository:

```sh
pip install -r requirements.txt
```

### API SETUP

Navigate to the url https://www.alphavantage.co/ and "get your free API key". Store the provided key in a .env file (name it ALPHA_VANTAGE_API.env). Ensure that you create a corresponding .gitignore file in the root directory and name the API key in it (ALPHA_VANTAGE_API.env should grey out): otherwise, your private API Key will be visible to the public, if the repository is committed. 

Also, in the command line, enter your env name and the corresponding key in this format: 

```sh
set ALPHA_VANTAGE_API=12123091823090382903  #on the right of the equals sign, here, is a fake/placeholder API key. 
```

You could also load this into a .env file and have it called by writing 'from dotenv import load_dotenv' in your code and then 'load_dotenv()'. If this method does not work, please input environment variables individually, as stated before^.

### run the app

To run the app, type the following into the command line:

```sh
python app/robo_advisor.py
```

The app will request an input for a stock ticker, with specific requirements for input. Following input, the app will run and recommend to buy or not buy based on a cumulative distribution function of day-to-day returns - for the past 100 days. The app will also produce a .csv file, corresponding to the stock ticker chosen, that will be saved in the 'data' folder, found within the root repository. 
