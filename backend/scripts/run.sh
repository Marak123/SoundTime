#!/bin/sh

set -e

# Black        0;30     Dark Gray     1;30
# Red          0;31     Light Red     1;31
# Green        0;32     Light Green   1;32
# Brown/Orange 0;33     Yellow        1;33
# Blue         0;34     Light Blue    1;34
# Purple       0;35     Light Purple  1;35
# Cyan         0;36     Light Cyan    1;36
# Light Gray   0;37     White         1;37

RED='\033[0;31m'
LIGHTRED='\033[1;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color


echo -e "${PURPLE}Run as user:${RED} $(whoami)"

echo -e "${GREEN}--------------------------- Waiting For DataBase ----------------------------${CYAN}"

python manage.py wait_for_db
if [ $? -ne 0 ]; then
    exit 3
fi

echo -e "${GREEN}----------------------------- DataBase is Ready -----------------------------"
echo -e "\n${GREEN}---------------------------- Make App Migrations ----------------------------${CYAN}"

python manage.py --migrate
if [ $? -ne 0 ]; then
    exit 3
fi

echo -e "\n${GREEN}---------------------------- App Migrations is Ready ----------------------------"
echo -e "\n${GREEN}--------------------------- Launching The Application ---------------------------${CYAN}"

gunicorn core.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4 --reload



# python manage.py runserver 0.0.0.0:8000

# uwsgi --socket :9000 --workers 4 --master --enable-threads --module core.wsgi
