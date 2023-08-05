# Copyright (C) 2021 Shubhendra Kushwaha
# @TheShubhendra shubhendrakushwaha94@gmail.com
import re
import json
from requests import get


def get_profile_page(username):
    url = f"https://www.quora.com/profile/{username}"
    res = get(url).text
    return res


def parse_page(html_data):
    data = re.findall(
        r'window\.ansFrontendGlobals\.data\.inlineQueryResults\.results\[".*?"\] = ("{.*}");',
        html_data,
    )[-1]
    data = json.loads(json.loads(data))
    return data["data"]["user"]
