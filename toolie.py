import asyncio
import os
import sys
import aiohttp
import re
import time
import random

from wonderwords import RandomWord
from termcolor import colored


clear_command = "clear" if os.name == "posix" else "cls"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0"
headers = {"User-Agent": user_agent}
alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpha_num = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


gt_backend_url = "https://www.gamertagavailability.com/check.php"
availability_regex = re.compile(r"seems to be available!")


def save_gamertag_to_text_file(gamertag: str):
    with open("gamertags.txt", "a+") as f:
        f.write(gamertag + "\n")


def get_random_word(random_word_length: int) -> str:
    r = RandomWord()
    word = r.word(word_min_length=random_word_length,
                  word_max_length=random_word_length)
    while "-" in word:
        word = r.word(word_min_length=random_word_length,
                      word_max_length=random_word_length)
    return word


def generate_random_characters_of_length(length: int) -> str:
    return f"{random.choice(alpha)}" + "".join(random.choice(alpha_num) for _ in range(length - 1))


def generate_semi_og_gamertag_combos(random_word: str) -> list[str]:
    leet_letters = {"o": "0"}
    acceptable_letter_substitutions = {"I": "l", "l": "I"}
    combo = []
    gamertag = random_word
    index = 0
    for letter in random_word:
        if index == 0:
            index += 1
            continue
        if letter in leet_letters:
            gamertag = gamertag.replace(letter, leet_letters[letter])
            if (gamertag.upper() not in combo):
                combo.append(gamertag.upper())
        elif letter in acceptable_letter_substitutions:
            gamertag = gamertag.replace(
                letter, acceptable_letter_substitutions[letter])
            if (gamertag.upper() not in combo):
                combo.append(gamertag.upper())

    index = 0
    random_word_reversed = random_word[::-1]
    for letter_reversed in random_word_reversed:
        if index == len(random_word) - 1:
            break
        if letter_reversed in leet_letters:
            gamertag = random_word_reversed.replace(
                letter_reversed, leet_letters[letter_reversed], 1
            )
            gamertag = gamertag[::-1]
            if (gamertag.upper() not in combo):
                combo.append(gamertag.upper())
        elif letter_reversed in acceptable_letter_substitutions:
            gamertag = random_word_reversed.replace(
                letter_reversed, acceptable_letter_substitutions[letter_reversed], 1
            )
            gamertag = gamertag[::-1]
            if (gamertag.upper() not in combo):
                combo.append(gamertag.upper())
        index += 1

    return combo


def lottery_gamertag():
    lottery_options = ["random_word", "random_characters"]
    min_random_word_length = 4
    max_random_word_length = 12
    min_random_character_length = 2
    max_random_character_length = 4
    random_lottery_option = random.choice(lottery_options)
    if random_lottery_option == "random_word":
        random_word_length = random.randint(
            min_random_word_length, max_random_word_length)
        return get_random_word(random_word_length)
    elif random_lottery_option == "random_characters":
        random_character_length = random.randint(
            min_random_character_length, max_random_character_length)
        return generate_random_characters_of_length(random_character_length)


async def check_gamertag(gamertag) -> bool:
    form_data = {"Gamertag": gamertag, "Gamerage": "", "Language": "English"}
    async with aiohttp.ClientSession() as session:
        async with session.post(gt_backend_url, headers=headers, data=form_data) as response:
            if response.status == 200:
                content = await response.text()
                match = re.search(availability_regex, content.strip())
                if match:
                    return True
                else:
                    return False
            else:
                return False


async def gt_menu():
    os.system(clear_command)

    try:
        while True:
            sys.stdout.write(
                colored(
                    """
                     ██████╗████████╗    ████████╗ ██████╗  ██████╗ ██╗          ██╗██╗  ██╗
                    ██╔════╝╚══██╔══╝    ╚══██╔══╝██╔═══██╗██╔═══██╗██║         ███║██║  ██║
                    ██║  ███╗  ██║          ██║   ██║   ██║██║   ██║██║         ╚██║███████║
                    ██║   ██║  ██║          ██║   ██║   ██║██║   ██║██║          ██║╚════██║
                    ╚██████╔╝  ██║          ██║   ╚██████╔╝╚██████╔╝███████╗     ██║██╗  ██║
                     ╚═════╝   ╚═╝          ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝     ╚═╝╚═╝  ╚═╝
"""
                    + "\n\n", "green"
                )
            )
            print(colored("Gamertag Availability Checker", "blue"))
            print(colored("Version: 1.0.0", "blue"))
            print(colored("By: aylo", "blue"))
            print("\n")
            print(colored("1. Check Custom Gamertag Availability", "white"))
            print(colored("2. Check Random Real Word Gamertag Availability", "white"))
            print(colored("3. Check Random Character Gamertag Availability", "white"))
            print(colored("4. Spam Random Real Word Gamertags", "white"))
            print(colored("5. Spam Random Character Gamertags", "white"))
            print(colored("6. Check Every Beginning Letter", "white"))
            print(colored("7. Check Every Ending Character", "white"))
            print(colored("8. Lottery", "white"))
            print(colored("9. Lottery Spam", "white"))
            print(colored("10. Check Semi OG Gamertags", "white"))
            print(colored("11. Spam Semi OG Gamertags", "white"))
            print(colored("12. Exit", "red"))
            print("\n")
            choice = input(colored("Enter your choice: ", "white"))
            if choice == "1":
                os.system(clear_command)
                do_another = True
                while do_another:
                    gamertag = input(colored("Enter your gamertag: ", "white"))
                    print(colored(f"Checking {gamertag}...", "white"))
                    if await check_gamertag(gamertag):
                        print(colored(f"{gamertag} is available", "green"))
                        save_gamertag_to_text_file(gamertag)
                    else:
                        print(colored(f"{gamertag} is not available", "red"))
                    do_another = input(colored(
                        "Do you want to check another gamertag? (y/n): ", "white")).lower() == "y"
                    os.system(clear_command)
            elif choice == "2":
                os.system(clear_command)
                do_another = True
                random_word_length = int(
                    input(colored("Enter the desired length of the random gamertag: ", "white")))
                while do_another:
                    gamertag = get_random_word(random_word_length)
                    print(colored(f"Checking {gamertag}...", "white"))
                    if await check_gamertag(gamertag):
                        print(colored(f"{gamertag} is available", "green"))
                        save_gamertag_to_text_file(gamertag)
                    else:
                        print(colored(f"{gamertag} is not available", "red"))
                    do_another = input(colored(
                        "Do you want to check another gamertag? (y/n): ", "white")).lower() == "y"
                    os.system(clear_command)
            elif choice == "3":
                os.system(clear_command)
                do_another = True
                while do_another:
                    length = int(
                        input(colored("Enter the length of the random gamertag: ", "white")))
                    gamertag = generate_random_characters_of_length(length)
                    print(colored(f"Checking {gamertag}...", "white"))
                    if await check_gamertag(gamertag):
                        print(colored(f"{gamertag} is available", "green"))
                        save_gamertag_to_text_file(gamertag)
                    else:
                        print(colored(f"{gamertag} is not available", "red"))
                    do_another = input(colored(
                        "Do you want to check another gamertag? (y/n): ", "white")).lower() == "y"
                    os.system(clear_command)
            elif choice == "4":
                os.system(clear_command)
                random_word_length = int(
                    input(colored("Enter the desired length of the random gamertag: ", "white")))
                print(colored("Starting spamming...", "white"))
                print(colored("Press Ctrl+C to stop", "white"))
                try:
                    while True:
                        gamertag = get_random_word(random_word_length)
                        print(colored(f"Checking {gamertag}...", "white"))
                        if await check_gamertag(gamertag):
                            print(colored(f"{gamertag} is available", "green"))
                            save_gamertag_to_text_file(gamertag)
                        else:
                            print(
                                colored(f"{gamertag} is not available", "red"))
                except:
                    print(colored("Stopping spamming...", "white"))
                    time.sleep(0.5)
                    os.system(clear_command)
            elif choice == "5":
                os.system(clear_command)
                print(colored("Starting spamming...", "white"))
                print(colored("Press Ctrl+C to stop", "white"))
                length = int(
                    input(colored("Enter the length of the random gamertag: ", "white")))
                try:
                    while True:
                        gamertag = generate_random_characters_of_length(length)
                        print(colored(f"Checking {gamertag}...", "white"))
                        if await check_gamertag(gamertag):
                            print(colored(f"{gamertag} is available", "green"))
                            save_gamertag_to_text_file(gamertag)
                        else:
                            print(
                                colored(f"{gamertag} is not available", "red"))
                except:
                    print(colored("Stopping spamming...", "white"))
                    time.sleep(0.5)
                    os.system(clear_command)
            elif choice == "6":
                os.system(clear_command)
                end_of_tag = input(
                    colored("Enter the end of the gamertag: ", "white"))
                print(colored("Starting checking...", "white"))
                print(colored("Press Ctrl+C to stop", "white"))
                alpha_list = list(alpha)
                try:
                    for i in range(len(alpha_list)):
                        gamertag = alpha_list[i] + end_of_tag
                        print(colored(f"Checking {gamertag}...", "white"))
                        if await check_gamertag(gamertag):
                            print(colored(f"{gamertag} is available", "green"))
                            save_gamertag_to_text_file(gamertag)
                        else:
                            print(
                                colored(f"{gamertag} is not available", "red"))
                    time.sleep(0.5)
                    os.system(clear_command)
                except:
                    print(colored("Stopping checking...", "white"))
                    time.sleep(0.5)
                    os.system(clear_command)
            elif choice == "7":
                os.system(clear_command)
                beg_of_tag = input(
                    colored("Enter the beginning of the gamertag: ", "white"))
                letters_only = input(
                    colored("Only letters? (y/n): ", "white")).lower() == "y"
                if letters_only:
                    alpha_list = list(alpha)
                else:
                    alpha_list = list(alpha_num)
                print(colored("Starting checking...", "white"))
                print(colored("Press Ctrl+C to stop", "white"))
                try:
                    for i in range(len(alpha_list)):
                        gamertag = beg_of_tag + alpha_list[i]
                        print(colored(f"Checking {gamertag}...", "white"))
                        if await check_gamertag(gamertag):
                            print(colored(f"{gamertag} is available", "green"))
                            save_gamertag_to_text_file(gamertag)
                        else:
                            print(
                                colored(f"{gamertag} is not available", "red"))
                    time.sleep(0.5)
                    os.system(clear_command)
                except:
                    print(colored("Stopping checking...", "white"))
                    time.sleep(0.5)
                    os.system(clear_command)
            elif choice == "8":
                os.system(clear_command)
                do_another = True
                while do_another:
                    gamertag = lottery_gamertag()
                    print(colored(f"Checking {gamertag}...", "white"))
                    if await check_gamertag(gamertag):
                        print(colored(f"{gamertag} is available", "green"))
                        save_gamertag_to_text_file(gamertag)
                    else:
                        print(colored(f"{gamertag} is not available", "red"))
                    do_another = input(colored(
                        "Do you want to check another gamertag? (y/n): ", "white")).lower() == "y"
                    os.system(clear_command)
            elif choice == "9":
                os.system(clear_command)
                print(colored("Starting Lottery Spamming...", "white"))
                print(colored("Press Ctrl+C to stop", "white"))
                try:
                    while True:
                        gamertag = lottery_gamertag()
                        print(colored(f"Checking {gamertag}...", "white"))
                        if await check_gamertag(gamertag):
                            print(colored(f"{gamertag} is available", "green"))
                            save_gamertag_to_text_file(gamertag)
                        else:
                            print(
                                colored(f"{gamertag} is not available", "red"))
                except:
                    print(colored("Stopping spamming...", "white"))
                    time.sleep(0.5)
                    os.system(clear_command)
            elif choice == "10":
                os.system(clear_command)
                do_another = True
                while do_another:
                    length = int(
                        input(colored("Enter the length of the gamertag: ", "white")))
                    random_word = get_random_word(length)
                    print(colored(f"Checking {random_word}...", "white"))
                    gamertags = generate_semi_og_gamertag_combos(random_word)
                    if len(gamertags) == 0:
                        print(colored(f"No combinations found for {
                              random_word}", "red"))
                        do_another = input(colored(
                            "Do you want to check another gamertag? (y/n): ", "white")).lower() == "y"
                        os.system(clear_command)
                        continue
                    print(
                        colored(f"Checking {", ".join(gamertags)}...", "white"))
                    tasks = [check_gamertag(gamertag)
                             for gamertag in gamertags]
                    results = await asyncio.gather(*tasks)
                    result_strings = [colored(f"{gamertag} is available", "green") if result else colored(
                        f"{gamertag} is not available", "red") for gamertag, result in zip(gamertags, results)]
                    for gamertag, result in zip(gamertags, results):
                        if result:
                            save_gamertag_to_text_file(gamertag)
                    print("\n".join(result_strings))
                    do_another = input(colored(
                        "Do you want to check another gamertag? (y/n): ", "white")).lower() == "y"
                    os.system(clear_command)
            elif choice == "11":
                os.system(clear_command)
                length = int(
                    input(colored("Enter the length of the gamertag: ", "white")))
                print(colored("Starting Semi OG Spamming...", "white"))
                print(colored("Press Ctrl+C to stop", "white"))
                try:
                    while True:
                        random_word = get_random_word(length)
                        print(colored(f"Checking {random_word}...", "white"))
                        gamertags = generate_semi_og_gamertag_combos(
                            random_word)
                        if len(gamertags) == 0:
                            print(colored(f"No combinations found for {
                                  random_word}", "red"))
                            time.sleep(0.5)
                            continue
                        print(
                            colored(f"Checking {', '.join(gamertags)}...", "white"))
                        tasks = [check_gamertag(gamertag)
                                 for gamertag in gamertags]
                        results = await asyncio.gather(*tasks)
                        result_strings = [colored(f"{gamertag} is available", "green") if result else colored(
                            f"{gamertag} is not available", "red") for gamertag, result in zip(gamertags, results)]
                        for gamertag, result in zip(gamertags, results):
                            if result:
                                save_gamertag_to_text_file(gamertag)
                        print("\n".join(result_strings))
                        time.sleep(0.5)
                except Exception as e:
                    print(colored(f"An error occurred: {e}", "red"))
                    time.sleep(5)
                    print(colored("Stopping spamming...", "white"))
                    time.sleep(0.5)
                    os.system(clear_command)
            elif choice == "12":
                os.system(clear_command)
                print(colored("Exiting...", "red"))
                time.sleep(0.5)
                sys.exit(0)
            else:
                print(colored("Invalid choice. Please try again.", "red"))
                time.sleep(2)
                os.system(clear_command)
                continue

    except KeyboardInterrupt:
        os.system(clear_command)
        print(colored("Exiting...", "red"))
        time.sleep(0.5)
        sys.exit(0)
    except EOFError:
        os.system(clear_command)
        print(colored("Exiting...", "red"))
        time.sleep(0.5)
        sys.exit(0)
    except Exception as e:
        os.system(clear_command)
        print(colored(f"An error occurred: {e}", "red"))
        time.sleep(0.5)
        sys.exit(1)


async def main() -> None:
    # if len(sys.argv) < 2:
    #   print(f"Usage: {sys.argv[0]} <gamertag>")
    #   sys.exit(1)

    # if sys.argv[1] == "-r":
    #   gamertag = get_random_word()
    # else:
    #   gamertag = sys.argv[1]

    # if not await check_gamertag(gamertag):
    #   print(colored(f"{gamertag} is not available", "red"))
    # else:
    #   print(colored(f"{gamertag} is available", "green"))

    await gt_menu()

if __name__ == "__main__":
    asyncio.run(main())
