#!/bin/sh
rm db.*
rm media/ -r 
python3 manage.py makemigrations users events pos content
python3 manage.py migrate
python3 f_seeder.py
