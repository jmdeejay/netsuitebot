# NetsuiteBot
![NetsuiteBot](./src/netsuite_logo.png)

NetsuiteBot allows you to always enter your Netsuite time on time.

Disclaimer:
This project is not intended to completely remove your habit of manually entering 
your Netsuite time. It is more a helper for when you save your time entries but 
forget to submit it or simply forget to create a time entry on time.

---

## Installation
- Make sure you have asdf already installed.


- Install the required python packages & create your virtual python environment with all the required packages.
  ```
  make install_requirements
  ```
  Once completed, you may setup PyCharm to use the created virtual environment, normally located:
  `~/.local/share/virtualenvs/netsuitebot-********`
  

- Compile the NetsuiteBot applications.
  ```
  make compile_applications
  ```

- Install NetsuiteBot.
  ```
  make install_netsuitebot
  ```
  
  On Mac, because we are saving a cronjob, you may need to approve the change. Click Ok.
  > "ApplicationXYZ" would like to administer your computer. Administration can include 
  > modifying password, networking and system settings.

  Configurator should be executed automatically at the end of the installation.
  (You can always execute it manually by running the Configurator executable)


- Enter & save your configurations.
  
  Test your login information (make sure everything works)

> **_!Important:_**  The bot cannot work properly without proper configurations entered & saved.

To uninstall NetsuiteBot simply run:
```
make uninstall_netsuitebot
```

To update NetsuiteBot simply run:
```
make update_netsuitebot
```

---

## Specifications
### Cronjob
When installing NetsuiteBot, a cronjob is automatically created for you.
The job will then run every weekday @ 11:00am.
You can verify its existence by running: `crontab -e`

There should be a cronjob similar to this:
```
0 11 * * 1-5 export PYTHONIOENCODING=UTF-8; export LANG=en_US.UTF-8; export LC_ALL=en_US.UTF-8; export DISPLAY=:0; cd "/home/user/netsuitebot" && ./NetsuiteBot > ./cron.log 2>&1
```

### Bot
NetsuiteBot will pop up the Configurator if there are invalid configurations or if he is unable to login with the credentials provided.
There will be 3 retries before closing completely & aborting the time submission.

NetsuiteBot will be smart when he submits your Netsuite timesheet.
At runtime, the bot will check the previous working day & it will either:
- Create a generic time entry (based on the information given in your configurations)
  then submit the timesheet, if there are no time entries already saved for the day.
- Submit your timesheet, if there is a time entry already saved for the day.
- Do nothing, if there is a time entry already saved & submitted for the day.

---

## Pre-requisites
- asdf
- python 3.8.3

## Required python packages
- beautifulsoup4
- configparser
- crontab
- macholib (Mac)
- pillow
- pyinstaller
- requests
- tkinter
  
## Development tools
- Install the required dev packages.
  ```
  make install_dev_requirements
  ```
- The code is pycodestyle (PEP8 if you use Pycharm) & Flake8 compliant.
  You can test code linting & styling by running:
  ```
  make code_lint
  make code_style
  ```
- The code is properly typed. You can test type checking by running:
  ```
  make type_check
  ```
- To output projects stats:
  ```
  make count_lines
  ```
