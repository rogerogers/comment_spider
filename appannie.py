import requests
import pandas as pd
from time import sleep


def parse_cookie_str():
    cookie_str = 'csrftoken=GJLeeGehKKx6XjFQxK9sqHsOgpDcyHl7; _gcl_au=1.1.252195049.1562724702; _ga=GA1.2.125688435.1562724702; _gid=GA1.2.1517012199.1562724702; _mkto_trk=id:071-QED-284&token:_mch-appannie.com-1562724702481-88033; _hp2_ses_props.3646280627=%7B%22r%22%3A%22https%3A%2F%2Fwww.appannie.com%2Fapps%2Fios%2Fapp%2F1094194042%2Freviews%2F%3Forder_by%3Ddate%26order_type%3Ddesc%26date%3D2019-06-07~2019-07-07%26translate_selected%3Dfalse%26granularity%3Dyearly%26stack%26percent%3Dfalse%26series%3Drating_star_1%2Crating_star_2%2Crating_star_3%2Crating_star_4%2Crating_star_5%22%2C%22ts%22%3A1562724703040%2C%22d%22%3A%22www.appannie.com%22%2C%22h%22%3A%22%2Faccount%2Flogin%2F%22%7D; aa_language=cn; django_language=zh-cn; rid=d1b03e3f98ce4919a4f9863447d8148a; aa_user_token=".eJxrYKotZNQI5SxNLqmIz0gszihkClUwSDM1STYzMkg0MDZLsUhLNkw1N0xLtEizTEoxNLA0TQkVik8sLcmILy1OLYpPSkzOTs1LKWQONShPTUrMS8ypLMlMLtZLTE7OL80r0XNOLE71zCtOzSvOLMksS_XNT0nNcYLqYQnlRTIpM6WQ1UvthiRDqR4A0IMz7A:1hl26K:LG2lbFdiGME7L5i6erRJJmYx5eg"; sessionId=".eJxNjc1Kw0AURmusViLxdyVuXIluQowN6tautLgp3vVwZ-amHRonTe4dpYLgSugbuvcVfAApVHF3-OCc7z16a9bOYJ-J2dV-Ri07FvKygGS1KRZsZdiBrQr9OOCYIDIeEoVBJiowtcrZ-9PPow7s_irkUVdkhxF0kZ2Fk6LIdKaxuCyt7Ze51raf5zdXhdY5ZuX1BWxLzSrMLArZJlrAwb-8RjMlbyF7IY0eq7k4wykaUwcv6QCZ7jyTZyfumR5qS9XtytjDilpRZkJmqsQ9kVkeLCH-g2Yd4t5XL452jpPvQzOby2us4HEQN93zUbPxMWo2Q_oD9fdngw:1hl27o:8J6MiMY6lBQDKxy_odPf_gs7RE4"; _hp2_id.3646280627=%7B%22userId%22%3A%228385806302765741%22%2C%22pageviewId%22%3A%228137437344690636%22%2C%22sessionId%22%3A%221662842836051844%22%2C%22identity%22%3A%221693734%22%2C%22trackerVersion%22%3A%224.0%22%2C%22identityField%22%3Anull%2C%22isIdentified%22%3A1%7D'

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
