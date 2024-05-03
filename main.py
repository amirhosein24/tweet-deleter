from creds import username, password, like_limit

import time
from os import path
from playwright.sync_api import Playwright, sync_playwright

home = path.dirname(path.abspath(__file__)) + "/"

if not path.isfile(home + "cookie.json"):
    def run(playwrighter: Playwright) -> None:
        browser = playwrighter.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://twitter.com/i/flow/login")
        page.get_by_label("Phone, email, or username").fill(username)
        page.get_by_role("button", name="Next").click()
        page.get_by_label("Password", exact=True).fill(password)
        page.get_by_test_id("LoginForm_Login_Button").click()
        page.wait_for_selector("text=For you")
        context.storage_state(path=home + "cookie.json")
        # ---------------------
        context.close()
        browser.close()
    with sync_playwright() as playwright:
        run(playwright)


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    with open(home + "cookie.json", encoding='utf-8') as file:
        from json import load
        cookies = load(file)["cookies"]

    context.add_cookies(cookies)
    page = context.new_page()
    page.goto(f"https://twitter.com/{username}/with_replies")

    scroll = 500
    for _ in range(50):
        page.evaluate(f"window.scrollTo(0, {scroll})")  # Scroll the page
        scroll += 1200
        time.sleep(0.3)

    while True:
        try:
            page.wait_for_selector('[data-testid="tweet"]', timeout=2000)
            tweets = page.query_selector_all('[data-testid="tweet"]')

            for tweet in tweets:

                tweet_link = tweet.query_selector('a[href*="/status/"]')
                if tweet_link:
                    tweet_link = tweet_link.get_attribute('href')
                    name = tweet_link.split("/")[1]

                    if name.lower() == username.lower():

                        tweet_like = tweet.query_selector(
                            '[data-testid="like"] span')
                        if tweet_like:
                            tweet_like = tweet_like.inner_text()
                            if tweet_like == "" or int(tweet_like) < like_limit:

                                try:
                                    page_tweet = context.new_page()
                                    page_tweet.goto(
                                        "https://twitter.com" + tweet_link)

                                    tweet_text = tweet.query_selector(
                                        '[data-testid="tweetText"]')
                                    if tweet_text:
                                        tweet_text = tweet_text.inner_text()
                                    else:
                                        continue

                                    try:

                                        if tweet_text == "":
                                            tweet_text = "گرشاسپـــ@garshaspz"

                                        page_tweet.get_by_label(tweet_text).get_by_test_id(
                                            "caret").last.click()
                                        page_tweet.get_by_test_id(
                                            "Dropdown").get_by_text("Delete").click()
                                        page_tweet.get_by_test_id(
                                            "confirmationSheetConfirm").click()
                                        time.sleep(0.1)

                                    except Exception as error:
                                        print("error in deletion: ", str(error))
                                        pass

                                finally:
                                    page_tweet.close()

            page.evaluate(f"window.scrollTo(0, {scroll})")
            scroll += 2000
            time.sleep(0.5)

        except Exception as error:
            print(f"error in run-crawl, error :\n{str(error)}")

    # ---------------------
    # context.close()
    # browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
