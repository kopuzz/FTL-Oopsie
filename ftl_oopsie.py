#!/bin/python3
"""
  Copyright (c) 2023 TpoMad
  All rights reserved.

  This file is part of FTL-Oopsie.

  FTL-Oopsie is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, GPL3.

  FTL-Oopsie is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with FTL-Oopsie. If not, see <http://www.gnu.org/licenses/>.

  You are required to maintain this copyright notice in all copies or
  substantial portions of the software.
"""


import os
import sys
import time
import json
from shutil import copy2
from datetime import datetime
import colorama
from colorama import Fore
from colorama import Style

colorama.init() # for windows, does nothing on nix


SEP = "\\" if os.name == "nt" else "/"
SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(sys.argv[0]))
JSON_DATA = None
with open(f"{SCRIPT_DIRECTORY}{SEP}settings.json", "r") as jf:
    JSON_DATA = json.loads(jf.read())

FTL_SAVE_FILE_NAME = JSON_DATA["ftl_oopsie_settings"]["SAVE_FILE_NAME"]
FTL_INI_FILE_MAME = JSON_DATA["ftl_oopsie_settings"]["INI_FILE_NAME"]
FTL_BACKUP_DIRECTORY_NAME = JSON_DATA["ftl_oopsie_settings"]["BACKUP_DIRECTORY_NAME"]
FTL_SAVE_DIRECTORY = JSON_DATA["ftl_oopsie_settings"]["DIRECTORY"]

FTL_SAVE_FILE_PATH = FTL_SAVE_DIRECTORY + FTL_SAVE_FILE_NAME
FTL_INI_FILE_PATH = FTL_SAVE_DIRECTORY + FTL_INI_FILE_MAME
FTL_BACKUP_DIRECTORY = FTL_SAVE_DIRECTORY + FTL_BACKUP_DIRECTORY_NAME


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
        "WIN : USER_NAME\Documents\My Games\FasterThanLight\n"
    )


def restore():
    files = []
    for idx, file in enumerate(os.listdir(FTL_BACKUP_DIRECTORY)):
        even = idx%2    # used to dim every other entry for easy reading
        if FTL_SAVE_FILE_NAME in file:
            print(
                f"{Fore.CYAN}[{Style.DIM if not even else Style.NORMAL}{idx}] - {file}{Style.RESET_ALL}"
            )
        
        if FTL_INI_FILE_MAME in file:
            print(
                f"{Fore.GREEN}[{Style.DIM if not even else Style.NORMAL}{idx}] - {file}{Style.RESET_ALL}"
            )

        files.append(file)

    print(f"\n{Fore.RED}[-1] Exit.{Fore.RESET}")
    print("\nWhich file would you like to restore? (select ONE via index)")
    user_input = input(f"{Fore.BLUE}Idx{Fore.RESET}> ")
    if not user_input.isdigit():
        print(f"{Fore.RED}Invalid Input{Fore.RESET}> {user_input}")
        exit()

    user_input = int(user_input)
    if user_input >= len(files):
        print(f"{Fore.RED}Invalid Input{Fore.RESET}> {user_input}")
        exit()

    print("Resotring ..")
    if FTL_SAVE_FILE_NAME in files[user_input]:
        print(
            f"{files[user_input]} > {copy2(FTL_BACKUP_DIRECTORY + files[user_input], FTL_SAVE_FILE_PATH)}"
        )
    elif FTL_INI_FILE_MAME in files[user_input]:
        print(
            f"{files[user_input]} > {copy2(FTL_BACKUP_DIRECTORY + files[user_input], FTL_INI_FILE_PATH)}"
        )

    time.sleep(0.5)
    print(f"Finished!")


def backup(no_name=False):
    DATE_TIME = datetime.now().strftime("%d-%B-%y-%H-%M-%S")
    FTL_BACKUP_SAVE_PATH = FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{FTL_SAVE_FILE_NAME}"
    FTL_BACKUP_INI_PATH = FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{FTL_INI_FILE_MAME}"

    if not os.path.exists(FTL_SAVE_FILE_PATH):
        print(f"File: {Fore.RED}{FTL_SAVE_FILE_PATH}> not found.{Fore.RESET}")
        exit()

    if not os.path.exists(FTL_INI_FILE_PATH):
        print(f"File: {Fore.RED}{FTL_INI_FILE_PATH}> not found.{Fore.RESET}")
        exit()

    if not os.path.exists(FTL_BACKUP_DIRECTORY):
        print(f"Creating a backup directory at: {FTL_BACKUP_DIRECTORY}")
        os.mkdir(FTL_BACKUP_DIRECTORY)

    if not no_name:
        print("Would you like to give this round of backups a custom name?")
        user_input = input(f"{Fore.BLUE}Y/N{Fore.RESET}> ").lower()
        if user_input == "y":
            user_input = input(f"{Fore.BLUE}Name{Fore.RESET}> ")
            user_input = user_input + "_"
            FTL_BACKUP_INI_PATH = (
                FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{user_input}_{FTL_INI_FILE_MAME}"
            )
            FTL_BACKUP_SAVE_PATH = (
                FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{user_input}_{FTL_SAVE_FILE_NAME}"
            )

    print("Backing up your save and settings files")
    print(f" > {copy2(FTL_INI_FILE_PATH, FTL_BACKUP_INI_PATH)}")
    time.sleep(0.5)
    print(f" > {copy2(FTL_SAVE_FILE_PATH, FTL_BACKUP_SAVE_PATH)}")
    time.sleep(0.5)
    print("Finished!\n")


def main(backup_files=False, restore_file=False, no_name=False):
    if not backup_files and not restore_file:
        help()
        return

    if not os.path.exists(FTL_SAVE_DIRECTORY):
        print(f"{Fore.RED}Driectory: {FTL_SAVE_DIRECTORY} not found.{Fore.RESET}")
        help()
        return

    if backup_files:
        backup(no_name)

    if restore_file:
        restore()


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
    if "help" in sys.argv or "h" in sys.argv:
        help()
        exit()

    if "dump-json" in sys.argv or "dj" in sys.argv:
        print(DEFAULT_JSON_SETTINGS)
        exit()

    main(
        True if "backup" in sys.argv or "b" in sys.argv else False,
        True if "restore" in sys.argv or "r" in sys.argv else False,
        True if "no-name" in sys.argv or "nn" in sys.argv else False,
    )
