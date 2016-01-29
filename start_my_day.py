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
    return "".join(["+ %s\n"%(s) for s in 
        random.sample(habit_list,habit_count)])

def get_reminder_today(conf):
    return "day"

def get_book_to_read(conf):
    book_list = conf["book_list"]
    note_template = conf["base_config"]["note_template"]

def get_questions(conf):
    questions_list = conf["questions_list"].keys()
    questions_count = min(len(questions_list),
            conf["base_config"]["questions_per_day"])
    return "\n".join(["+ %s\n"%(s) for s in 
        random.sample(questions_list,questions_count)])

def get_whether(conf):
    return "today_whether"

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
    print template_string.format(**data)

if __name__ == "__main__":
    main(CONFIG_FILE)
