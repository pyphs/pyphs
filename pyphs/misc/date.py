# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 13:55:52 2016

@author: Falaize
"""


def get_date():
    " Return current date and time "
    from datetime import datetime
    now = datetime.now()
    dt_format = '%Y/%m/%d %H:%M:%S'
    return now.strftime(dt_format)
