#! /usr/bin/env python
# coding: utf-8

import sys,os
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

if __name__ == "__main__":
    print load_config(CONFIG_FILE)
