#!/bin/sh
while :;
    do clear;
    tree -C -t --dirsfirst;
    echo "";
    git status;
    git glog;
    echo "";
    python manage.py validate | pygmentize -l python;
    echo "";
    sleep 5;
done
