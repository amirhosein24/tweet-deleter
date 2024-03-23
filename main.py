


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


    if "Something went wrong. Try reloading." in page.inner_text('body'):
        print("text found in main run : Something went wrong. Try reloading.")
        context.close()
        browser.close()
        return

    scroll, repeat, repeatlist = 500, 0, []
    while True:
        try:

            page.wait_for_selector('[data-testid="tweet"]', timeout=2000)
            tweets = page.query_selector_all('[data-testid="tweet"]')

            for tweet in tweets:
                tweet_link = tweet.query_selector('a[href*="/status/"]')
                if tweet_link:
                    tweet_link = tweet_link.get_attribute('href')
                    name = tweet_link.split("/")[1]

                    if name.lower() != username.lower():
                        continue

                    if tweet_link in repeatlist:
                        repeat += 1
                        continue
                    else:
                        repeat = 0
                        repeatlist.append(tweet_link)

                tweet_text = tweet.query_selector('[data-testid="tweetText"]')
                if tweet_text:
                    tweet_text = tweet_text.inner_text()
                else:
                    tweet_text = None

                tweet_like = tweet.query_selector('[data-testid="like"] span')
                if tweet_like:
                    tweet_like = tweet_like.inner_text()

                    try:
                        tweet_like = int(tweet_like)
                    except:
                        if type(tweet_like) == str and tweet_like == "":
                            tweet_like = 0

                    try:
                        if tweet_like < like_limit and tweet_text != None:
                            page.get_by_label(tweet_text).get_by_test_id("caret").click()
                            page.get_by_test_id("Dropdown").get_by_text("Delete").click()
                            page.get_by_test_id("confirmationSheetConfirm").click()
                            time.sleep(0.1)

                    except Exception as error:
                        print("error in deletion: ", str(error))

                # tweet_repost = tweet.query_selector('[data-testid="retweet"] span')
                # if tweet_repost:
                #     tweet_repost = tweet_repost.inner_text()
                # else:
                #     tweet_repost = None
                    
                # tweet_mention = tweet.query_selector('[data-testid="reply"] span')
                # if tweet_mention:
                #     tweet_mention = tweet_mention.inner_text()
                # else:
                #     tweet_mention = None
                # tweet_time = tweet.query_selector('time')

        except Exception as error:
            print(f"error in run-crawl, error :\n{str(error)}")

        page.evaluate(f"window.scrollTo(0, {scroll})")  # Scroll the page
        scroll += 1200

        if repeat > 100:
            time.sleep(5)
            break

    # ---------------------
    context.close()
    browser.close()


if __name__ == "__main__":
        with sync_playwright() as playwright:
            run(playwright)
