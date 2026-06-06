import random

# number guessing game by fayllar
# you have to guess the number between 1 and 100

print("=== Number Guessing Game ===")
print("im thinking of a number between 1 and 100...")
print("")

# pick difficulty
print("choose difficulty:")
print("1. Easy (10 tries)")
print("2. Medium (7 tries)")  
print("3. Hard (5 tries)")

difficulty = input("pick 1, 2 or 3: ")

# set the tries based on difficulty
if difficulty == "1":
    maxTries = 10
    print("easy mode! you get 10 tries")
elif difficulty == "2":
    maxTries = 7
    print("medium mode! you get 7 tries")
elif difficulty == "3":
    maxTries = 5
    print("hard mode! good luck lol")
else:
    maxTries = 7  # default to medium i guess
    print("ill just give you medium since you didnt pick right")

secret_number = random.randint(1, 100)
tries = 0
won = False
guessedNumbers = []  # keep track of guesses

# TODO: add a hint system maybe

while tries < maxTries:
    print("\ntries left:", maxTries - tries)
    guess = input("enter your guess: ")
    
    # make sure its a number
    if guess.isdigit() == False:
        print("thats not a number bruh")
        continue
    
    guess = int(guess)
    guessedNumbers.append(guess)
    tries = tries + 1
    
    if guess == secret_number:
        print("\n🎉 YOU GOT IT!! the number was", secret_number)
        print("it took you", tries, "tries")
        won = True
        break
    elif guess < secret_number:
        print("too low! go higher")
    elif guess > secret_number:
        print("too high! go lower")

if won == False:
    print("\nyou ran out of tries :(")
    print("the number was:", secret_number)

print("\nyour guesses were:", guessedNumbers)
print("thanks for playing!!")
