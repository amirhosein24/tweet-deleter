from os import path

from datetime import datetime
from creds import username, password
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


def convert_to_local_time(utc_time):
    utc_dt = datetime.strptime(utc_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    utc_dt = utc_dt.replace(tzinfo=timezone('UTC'))
    local_dt = utc_dt.astimezone(timezone('Asia/Tehran'))
    return local_dt


def run(playwright: Playwright, update, user, scroltime) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()

    with open(home + "cookies/", encoding='utf-8') as file:
        from json import load
        cookies = load(file)["cookies"]

    context.add_cookies(cookies)
    page = context.new_page()
    page.goto(f"https://twitter.com/{user}", timeout=30000)

    scroll, repeat = 500, 0

    for _ in range(scroltime):
        try:
            if "Something went wrong. Try reloading." in page.inner_text('body'):
                update.message.reply_text(
                    f"text found in run-crawl : Something went wrong. Try reloading.\ncookie : {cookie}\nuser : {user}")
                context.close()
                browser.close()
                return

            if "These posts are protected" in page.inner_text('body'):
                update.message.reply_text(f"text found in run-crawl : page is private\n user : {user}")
                context.close()
                browser.close()
                return

            page.wait_for_selector('[data-testid="tweet"]')
            tweets = page.query_selector_all('[data-testid="tweet"]')
            for tweet in tweets:

                tweet_like = tweet.query_selector('[data-testid="like"] span')
                if tweet_like:
                    tweet_like = tweet_like.inner_text()
                else:
                    tweet_like = None



                # tweet_text = tweet.query_selector('[data-testid="tweetText"]')
                # if tweet_text:
                #     tweet_text = tweet_text.inner_text()
                # else:
                #     tweet_text = None
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



            page.evaluate(f"window.scrollTo(0, {scroll})")  # Scroll the page
            scroll += 1300
        except Exception as error:
            update.message.reply_text(f"error in run-crawl, error :\n{str(error)}")
            context.close()
            browser.close()
            return



    # ---------------------
    context.close()
    browser.close()


def get_tweets(update, username, scroltime):
    try:
        with sync_playwright() as playwright:
            run(playwright, update, username, scroltime)
        return True
    except Exception as error:
        update.message.reply_text(f"error in get-tweet, error :\n{str(error)}")
        return False

# while True:
#     get_tweets(None, "garshaspy", 3)
