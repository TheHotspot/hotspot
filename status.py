# helpful development script for django development
# trees current dir, shows git status and log, and validates models with a configurable refresh rate
# clicking on the growl notifications takes you directly to the relevant file

# GNTP uses the standard Python logging for Growl on Mac
import gntp.notifier
from time import sleep
import subprocess
import sys

AUTOCOMMIT_AFTER_PASS = True

# More complete example
growl = gntp.notifier.GrowlNotifier(
    applicationName = "Django Dev",
    notifications = ["Django Dev"],
    defaultNotifications = ["Django Dev"],
    # hostname = "computer.example.com", # Defaults to localhost
    # password = "abc123" # Defaults to a blank password
)
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

last_failed=False
last_state=""
filename="None"
linenum=0
while True:
    current_state = subprocess.check_output("ls -lstcR .", shell=True)
    if last_state != current_state:
        subprocess.call("git status -s --column", stdin=None, stdout=sys.stdout, stderr=sys.stderr, shell=True)
        subprocess.call("tree -d -C -t --dirsfirst", stdin=None, stdout=sys.stdout, stderr=sys.stderr, shell=True)
        sys.stdout.write("\n")
        sys.stdout.write("\n".join(subprocess.check_output("git glog", stdin=None, stderr=sys.stderr, shell=True).split("\n")[:4]))
        sys.stdout.write("\n")
        sys.stdout.write("\n")

        result = subprocess.check_output("python manage.py validate || echo '   '; exit 0;", stderr=subprocess.STDOUT, shell=True)
        if result.find("   ") != -1:
            sys.stdout.write(result)
            err_msg = "\n".join(result.split("\n")[-6:-2]).strip()
            if not last_failed:
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
            last_failed = True
        else:
            if last_failed:
                if AUTOCOMMIT_AFTER_PASS:
                    commit_result = subprocess.check_output('git commit -a -m "AUTOCOMMIT: fixed last error on %s:%s"; exit 0' % (filename, linenum), stderr=subprocess.STDOUT, shell=True)
                    alert_on_pass(commit_result)
                else:
                    alert_on_pass()
            last_failed = False
    last_state = current_state
    sleep(1)
