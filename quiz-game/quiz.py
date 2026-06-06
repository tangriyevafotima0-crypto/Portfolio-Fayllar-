# quiz game by fayllar
# 10 questions, try to get them all right!

# all the questions are stored here
questions = [
    {
        "question": "What is the capital of France?",
        "options": ["A. London", "B. Paris", "C. Berlin", "D. Madrid"],
        "answer": "B"
    },
    {
        "question": "What planet is known as the Red Planet?",
        "options": ["A. Venus", "B. Jupiter", "C. Mars", "D. Saturn"],
        "answer": "C"
    },
    {
        "question": "How many legs does a spider have?",
        "options": ["A. 6", "B. 8", "C. 10", "D. 4"],
        "answer": "B"
    },
    {
        "question": "What is the largest ocean?",
        "options": ["A. Atlantic", "B. Indian", "C. Arctic", "D. Pacific"],
        "answer": "D"
    },
    {
        "question": "Who painted the Mona Lisa?",
        "options": ["A. Picasso", "B. Van Gogh", "C. Da Vinci", "D. Monet"],
        "answer": "C"
    },
    {
        "question": "What is 7 x 8?",
        "options": ["A. 54", "B. 56", "C. 48", "D. 64"],
        "answer": "B"
    },
    {
        "question": "Which animal is the fastest?",
        "options": ["A. Lion", "B. Cheetah", "C. Horse", "D. Eagle"],
        "answer": "B"
    },
    {
        "question": "How many continents are there?",
        "options": ["A. 5", "B. 6", "C. 7", "D. 8"],
        "answer": "C"
    },
    {
        "question": "What language is spoken in Brazil?",
        "options": ["A. Spanish", "B. English", "C. Portuguese", "D. French"],
        "answer": "C"
    },
    {
        "question": "What year did World War 2 end?",
        "options": ["A. 1943", "B. 1944", "C. 1945", "D. 1946"],
        "answer": "C"
    }
]

# start the quiz
print("=== QUIZ GAME ===")
print("10 questions, lets see how smart you are!!")
print("")

score = 0
questionNum = 1
totalQuestions = len(questions)  # this is 10 but whatever

for q in questions:
    print(f"Question {questionNum}/{totalQuestions}: {q['question']}")
    for option in q["options"]:
        print("  ", option)
    
    playerAnswer = input("\nyour answer (A/B/C/D): ").upper()
    
    # check if right
    if playerAnswer == q["answer"]:
        print("CORRECT!! nice one 🎉")
        score = score + 1
    else:
        print(f"WRONG! the answer was {q['answer']}")
        # show what the right answer was
        for option in q["options"]:
            if option[0] == q["answer"]:
                print(f"  -> {option}")
    
    print("")  # empty line
    questionNum = questionNum + 1

# show final score
print("=== RESULTS ===")
print(f"you got {score} out of {totalQuestions}!")

# give a message based on score
if score == 10:
    print("PERFECT SCORE!! youre a genius!!")
elif score >= 7:
    print("pretty good! nice job")
elif score >= 5:
    print("not bad, could be better tho")
else:
    print("oof... maybe study more lol")

# TODO: add more questions later
# TODO: add different categories maybe
