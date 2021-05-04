#!/usr/bin/python

# Standard library imports
import getpass
import os
import sys

# Third party imports
from crontab import CronTab


def cron_exists():
    exists = False
    for item in cron.find_comment(comment):
        if cmd in str(item):
            exists = True
            break
    return exists


def install_cron():
    if not cron_exists():
        job = cron.new(command=cmd, comment=comment, pre_comment=True)
        job.minute.on(30)
        job.hour.on(11)
        job.dow.during(1, 5)
        job.enable()
        cron.write()


def uninstall_cron():
    cron.remove_all(command=cmd, comment=comment)
    cron.write()


if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] not in ["install", "uninstall"]:
        print("Usage: pipenv run python ./cron.py ACTION FILEPATH FILENAME")
        print("ACTION [install | uninstall]")
        exit()

    action = sys.argv[1]
    filepath = sys.argv[2]
    filename = sys.argv[3]

    if not os.path.isdir(filepath):
        print("Invalid filepath: \"" + filepath + "\"")
        exit()

    if not os.path.isfile(os.path.join(filepath, filename)):
        print("File cannot be found on: \"" + os.path.join(filepath, filename) + "\"")
        exit()

    cron = CronTab(user=getpass.getuser())
    cmd = "export DISPLAY=:0; cd \"" + filepath + "\" && ./" + filename + " > ./cron.log 2>&1"
    comment = "NetsuiteBot scheduled job"

    if action == "install":
        install_cron()
        print("NetsuiteBot cronjob installed successfully.")
    elif action == "uninstall":
        uninstall_cron()
        print("NetsuiteBot cronjob uninstalled successfully.")
