#!/usr/bin/python3

# Third party imports
from bs4 import BeautifulSoup
import configparser
import requests

# Local application imports
import classes.bcolors as bcolors
from classes.utilities import *
from classes.logs import *
from classes.tasks import *

# Consts
DEV_MODE = False
VERSION = "1.0"
TITLE = "NetsuiteBot"
SEPARATOR = "════════════════════════════════════"
SMALL_SEPARATOR = "────────────────────────────────────"
CONFIG_FILE = "configs.ini"
COOKIE_FILE = "cookies.txt"

# Global vars
# Login
login_url = "https://adfs.equisoft.com/adfs/ls/idpinitiatedsignon.aspx?loginToRp=http://www.netsuite.com/sp"
saml_response_url = "https://system.na1.netsuite.com:443/saml2/acs"
saml_login_url = "https://system.na1.netsuite.com/app/login/secure/saml.nl"
# Home
netsuite_base_url = "https://{user_session_id}.app.netsuite.com/app/site/hosting/scriptlet.nl"
netsuite_timesheet_url = netsuite_base_url + "?script=4&deploy=1&compid={user_session_id}&custparam_date={date}"
session_validation_url = netsuite_base_url + "?script=106&deploy=1"


def printLogo():
    # @formatter:off
    print(bcolors.output(" _   _        _                _  _        ", BColors.BLUE)  + bcolors.output("______           _   ", BColors.RED))  # nopep8
    print(bcolors.output("| \ | |      | |              (_)| |       ", BColors.BLUE)  + bcolors.output("| ___ \         | |  ", BColors.RED))  # nopep8
    print(bcolors.output("|  \| |  ___ | |_  ___  _   _  _ | |_  ___ ", BColors.BLUE)  + bcolors.output("| |_/ /  _____  | |_ ", BColors.RED))  # nopep8
    print(bcolors.output("| . ` | / _ \| __|/ __|| | | || || __|/ _ \\", BColors.BLUE) + bcolors.output("| ___ \ / ___ \ | __|", BColors.RED))  # nopep8
    print(bcolors.output("| |\  ||  __/| |_ \__ \| |_| || || |_|  __/", BColors.BLUE)  + bcolors.output("| |_/ /| (ʘ‿ʘ) || |_ ", BColors.RED))  # nopep8
    print(bcolors.output("\_| \_/ \___| \__||___/ \__,_||_| \__|\___|", BColors.BLUE)  + bcolors.output("\____/  \_____/  \__|", BColors.RED) +  # nopep8
          " " + bcolors.output(VERSION, BColors.BOLD))
    # @formatter:on


def open_config_file():
    if not os.path.exists(CONFIG_FILE):
        return False
    try:
        log_info("Reading configs file.")
        config.read(CONFIG_FILE)
        config_email = config.get("Credentials", "Email")
        config_password = config.get("Credentials", "Password")
        config_task = config.get("Informations", "Task")
        config_time = config.get("Informations", "Time")
        config_comment = config.get("Informations", "Comment")

        config["Credentials"]["Email"] = decode_base64(config_email)
        config["Credentials"]["Password"] = secure_decode_base64(config_password)

        if not is_valid_task_id(config_task):
            return False
        if config_time == "" or not valid_time(config_time):
            return False
        if config_comment.strip() == "":
            return False

        log_success("Configs loaded successfully.")
        log(SMALL_SEPARATOR)
        return True
    except configparser.NoOptionError:
        return False
    except UnicodeDecodeError:
        return False
    except binascii.Error:
        return False


def executeConfigurator():
    if getattr(sys, "frozen", False):
        app_name = "Configurator.appimage"
        app_path = os.path.join(os.path.dirname(sys.executable), "")
        os.system("cd \"" + app_path + "\" && ./" + app_name)
    else:  # Dev use only
        app_name = "configurator.py"
        app_path = os.path.join(os.path.abspath("."), "")
        os.system("cd \"" + app_path + "\" && python3 ./src/" + app_name)


def try_login(email, password, req=None):
    log_info("Getting SAML response.")
    data = {
        "UserName": email,
        "Password": password,
        "Kmsi": "true",
        "AuthMethod": "FormsAuthentication"
    }
    if req is None:
        req = requests
    request = req.post(login_url, data=data)
    page = BeautifulSoup(request.content, "html.parser")
    error = page.find("label", id="errorText")

    if error is None:
        log_info("Received SAML response.")
        return page
    else:
        log_error("Error while getting SAML response.")
        return None


def saml_login_authenticate(page):
    try:
        log_info("Sending SAML response.")
        saml_response = page.find("input", attrs={"name": "SAMLResponse", "type": "hidden"}).get("value")
        data = {"SAMLResponse": saml_response}
        request = cur_session.post(saml_response_url, data=data)

        log_info("Sending SAML login informations.")
        page_2 = BeautifulSoup(request.content, "html.parser")
        id_provider = page_2.find("input", attrs={"name": "identityProviderId", "type": "hidden"}).get("value")
        comp_id = page_2.find("input", attrs={"name": "c", "type": "hidden"}).get("value")
        email = page_2.find("input", attrs={"name": "email", "type": "hidden"}).get("value")
        session_id = page_2.find("input", attrs={"name": "sessionIndexId", "type": "hidden"}).get("value")
        lang = page_2.find("input", attrs={"name": "languageTag", "type": "hidden"}).get("value")
        signature = page_2.find("input", attrs={"name": "signature", "type": "hidden"}).get("value")
        data = {
            "identityProviderId": id_provider,
            "c": comp_id,
            "email": email,
            "sessionIndexId": session_id,
            "languageTag": lang,
            "signature": signature
        }
        cur_session.post(saml_login_url, data=data)
        return comp_id
    except (ValueError, Exception):
        log_error("Error while sending the SAML login informations.")
        return None


def authenticate_with_retries():
    result = None
    tries = 0
    max_tries = 3

    while result is None and tries < max_tries:
        while open_config_file() is False and tries < max_tries:
            # The first execution of Configurator will create the basic config.ini file.
            executeConfigurator()
            tries += 1
            log_info("Retrying to open valid configs...")
        if tries >= max_tries:
            log_error("Unable to read valid configs.")
            return

        login_email = config.get("Credentials", "Email")
        login_password = config.get("Credentials", "Password")
        if tries == 0:
            log_info("Trying to login...")
        else:
            log_info("Retrying to login...")
        login_result = try_login(login_email, login_password, cur_session)
        if login_result is not None:
            if os.path.exists(COOKIE_FILE) and DEV_MODE:
                result = "4146758"  # Dev
                log_info("Loading session " + result + " from cookies.")
                load_cookie_file()
                log_info("Cookies loaded successfully.")
            else:
                result = saml_login_authenticate(login_result)
                log_info("Session " + result + " created by authentification.")
                if DEV_MODE:
                    save_cookie_file()
                    log_info("Cookies saved successfully.")
        else:
            executeConfigurator()
            tries += 1

    return result


def load_cookie_file():  # Dev use only
    cookies = {}
    domain = ""
    if os.path.exists(COOKIE_FILE):
        with open(COOKIE_FILE, "r") as fp:
            for line in fp:
                if re.match(r"^#", line):
                    domain = line[1:].strip()
                    continue

                if line != "\n":
                    line_fields = line.strip().split("=", 1)
                    if len(line_fields) >= 2:
                        cookies[line_fields[0].strip()] = line_fields[1].strip()
                        cur_session.cookies.set(line_fields[0].strip(), line_fields[1].strip(), domain=domain)
    return cookies


def save_cookie_file():  # Dev use only
    cookie_file = open(COOKIE_FILE, "w+")
    empty_file = True
    domain = ""
    for cookie in iter(cur_session.cookies):
        if domain != cookie.domain:
            domain = cookie.domain
            if not empty_file:
                cookie_file.write("\n")
            empty_file = False
            cookie_file.write("# " + domain + "\n")
        cookie_file.write(cookie.name + " = " + cookie.value + "\n")
    cookie_file.close()


def is_time_submitted(time_entries):
    if len(time_entries) < 1:
        return False

    time_entry = time_entries[get_json_key_by_index(time_entries, 0)]
    if "isPendingApprovalFlag" in time_entry and time_entry["isPendingApprovalFlag"] == "T":
        return True
    return False


def is_time_only_saved(time_entries):
    if len(time_entries) < 1:
        return False
    time_entry = time_entries[get_json_key_by_index(time_entries, 0)]
    if len(time_entries) > 1 and time_entry["isPendingApprovalFlag"] == "F":
        return True
    if "hours" in time_entry and time_entry["hours"] != "" and \
            "comment" in time_entry and time_entry["comment"] != "" and \
            "isPendingApprovalFlag" in time_entry and time_entry["isPendingApprovalFlag"] == "F":
        return True
    return False


def submit_time(user_session_id, payload):
    formatted_session_validation_url = session_validation_url.format(user_session_id=user_session_id)
    request = cur_session.get(formatted_session_validation_url)
    validation_page = BeautifulSoup(request.content, "html.parser")
    if validation_page.text.strip() != "true":
        log_error("Cannot submit the timesheet. Session expired.")
    else:
        formatted_netsuite_timesheet_url = netsuite_timesheet_url.format(user_session_id=user_session_id, date="")
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.93 Safari/537.36",
        }
        data = {"submittedData": prettify_json(payload)}
        if DEV_MODE:
            log_info("Payload: \n" + prettify_json(payload, True))
            log_warning("Dev Mode: Time is NOT submitted.")
        else:
            result = cur_session.post(formatted_netsuite_timesheet_url, headers=headers, data=data)

            log(SMALL_SEPARATOR)
            if result.status_code == 200:
                log_success("Time submitted successfully!")
            else:
                log_error("Error while submitting the timesheet.")


def scrape():
    if DEV_MODE:
        log_warning("Dev mode is enabled.")

    user_session_id = authenticate_with_retries()
    if user_session_id is not None:
        log_success("Login successful.")
        log(SMALL_SEPARATOR)

        date = get_previous_working_date().strftime("%Y/%m/%d")
        # Dev test custom date
        # date = datetime.datetime(2021, 5, 1).strftime("%Y/%m/%d")
        log_info("Getting the Netsuite timeSheet page for: " + date)
        formatted_netsuite_timesheet_url = netsuite_timesheet_url.format(user_session_id=user_session_id, date=date)
        request = cur_session.get(formatted_netsuite_timesheet_url)

        # Dev: Test local pages
        # with open("src/payloads/netsuite/loggedin_landing_page_saved.html") as fp:
        #     netsuite_page = BeautifulSoup(fp, 'html.parser')

        netsuite_page = BeautifulSoup(request.content, "html.parser")
        time_sheet_page = netsuite_page.find("body", {"id": "timeSheetPage"})
        if time_sheet_page:
            log_info("Finding the data in the page.")
            script_text = time_sheet_page.find("script", {"src": False}).string.strip()
            if script_text:
                log_info("Parsing the time entries data.")
                time_entries = json.loads(get_js_var("timeEntries", script_text))
                if time_entries:
                    log_success("Data extraction successful.")
                    log(SMALL_SEPARATOR)
                    log_info("NetsuiteBot detecting action to take...")
                    if is_time_submitted(time_entries):
                        log_success("Time already submitted.")
                    elif is_time_only_saved(time_entries):
                        log_info("Time already saved. Submitting time...")
                        for entry in time_entries:
                            time_entries[entry]["isPendingApprovalFlag"] = "T"
                            time_entries[entry]["projectIsClosed"] = "F"
                        submit_time(user_session_id, time_entries)
                    else:
                        log_info("No existing time entry.")
                        log_info("Creating a new time entry. Submitting time...")
                        key = get_json_key_by_index(time_entries, 0)
                        time_entries[key]["task"] = config.get("Informations", "Task")
                        time_entries[key]["hours"] = config.get("Informations", "Time")
                        time_entries[key]["comment"] = config.get("Informations", "Comment").replace('"', '\"')
                        time_entries[key]["timeBillId"] = -100
                        time_entries[key]["isPendingApprovalFlag"] = "T"
                        time_entries[key]["projectIsClosed"] = "F"
                        submit_time(user_session_id, time_entries)
                else:
                    log_error("No time entries found.")
            else:
                log_error("Error while trying to parse the script.")
        else:
            error_msg = "Error while trying to load the Netsuite timeSheet page."
            page_title = netsuite_page.find("title").text
            if page_title:
                error_msg += "\nWe're on page titled: " + page_title
            log_error(error_msg)
    else:
        log_error("Failed to create user session id.")


if __name__ == "__main__":
    printLogo()
    log(SEPARATOR)

    config = configparser.ConfigParser()
    cur_session = requests.Session()
    scrape()
