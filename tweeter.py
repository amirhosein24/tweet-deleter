
from creds import username, password

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

maintext = ".."

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    with open(home + "cookie.json", encoding='utf-8') as file:
        from json import load
        cookies = load(file)["cookies"]

    context.add_cookies(cookies)
    page = context.new_page()
    page.goto(f"https://twitter.com/", timeout=60000)


    # if "Something went wrong. Try reloading." in page.inner_text('body'):
    #     print("text found in main run : Something went wrong. Try reloading.")
    #     context.close()
    #     browser.close()
    #     return

    scroll, times = 500, 5
    for _ in range(times):
        try:
            page.wait_for_selector('[data-testid="tweet"]', timeout=2000)
            tweets = page.query_selector_all('[data-testid="tweet"]')

            for tweet in tweets:
                tweet_link = tweet.query_selector('a[href*="/status/"]')
                if tweet_link:
                    tweet_link = "https://twitter.com" + tweet_link.get_attribute('href')
                    page_reply = context.new_page()
                    page_reply.goto(tweet_link)
                    time.sleep(2.5)

                    try:
                        page_reply.get_by_test_id("reply").first.click()
                        page_reply.get_by_role("textbox", name="Post text").fill(maintext)
                        page_reply.get_by_test_id("tweetButton").click()
                        time.sleep(0.5)
                    except Exception as e:
                        print(e)
                    page_reply.close()
                    input("------------------")

        except Exception as error:
            print(f"error in run-crawl, error :\n{str(error)}")

        page.evaluate(f"window.scrollTo(0, {scroll})")  # Scroll the page
        scroll += 2500

    # ---------------------
    context.close()
    browser.close()

if __name__ == "__main__":
        with sync_playwright() as playwright:
            run(playwright)