
# Tweet deletor


This code is a simple bot that uses the Playwright library to automate Twitter actions. The bot logs into a Twitter account using provided credentials, saves the cookies for future use, and deletes tweets with like counts below a specified limit.

Requirements
------------

* Python 3.x
* Playwright library

Installation
------------

1. Install Playwright library using pip:
```
pip install playwright
```
2. Install the required browser (Chromium, in this case) using Playwright CLI:
```lua
playwright install chromium
```
Usage
-----

1. Create a `creds.py` file in the same directory as the script with the following variables:
```python
username = "your_twitter_username"
password = "your_twitter_password"
like_limit = 10  # or any other number as your preference
```
2. Run the script:
```bash
python twitter_bot.py
```
Features
--------

* Logs into a Twitter account using the provided credentials in `creds.py`.
* Saves the cookies after a successful login for future use.
* Loads the cookies from the saved file for subsequent runs.
* Navigates to the user's profile with replies.
* Scrolls through the tweets and deletes those with like counts below the specified limit.

Note
----

- the bot might not be able to delete all the tweets below specified like count on the first try, so rerun the bot just in case

- the bot is not running in headless mode. If you dont want to see the bot in action, change `headless=False` to `headless=True` when running the code.

Disclaimer
----------

This bot is intended for educational purposes only. Automating Twitter actions may violate Twitter's Terms of Service. Use this code responsibly and at your own risk. I am not responsible for any misuse of this code or any consequences that may arise from its use.