#!/bin/python


from os import path
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
    json_data = None
    try:
        with open(file_path, "r") as fh:
            json_data = loads(fh.read())

    except IOError as e:
        print(f"I/O error({e.errno}): {e.strerror}")
        return None

    except:
        print(f"Unexpected error: {exc_info()[0]}")
        return None

    return json_data


def restore(cfg):
    files = []
    for idx, file in enumerate(os.listdir(cfg.FTL_BACKUP_DIRECTORY)):
        even = idx % 2      # used to dim every other entry for easy reading
        if cfg.FTL_SAVE_FILE_NAME in file:
            print(
                f"{Fore.CYAN}[{Style.DIM if not even else Style.NORMAL}{idx}] - {file}{Style.RESET_ALL}"
            )
        
        if cfg.FTL_INI_FILE_MAME in file:
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
    if cfg.FTL_SAVE_FILE_NAME in files[user_input]:
        print(
            f"{files[user_input]} > {copy2(cfg.FTL_BACKUP_DIRECTORY + files[user_input], FTL_SAVE_FILE_PATH)}"
        )
    elif cfg.FTL_INI_FILE_MAME in files[user_input]:
        print(
            f"{files[user_input]} > {copy2(cfg.FTL_BACKUP_DIRECTORY + files[user_input], FTL_INI_FILE_PATH)}"
        )

    sleep(0.5)
    print("Finished!")


def backup(cfg, no_name=False):
    DATE_TIME = datetime.now().strftime("%d-%B-%y-%H-%M-%S")
    FTL_BACKUP_SAVE_PATH = cfg.FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{cfg.FTL_SAVE_FILE_NAME}"
    FTL_BACKUP_INI_PATH = cfg.FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{cfg.FTL_INI_FILE_MAME}"

    if not path.exists(cfg.FTL_SAVE_FILE_PATH):
        print(f"File: {Fore.RED}{cfg.FTL_SAVE_FILE_PATH}> not found.{Fore.RESET}")
        exit()

    if not path.exists(cfg.FTL_INI_FILE_PATH):
        print(f"File: {Fore.RED}{cfg.FTL_INI_FILE_PATH}> not found.{Fore.RESET}")
        exit()

    if not path.exists(cfg.FTL_BACKUP_DIRECTORY):
        print(f"Creating a backup directory at: {cfg.FTL_BACKUP_DIRECTORY}")
        os.mkdir(cfg.FTL_BACKUP_DIRECTORY)

    if not no_name:
        print("Would you like to give this round of backups a custom name?")
        user_input = input(f"{Fore.BLUE}Y/N{Fore.RESET}> ").lower()
        if user_input == "y":
            user_input = input(f"{Fore.BLUE}Name{Fore.RESET}> ")
            user_input = user_input + "_"
            FTL_BACKUP_INI_PATH = (
                cfg.FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{user_input}_{cfg.FTL_INI_FILE_MAME}"
            )
            FTL_BACKUP_SAVE_PATH = (
                cfg.FTL_BACKUP_DIRECTORY + f"{DATE_TIME}_{user_input}_{cfg.FTL_SAVE_FILE_NAME}"
            )

    print("Backing up your save and settings files")
    print(f" > {copy2(cfg.FTL_INI_FILE_PATH, FTL_BACKUP_INI_PATH)}")
    sleep(0.5)
    print(f" > {copy2(cfg.FTL_SAVE_FILE_PATH, FTL_BACKUP_SAVE_PATH)}")
    sleep(0.5)
    print(f"{Fore.GREEN}Finished!{Fore.RESET}\n")


def main(backup_files=False, restore_file=False, no_name=False):
    SCRIPT_DIRECTORY = path.dirname(path.realpath(argv[0]))
    user_config = OopsieConfig(parse_json(Path(SCRIPT_DIRECTORY, "settings.json")))
    if not user_config:
        help()
        return

    if not backup_files and not restore_file:
        help()
        return

    if not path.exists(user_config.FTL_SAVE_DIRECTORY):
        print(f"{Fore.RED}Driectory: {user_config.FTL_SAVE_DIRECTORY} not found.{Fore.RESET}")
        help()
        return

    if backup_files:
        backup(user_config, no_name)

    if restore_file:
        restore(user_config)


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
