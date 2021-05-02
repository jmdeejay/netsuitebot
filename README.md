# NetsuiteBot
![NetsuiteBot](./src/netsuite_logo.png)

NetsuiteBot allows you to always enter your Netsuite time on time.

---

## Usage
- Install NetsuiteBot.
  ```
  ./install_netsuitebot.sh
  ```
  
  Configurator should be executed automatically at the end of the installation.
  (You can always execute it manually by double-clicking the Configurator executable)

- Enter & save your configurations.
  Test your login information (make sure everything works)

> **_!Important:_**  The bot cannot work properly without proper configurations entered & saved.

To uninstall NetsuiteBot simply run:
```
./install_netsuitebot.sh --remove
```

To update NetsuiteBot simply run:
```
./install_netsuitebot.sh --update
```

## Specifications
### Cronjob
When running the `install_netsuitebot.sh` script, a cronjob is automatically created for you.
NetsuiteBot will run every weekday @ 11:30am.
You can verify its existence by running: `crontab -e`

There should be a cronjob similar to this:
```
# NetsuiteBot scheduled job
30 11 * * 1-5 export DISPLAY=:0; cd "/home/user/netsuitebot" && ./NetsuiteBot > ./cron.log 2>&1
```

### Bot
NetsuiteBot will pop up the Configurator if there is invalid configurations or if he is unable to login with the credentials provided.
There will be 3 retries before closing completely & aborting the time submission.

NetsuiteBot will be smart when he submits your Netsuite timesheet.
At runtime, the bot will check the previous working day & it will either:
- Create a generic time entry (based on the information given in your configurations)
  then submit the timesheet, if there are no time entries already saved for the day.
- Submit your timesheet, if there is a time entry already saved for the day.
- Do nothing, if there is a time entry already saved & submitted for the day.

---

## Pre-requisites
- python3

## Required python packages
- beautifulsoup4
- configparser
- crontab
- pillow
- pyinstaller
- requests
- tkinter

## Development
- Install the required python packages.
  ```
  ./install_requirements.sh
  ```
- Create the NetsuiteBot configurator application in "./dist/Configurator".
  ```
  ./make_configurator.bash
  ```
- Create the NetsuiteBot scraper application in "./dist/NetsuiteBot".
  ```
  ./make_netsuitebot.bash
  ```
