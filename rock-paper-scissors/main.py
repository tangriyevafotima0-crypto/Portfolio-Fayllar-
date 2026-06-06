import random

# rock paper scissors game
# made by fayllar

print("=== Rock Paper Scissors ===")
print("first to 3 wins!!")

player_score = 0
compScore = 0  # computer score
rounds = 0

while player_score < 3 and compScore < 3:
    print("\n--- Round", rounds + 1, "---")
    print("Score: You", player_score, "- Computer", compScore)
    
    player_choice = input("choose rock, paper or scissors: ").lower()
    
    # check if valid
    if player_choice != "rock" and player_choice != "paper" and player_choice != "scissors":
        print("thats not valid!! try again")
        continue
    
    options = ["rock", "paper", "scissors"]
    compChoice = random.choice(options)
    print("computer chose:", compChoice)
    
    # figure out who wins
    if player_choice == compChoice:
        print("its a tie!!")
    elif player_choice == "rock" and compChoice == "scissors":
        print("you win this round!")
        player_score = player_score + 1
    elif player_choice == "paper" and compChoice == "rock":
        print("you win this round!")
        player_score = player_score + 1
    elif player_choice == "scissors" and compChoice == "paper":
        print("you win this round!")
        player_score = player_score + 1
    else:
        print("computer wins this round!")
        compScore = compScore + 1
    
    rounds = rounds + 1

# game over
print("\n=== GAME OVER ===")
if player_score == 3:
    print("YOU WON!! congrats!!")
else:
    print("computer won... better luck next time")
print("total rounds played:", rounds)
