import random, string, os, requests, hashlib, threading, time #, multiprocessing

''' Red: \u001b[31m
Green: \u001b[32m
Yellow: \u001b[33m
Blue: \u001b[34m
Magenta: \u001b[35m
Cyan: \u001b[36m
White: \u001b[37m '''

# COLOURS FOR TEXT

class colour:
    Green = "\u001b[32m"
    Yellow = "\u001b[33m"
    Blue = "\u001b[34m"
    Magenta = "\u001b[35m"
    White = "\u001b[37m"

os.system('cls' if os.name == 'nt' else 'clear')
print(colour.Magenta + "\033[1m▒▒▒▒▒ GATHERER ▒▒▒▒▒\033[0m")
print()

# FUNCTIONS

def save_to_file(strings, filename):
    with open(filename, 'a') as file:
        for s in strings:
            file.write(s + '\n')

''' def keygen(number_of_symbols): #old
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

def keygen_unique(number_of_symbols):
	random_api_key = ''.join(random.choices(string.ascii_lowercase + string.digits, k=number_of_symbols))
	unique_key = hashlib.sha256(random_api_key.encode()).hexdigest()[:number_of_symbols]
	url = "https://api.hunter.io/v2/email-finder?domain=gmail.com&first_name=test&last_name=test&api_key=" + unique_key
	try:
		donecheck = requests.get(url)
		if donecheck.status_code == 400: # 401 to test
			save_to_file([unique_key + " "], "hunter_key.txt")
			print(f"\033[1mKey {unique_key} picked and saved to 'hunter_key.txt'\033[0m")
		elif donecheck.status_code == 403:
			print("\033[1mForbidden (403)\033[0m")
			while donecheck.status_code == 403:
				time.sleep(0.5)
				url = "https://api.hunter.io/v2/email-finder?domain=gmail.com&first_name=test&last_name=test&api_key=" + unique_key
	except KeyboardInterrupt:
		print()
	except Exception as e:
		print("An error occurred:", e)
	return unique_key

# MAIN MENU

def main_menu():
	print(colour.Yellow + "\033[1mMain menu:\033[0m")
	print(colour.Yellow + "\033[1m[1] - hunter.io API key finder\033[0m")
	print(colour.Yellow + "\033[1m[0] - Exit\033[0m")
	print()
	print(colour.Yellow + "\033[1m[i] - Instructions\033[0m")
	print()

	choise = input(colour.Yellow + "\033[1m=> \033[0m").strip()

	if choise == "1":
		print()
		print("Trying...")
		print()
		try:
			# keygen_unique(40) # old
			num_threads = 2
			while True:
				threads = []
				for _ in range(num_threads):
					thread = threading.Thread(target=keygen_unique, args=(40,))
					threads.append(thread)
					thread.start()
					time.sleep(0.1) # bypassing Forbidden error (403)
				for thread in threads:
					thread.join()

			''' num_processes = 2 # not finished
			while True:
				processes = []
				for _ in range(num_processes):
					process = multiprocessing.Process(target=keygen_unique, args=(40,))
					processes.append(process)
					process.start()
				for process in processes:
					process.join() '''

		except KeyboardInterrupt:
			print("Operation cancelled by user (KeyboardInterrupt exception)")	
			input("\033[1mPress Enter to continue\033[0m")
			print()
			main_menu()

	elif choise == "i":
		print("\033[1m!THE PROGRAM IS UNDER DEVELOPMENT!\033[0m")
		print("\033[1mManual usage for Email finder:" + colour.Magenta + "https://api.hunter.io/v2/email-finder?domain=" + colour.Yellow + "[DOMAIN]" + colour.Magenta + "&first_name=" + colour.Yellow + "[FIRST NAME]" + colour.Magenta + "&last_name=" + colour.Yellow + "[LAST NAME]" + colour.Magenta + "&api_key=" + colour.Yellow + "[YOUR API KEY]\033[0m")
		print("\033[1mPress " + colour.Yellow + "'Ctrl+C'" + colour.White + " to stop the work of key generator.\033[0m")
		print("\033[1mEnter " + colour.Yellow + "'M'" + colour.White + " to return to main menu.\033[0m")
		key = input(colour.Yellow + "\033[1m=> \033[0m")
		if key == "m":
			main_menu()

	elif choise == "0":
		print("\033[1mGoodbye!\033[0m")
		exit()	

	else:
		main_menu()

# STARTING SCRIPT
		
if __name__ == "__main__":
	try:
		main_menu()
	except KeyboardInterrupt:
		print("\nScript interrupted by user.")
