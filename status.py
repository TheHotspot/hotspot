# -*- coding: utf-8 -*-
# helpful development script for django development
# trees current dir, shows git status and log, and validates models with a configurable refresh rate
# clicking on the growl notifications takes you directly to the relevant file

import gntp.notifier
from time import sleep
import subprocess
import sys

AUTOCOMMIT_AFTER_PASS = True            # autocommit when validate passes after previously failing using git commit -a -m "AUTOCOMMIT: after errorfix filelocation:linenum"
REFRESH_DELAY = 2                       # time to wait before checking code tree for changes using recently modified date
VERBOSE = True                        # display file tree, git status, and git log on terminal

growl = gntp.notifier.GrowlNotifier( applicationName = "Django Dev", notifications = ["Django Dev"], defaultNotifications = ["Django Dev"])
growl.register()

def alert_on_fail(error="Model Validation Fail", message="Alert error.", url=None, num=1):
    growl.notify(
        noteType = "Django Dev",
        title = error,
        description = message,
        icon = "http://vpn.nicksweeting.com/images/django.png",
        sticky = False,
        callback = url,
        priority = num,
    )

def alert_on_pass(message="COMMIT IT"):
    growl.notify(
        noteType = "Django Dev",
        title = "Model Validation Passed",
        description = message,
        icon = "http://vpn.nicksweeting.com/images/up.gif",
        sticky = False,
        priority = -2,
    )

def highlight_modified(git_status, dir_tree):
    """
    git_status = "
     M hotspot/apps/desktop/views.py
     M status.py
     "

    dir_tree = "
    .
    ├── hotspot
    │   ├── api
    │   │   ├── templates
    │   │   └── migrations
    │   ├── templates
    │   │   └── accounts
    │   ├── apps
    │   │   ├── desktop
    │   │   │   └── templates
    │   │   └── mobile
    │   │       └── templates
    │   └── libs
    ...
    "
    """

    git_status = git_status.split("\n")[:1]
    if git_status[0]:
        for line in git_status:
            line = line[10:]
            print line
            folders = []
            for folder in line.split("/")[:-1]:
                folders.append(folder)
            print folders

            for expected_depth,folder in enumerate(folders):
                for line in dir_tree.split("\n"):
                    depth_in_tree = len(line.replace("\xe2\x94\x9c","!").replace("\xe2\x94\x94", "!").replace("\xe2\x94\x82","!").split("!"))   # number of "│"s + "└─"s + "├"s = depth in tree
                    if depth_in_tree == expected_depth:
                        dir_tree = dir_tree.replace(line, line.replace(folder, "\x1b[31;1m"+folder))
        return dir_tree

    else:
        return dir_tree


last_passed=True
last_dir_state=""
short_filename="None"
linenum=0
while True:
    current_dir_state = subprocess.check_output("ls -lstcR .", shell=True)

    if last_dir_state != current_dir_state:
        if VERBOSE:
            git_status = subprocess.check_output("clear; git status -s", stderr=subprocess.STDOUT, shell=True)
            sys.stdout.write(git_status)
            dir_tree = subprocess.check_output("tree -d -C -t --dirsfirst", stderr=subprocess.STDOUT, shell=True)
            sys.stdout.write(highlight_modified(git_status, dir_tree))
            sys.stdout.write("\n")
            sys.stdout.write("\n".join(subprocess.check_output("git glog", stdin=None, stderr=sys.stderr, shell=True).split("\n")[:4]))
            sys.stdout.write("\n")
        sys.stdout.write("\n")

        result = subprocess.check_output("python manage.py validate || echo '   '; exit 0;", stderr=subprocess.STDOUT, shell=True) # if validate fails, append three spaces to output (...ugh so hacky)

        if result.find("   ") != -1:
            sys.stdout.write(result)
            err_msg = "\n".join(result.split("\n")[-6:-2]).strip()
            if last_passed:
                if err_msg.find("File") != -1:
                    filename = err_msg.split("\"")[1]
                    short_filename = filename.split("django-hotspot")[1]
                    short_errmsg = "\n".join(err_msg.split("\n")[1:])
                    linenum = err_msg[err_msg.find("line")+5:err_msg.find("\n")]

                    alert_on_fail(error="Syntax: "+short_filename.split("/")[-1]+":"+linenum, message=short_errmsg+"\n\n"+short_filename+":"+linenum, url="file://"+filename, num=1)
                else:
                    short_filename = err_msg.split("/django-hotspot")[1]
                    short_errmsg = "\n".join(err_msg.split("\n")[1:])
                    alert_on_fail("Model: "+short_filename, short_errmsg, num=2)
            last_passed = False
        else:
            if not last_passed:
                if AUTOCOMMIT_AFTER_PASS:
                    commit_result = subprocess.check_output('git commit -a -m "AUTOCOMMIT: errorfix most likely for %s:%s"; exit 0' % (short_filename, linenum), stderr=subprocess.STDOUT, shell=True)
                    alert_on_pass(commit_result)
                else:
                    alert_on_pass()
            last_passed = True

    last_dir_state = current_dir_state
    sleep(REFRESH_DELAY)
