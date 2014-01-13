#!/bin/sh
while :;
    do clear;
    tree -C -t --dirsfirst;
    echo "";
    git status;
    git glog;
    echo "";
    python manage.py validate 2>&1 | pygmentize -l python;
    echo "";
    sleep 10;
done
