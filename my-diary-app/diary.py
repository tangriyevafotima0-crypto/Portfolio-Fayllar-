# My Diary App
# by fayllar
# write your thoughts and read them later!

from datetime import datetime

# this is the file where entries get saved
fileName = "diary.txt"

def write_entry():
    print("\n--- Write New Entry ---")
    entry = input("whats on your mind today?\n> ")
    
    # get current date and time
    now = datetime.now()
    dateStr = now.strftime("%Y-%m-%d %H:%M")
    
    # save to file
    file = open(fileName, "a")
    file.write("--- " + dateStr + " ---\n")
    file.write(entry + "\n")
    file.write("\n")
    file.close()
    
    print("entry saved! ✅")

def read_entries():
    print("\n--- All Entries ---")
    try:
        file = open(fileName, "r")
        content = file.read()
        file.close()
        
        if content == "":
            print("no entries yet! write something first")
        else:
            print(content)
    except:
        print("no diary file found. write an entry first!")

def search_entries():
    print("\n--- Search ---")
    searchWord = input("what do you want to search for? ")
    
    try:
        file = open(fileName, "r")
        lines = file.readlines()
        file.close()
        
        found = False
        currentDate = ""
        
        for line in lines:
            if line.startswith("---"):
                currentDate = line.strip()
            if searchWord.lower() in line.lower():
                if found == False:
                    print(f"\nfound results for '{searchWord}':")
                    found = True
                print(currentDate)
                print(line.strip())
                print("")
        
        if found == False:
            print(f"couldnt find anything with '{searchWord}'")
    except:
        print("no diary file found!")

# main loop
print("=== My Diary App 📔 ===")
print("keep your thoughts safe!")

running = True
while running:
    print("\n--- Menu ---")
    print("1. Write new entry")
    print("2. Read all entries")
    print("3. Search entries")
    print("4. Exit")
    
    choice = input("\npick an option (1-4): ")
    
    if choice == "1":
        write_entry()
    elif choice == "2":
        read_entries()
    elif choice == "3":
        search_entries()
    elif choice == "4":
        print("bye! remember to write in your diary tomorrow 👋")
        running = False
    else:
        print("thats not a valid option!!")

# TODO: add option to delete entries
# TODO: add password protection maybe?
