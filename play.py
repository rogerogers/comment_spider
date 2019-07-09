from selenium import webdriver
import pandas as pd
from time import sleep


def collect():

    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(
        "https://play.google.com/store/apps/details?id=com.mumzworld.android&showAllReviews=true"
    )

    start = 0

    data = []

    i = 0
    while len(data) < 500:
        comment_blocks = get_comment_blocks(browser, i)
        len_before = len(data)
        data.extend(comment_blocks[0])
        len_after  = len(data)
        if len_before == len_after:
            break
        print(len(data))
        i = comment_blocks[1]
        get_next_page(browser)
        sleep(2)
    df = pd.DataFrame(data)
    df.to_excel("/home/rogers/mumzworld.xls", index=False)


def get_comment_blocks(browser, begin=0):

    comment_blocks = browser.find_elements_by_css_selector(
        'div[jscontroller="H6eOGe"]>div.zc7KVe'
    )

    data = []

    for comment_block in comment_blocks[begin:]:

        rate = get_rate(comment_block)

        if rate >= 4:

            dataItem = {
                "username": get_username(comment_block),
                "content": get_content(comment_block),
                "rate": get_rate(comment_block),
            }
            data.append(dataItem)
    print(len(comment_blocks))
    return data, len(comment_blocks)


def get_rate(comment_block):
    rate = comment_block.find_elements_by_class_name("vQHuPe")
    return len(rate)


def get_content(comment_block):
    content = comment_block.find_element_by_css_selector(
        'span[jsname="bN97Pc"]'
    ).text.strip()
    try:
        button = comment_block.find_element_by_css_selector('button.LkLjZd.ScJHi.OzU4dc')
        button.click()
    except Exception as e:
        pass
    full_content = comment_block.find_element_by_css_selector('span[jsname="fbQN7e"]').text.strip()
    if len(full_content) > 0:
        content = full_content
    return content


def get_username(comment_block):
    title = comment_block.find_element_by_class_name("X43Kjb")
    return title.text.strip()


def get_next_page(browser):
    try:

        next_button = browser.find_element_by_css_selector("span.RveJvd.snByac")
        next_button.click()
    except Exception as e:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")


if __name__ == "__main__":
    collect()
