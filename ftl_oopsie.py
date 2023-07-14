#!/bin/python3.11

"""
*********************************************************************************
*    Copyright (c) 2023 TpoMad                                                  *
*    All rights reserved.                                                       *
*                                                                               *
*    This file is part of FTL-Oopsie.py.                                        *
*                                                                               *
*    FTL-Oopsie.py is free software: you can redistribute it and/or modify      *
*    it under the terms of the GNU General Public License as published by       *
*    the Free Software Foundation, either version 3 of the License, GPL3.       *
*                                                                               *
*    FTL-Oopsie.py is distributed in the hope that it will be useful,           *
*    but WITHOUT ANY WARRANTY; without even the implied warranty of             *
*    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the               *
*    GNU General Public License for more details.                               *
*                                                                               *
*    You should have received a copy of the GNU General Public license          *
*    along with FTL-Oopsie.py. If not, see <http://www.gnu.org/licenses/>.      *
*                                                                               *
*    You are required to maintain this copyright notice in all copies or        *
*    substantial portions of the software.                                      *
*********************************************************************************
"""


from os import path, mkdir, listdir
from sys import argv
import colorama
from colorama import Fore
from colorama import Style
from pathlib import Path
from json import loads
from time import sleep
from datetime import datetime
from shutil import copy2


colorama.init() # for windows, does nothing on nix


def help():
    print(
        "Usage:\n"
        "   ftl_oopsie.py [options]\n\n"
        "Options:\n"
        "   b  or  backup       - backup mode\n"
        "   r  or  restore      - restore mode\n"
        "   nn or  no-name      - use this and you wont be asked for a custom name (quick backups)\n"
        "   dj or  dump-json    - dumps defaut FTL json settings\n\n"
        "If both backup and restore are used, backups will happen first.\n\n"
        "If this script cant find your save and settings files please check these locations.\n\n"
        "NIX : /home/USER_NAME/.local/share/FasterThanLight\n"
        "MAC : /home/USER_NAME/Library/Application Support/FasterThanLight\n"
        "WIN : USER_NAME\\Documents\\My Games\\FasterThanLight\n"
    )


def log_info(msgType, msg, msgColor=None, msgStyle=None):
    if not msgColor and msgType == "ERR":
        msgColor = f"{Fore.RED}"
    elif not msgColor and msgType == "INF":
        msgColor = f"{Fore.GREEN}"
    
    print(f"[*] {msgColor if msgColor else ''}{msgStyle if msgStyle else ''}{msg}{Style.RESET_ALL}")


# log_info("ERR", "Error Test")
# log_info("INF", "Info Test 1")
# log_info("INF", "Info Test 2", f"{Fore.CYAN}")
# log_info("INF", "Info Test 3", f"{Fore.CYAN}", f"{Style.DIM}")


class OopsieConfig:
    def __init__(self, json_data):
        self.FTL_SAVE_FILE_NAME = json_data["ftl_oopsie_settings"]["SAVE_FILE_NAME"]
        self.FTL_INI_FILE_MAME = json_data["ftl_oopsie_settings"]["INI_FILE_NAME"]
        self.FTL_BACKUP_DIRECTORY_NAME = json_data["ftl_oopsie_settings"]["BACKUP_DIRECTORY_NAME"]
        self.FTL_SAVE_DIRECTORY = json_data["ftl_oopsie_settings"]["DIRECTORY"]
        self.FTL_SAVE_FILE_PATH = self.FTL_SAVE_DIRECTORY + self.FTL_SAVE_FILE_NAME
        self.FTL_INI_FILE_PATH = self.FTL_SAVE_DIRECTORY + self.FTL_INI_FILE_MAME
        self.FTL_BACKUP_DIRECTORY = self.FTL_SAVE_DIRECTORY + self.FTL_BACKUP_DIRECTORY_NAME


def parse_json(file_path):
    try:
        with open(file_path, "r") as fh:
            json_data = loads(fh.read())

    except IOError as e:
        log_info("ERR", f"I/O error({e.errno}): {e.strerror}")

    except:
        log_info("ERR", f"Unexpected error: {exc_info()[0]}")

    return json_data if json_data else None


def restore_files(cfg):
    files = []
    for idx, file in enumerate(listdir(cfg.FTL_BACKUP_DIRECTORY)):
        even = idx % 2      # used to dim every other entry for easy reading
        if cfg.FTL_SAVE_FILE_NAME in file:
            log_info("INF", f"{idx} - {file}", f"{Fore.CYAN}", f"{Style.DIM if not even else Style.NORMAL}")
        
        if cfg.FTL_INI_FILE_MAME in file:
            log_info("INF", f"{idx} - {file}", f"{Fore.GREEN}", f"{Style.DIM if not even else Style.NORMAL}")

        files.append(file)

    print()
    log_info("INF", "-1 - Exit\n", f"{Fore.RED}")
    log_info("INF", "Which file would you like to restore? (select ONE via index)")
    user_input = input(f"[*] {Fore.BLUE}Idx {Fore.RESET}> ")
    if not user_input.isdigit():
        log_info("ERR", f"Invalid Input{Fore.RESET} {user_input}")
        return False

    user_input = int(user_input)
    if user_input >= len(files):
        log_info("ERR", f"Invalid Input{Fore.RESET}> {user_input}")
        return False

    print()
    log_info("INF", "Resotring file ..")
    if cfg.FTL_SAVE_FILE_NAME in files[user_input]:
        log_info(
            "INF",
            f"{files[user_input]} > {copy2(cfg.FTL_BACKUP_DIRECTORY + files[user_input], cfg.FTL_SAVE_FILE_PATH)}"
        )
    elif cfg.FTL_INI_FILE_MAME in files[user_input]:
        log_info(
            "INF",
            f"{files[user_input]} > {copy2(cfg.FTL_BACKUP_DIRECTORY + files[user_input], cfg.FTL_INI_FILE_PATH)}"
        )

    sleep(0.5)
    log_info("INF", "Finished resotring your file.\n")
    return True


def backup_files(cfg, no_name=False):
    DATE_TIME = datetime.now().strftime("%d-%B-%y-%H-%M-%S")
    FTL_BACKUP_SAVE_PATH = cfg.FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{cfg.FTL_SAVE_FILE_NAME}"
    FTL_BACKUP_INI_PATH = cfg.FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{cfg.FTL_INI_FILE_MAME}"

    if not path.exists(cfg.FTL_SAVE_FILE_PATH):
        log_info("ERR", f"File: {cfg.FTL_SAVE_FILE_PATH}> not found.")
        return False

    if not path.exists(cfg.FTL_INI_FILE_PATH):
        log_info("ERR", f"File: {cfg.FTL_INI_FILE_PATH}> not found.")
        return False

    if not path.exists(cfg.FTL_BACKUP_DIRECTORY):
        log_info("INF", f"Creating a backup directory at: {cfg.FTL_BACKUP_DIRECTORY}")
        mkdir(cfg.FTL_BACKUP_DIRECTORY)

    if not no_name:
        log_info("INF", "Would you like to give this round of backups a custom name?")
        user_input = input(f"[*] {Fore.BLUE}Y/n {Fore.RESET}> ").lower()
        if user_input == "y":
            user_input = input(f"[*] {Fore.BLUE}Name {Fore.RESET}> ")
            user_input = user_input + "_"
            FTL_BACKUP_INI_PATH = (
                cfg.FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{user_input}_{cfg.FTL_INI_FILE_MAME}"
            )
            FTL_BACKUP_SAVE_PATH = (
                cfg.FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{user_input}_{cfg.FTL_SAVE_FILE_NAME}"
            )

    print()
    log_info("INF", "Backing up your save and settings files")
    log_info("INF", f" > {copy2(cfg.FTL_INI_FILE_PATH, FTL_BACKUP_INI_PATH)}")
    sleep(0.5)
    log_info("INF", f" > {copy2(cfg.FTL_SAVE_FILE_PATH, FTL_BACKUP_SAVE_PATH)}")
    sleep(0.5)
    log_info("INF", "Finished backingup your files.\n")
    return True


def main(backup=False, restore=False, no_name=False):
    SCRIPT_DIRECTORY = path.dirname(path.realpath(argv[0]))
    user_config = OopsieConfig(parse_json(Path(SCRIPT_DIRECTORY, "settings.json")))
    if not user_config:
        log_info("ERR", "user config is: None")
        help()
        return

    if not backup and not restore:
        log_info("ERR", "No mode was given")
        help()
        return

    if not path.exists(user_config.FTL_SAVE_DIRECTORY):
        log_info("ERR", f"Driectory: {user_config.FTL_SAVE_DIRECTORY} not found.")
        help()
        return

    if backup:
        if not backup_files(user_config, no_name):
            log_info("ERR", "Backup Failed!")
            return

    if restore:
        if not restore_files(user_config):
            log_info("ERR", "Restore Failed!")
            return


DEFAULT_JSON_SETTINGS = """
{
    "ftl_oopsie_settings": {
        "DIRECTORY": "/home/{USER_NAME}/.local/share/FasterThanLight/",
        "BACKUP_DIRECTORY_NAME": "save-backups/",
        "SAVE_FILE_NAME": "ae_prof.sav",
        "SETTINGS_FILE_NAME": "settings.ini"
    }
}
"""


if __name__ == "__main__":
    print("FTL-Oopsie (to never make the same mistake again)\n")
    if "help" in argv or "h" in argv:
        help()
        exit()

    if "dump-json" in argv or "dj" in argv:
        print(DEFAULT_JSON_SETTINGS)
        exit()

    main(
        True if "backup" in argv or "b" in argv else False,
        True if "restore" in argv or "r" in argv else False,
        True if "no-name" in argv or "nn" in argv else False,
    )
