#!usr/bin/python

from __future__ import print_function
import argparse
import os, sys

def to_bool(x):
    if x.lower() in ['true','t']:
        return True
    elif x.lower() in ['false','f']:
        return False
    else:
        raise argparse.ArgumentTypeError('Bool 값을 넣으세요')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', type=to_bool, default=False,
                        metavar='runserver',
                        help='if you want to run server only'
                        )

    args = parser.parse_args()


    cmds = ['./django_dev', 'pip install -r requirements.txt', 'python manage.py migrate', 'python manage.py runserver']

    if args.r :
        os.chdir('./django_dev')
        os.system('python manage.py runserver')
    else :
        for cmd in cmds:
            if 'django' in cmd:
                os.chdir(cmd)
            else :
                os.system(cmd)

if __name__ == '__main__':
    main()