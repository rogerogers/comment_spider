import requests
import pandas as pd
from time import sleep


def parse_cookie_str():
    cookie_str = ''

    return {
        item[0]: item[1]
        for item in [
            key_value.strip().split("=") for key_value in cookie_str.split(";")
        ]
    }


def make_request():
    cookies = parse_cookie_str()
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "accept-encoding": "gzip, deflate, br",
        "referer": "https://www.appannie.com/apps/ios/app/1212024125/reviews/?order_by=rating&order_type=desc&date=2018-07-10~2019-07-09&translate_selected=false&granularity=monthly&stack&percent=false&series=rating_star_1,rating_star_2,rating_star_3,rating_star_4,rating_star_5",
        "x-requested-with": "XMLHttpRequest",
    }
    data = []
    for i in range(51):
        print("page", i)
        url = "https://www.appannie.com/apps/ios/app/1094194042/reviews/table/?order_by=rating&order_type=desc&&interval=10&translate_lang=&start_date=2018-07-11&end_date=2019-07-10"
        url = url + "&page=" + str(i)
        res = requests.get(url, cookies=cookies, headers=headers)
        print(res)
        json_res = res.json()
        for row in json_res["data"]["table"]["rows"]:
            rate = row[0][0]
            if rate < 4:
                return data
            content = row[1][0]
            user = row[1][1]
            print(row)
            data.append({"rate": rate, "content": content, "user": user})
        sleep(5)
    return data


if __name__ == "__main__":
    data = make_request()
    df = pd.DataFrame(data)
    df.to_excel("/home/rogers/Documents/mumzworld.xls", index=False)
