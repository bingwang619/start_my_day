#! /usr/bin/env python
# coding: utf-8

import sys
import os
import random
from datetime import datetime
import ConfigParser

CONFIG_FILE = "./start_my_day.conf"

def load_config(config_file):
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    config.readfp(open(config_file))
    sec_opt2val = {}
    for section in config.sections():
        sec_opt2val[section] = {}
        for option in config.options(section):
            sec_opt2val[section][option] = config.get(section,option)
    return sec_opt2val

def load_template(template_file):
    template_file = open(template_file).read()
    return template_file

def get_date_today(time_str):
    # time_str = "{0:%Y}年{0:%m}月{0:%d}日 {0:%H}时{0:%M}分"
    return time_str.format(datetime.today())

def get_today_habit(habit_list):
    return "".join(random.sample(habit_list,1))

def main(config_file):
    conf = load_config(config_file)
    template_string = load_template(conf["base_config"]["diary_template"])
    data = {"date_today":get_date_today(conf["formatter"]["date_today"]),
            "habit_today":get_today_habit(conf["habit_list"].keys())}
    print template_string.format(**data)

if __name__ == "__main__":
    main(CONFIG_FILE)
