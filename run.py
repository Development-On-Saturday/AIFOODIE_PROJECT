#!usr/bin/python

import os, sys

cmds = ['./django_dev', 'pip install -r requirements.txt', 'python manage.py migrate', 'python manage.py runserver']

for cmd in cmds:
    if 'django' in cmd:
        os.chdir(cmd)
    else :
        os.system(cmd)