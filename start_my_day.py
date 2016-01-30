#! /usr/bin/env python
# coding: utf-8

import sys
import os
import requests
import random
from pprint import pprint
from datetime import datetime
import configparser
import json
import shutil

CONFIG_FILE = "./start_my_day.conf"
BAIDU_WEATHER_API = "http://apis.baidu.com/heweather/weather/free"

def load_config(config_file):
    config = configparser.RawConfigParser(allow_no_value=True)
    config.readfp(open(config_file))
    sec_opt2val = {}
    for section in config.sections():
        sec_opt2val[section] = {}
        for option in config.options(section):
            sec_opt2val[section][option] = config.get(section,option)
    return sec_opt2val

def load_template(conf):
    template_file = conf["base_config"]["diary_template"]
    temp_block = []
    handle = open(template_file)
    line = handle.readline()
    while line:
        if line.startswith("<!--"):
            while "-->" not in line:
                line = handle.readline()
            line = handle.readline()
            continue
        temp_block.append(line)
        line = handle.readline()
    return "".join(temp_block)

def get_date_today(conf):
    time_str = conf["formatter"]["date_today"]
    # time_str = "{0:%Y}年{0:%m}月{0:%d}日 {0:%H}时{0:%M}分"
    return time_str.format(datetime.today())

def get_today_habit(conf):
    habit_list = conf["habit_list"].keys()
    habit_count = 1
    return "\n".join(["+ %s"%(s) for s in 
        random.sample(habit_list,habit_count)])

def days_matter_reminder(conf):
    days_matter_block = []
    for day in conf["days_matter"].keys():
        days_matter_block.append({"day":day,"event":conf["days_matter"][day]})
    return days_matter_block

def get_reminder_today(conf):
    days_matter = days_matter_reminder(conf)
    return "day"

def get_book_to_read(conf):
    book_list = conf["book_list"].keys()
    book_count = 1
    book_today = [s for s in random.sample(book_list,book_count)]
    note_template = conf["base_config"]["note_template"]
    for book in book_today:
        note_target = "%s/笔记_%s_%s.mkd"%(conf["base_config"]["diary_path"],
            book,datetime.today().strftime("%Y%m%d"))
        # copy template file
        shutil.copyfile(note_template,note_target)
    return "\n".join(["+ 「%s」"%(s) for s in book_today])

def get_questions(conf):
    questions_list = conf["questions_list"].keys()
    questions_count = min(len(questions_list),
            int(conf["base_config"]["questions_per_day"]))
    return "\n\n".join(["+ %s"%(s) for s in 
        random.sample(questions_list,questions_count)])

def get_whether(conf):
    api_key = open(conf["base_config"]["baidu_api_key"]).read().strip()
    city = conf["base_config"]["city"]
    api_url = "%s?city=%s"%(BAIDU_WEATHER_API,city)
    r = requests.get(api_url, headers={"apikey":api_key})
    content = json.loads(r.text)
    a = content["HeWeather data service 3.0"][0]
    if not a["status"] == u"ok":
        return "weather api down"

    tmp_data = {
        "temp_range": "%s ℃ - %s ℃"%(a["daily_forecast"][0]["tmp"]["min"],
            a["daily_forecast"][0]["tmp"]["max"]),
        "rain_percent": "\n".join(["    + %s: %s %%"%(rp["date"].split(" ")[1],rp["pop"]) for
            rp in a["hourly_forecast"]]),
        "air_quality": a["aqi"]["city"]["qlty"],
        "aqi": a["aqi"]["city"]["aqi"],
        "pm25": a["aqi"]["city"]["pm25"],
        }

    whether_string = \
"""+ 温差：{temp_range}
+ 空气质量：{air_quality}
    + AQI: {aqi}
    + PM2.5: {pm25}
+ 下雨概率：
{rain_percent}""".format(**tmp_data)
   
    return whether_string

def date2weekday(date_str):
    return datetime.strptime(date_str,"%Y-%m-%d").strftime("%A")

def date2datetime(date_str):
    return datetime.strptime(date_str,"%Y-%m-%d")

def main(config_file):
    conf = load_config(config_file)
    template_string = load_template(conf)
    data = {"date_today":get_date_today(conf),
            "habit_today":get_today_habit(conf),
            "reminder_today":get_reminder_today(conf),
            "book_to_read_today":get_book_to_read(conf),
            "questions_today":get_questions(conf),
            "whether_today":get_whether(conf)
            }
    print(template_string.format(**data))

if __name__ == "__main__":
    main(CONFIG_FILE)
