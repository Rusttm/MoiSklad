# -*- coding: utf8 -*-

import times
import schedule
from threading import Thread
from datetime import datetime


my_book_link = 'https://docs.google.com/spreadsheets/d/1_C6uxRFz5wb8K_Cu4c4HcUn8EYk0vnhARhA_UvtKT1c/edit#gid=0'
markdown = "<a href='<" + my_book_link + ">'>Сравнение цен</a>"

print(markdown)