# simple calculator
# by fayllar
# does basic math stuff

# functions for the operations
def Add(a, b):
    result = a + b
    return result

def subtract(a, b):
    return a - b

def Multiply(a,b):
    return a*b

def divide(a, b):
    # cant divide by zero
    if b == 0:
        return "ERROR cant divide by zero!!"
    return a / b

def power(a, b):
    return a ** b

# main program starts here
print("===== Simple Calculator =====")
print("by fayllar")
print("")

running = True
lastResult = 0  # save the last result

while running:
    print("\nwhat do you want to do?")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")
    print("5. Power")
    print("6. Exit")
    
    choice = input("\npick a number (1-6): ")
    
    if choice == "6":
        print("bye bye!")
        running = False
        continue
    
    if choice not in ["1", "2", "3", "4", "5"]:
        print("thats not a valid choice!!")
        continue
    
    num1 = float(input("enter first number: "))
    num2 = float(input("enter second number: "))
    
    # do the calculation
    if choice == "1":
        answer = Add(num1, num2)
        print("result:", num1, "+", num2, "=", answer)
    elif choice == "2":
        answer = subtract(num1, num2)
        print("result:", num1, "-", num2, "=", answer)
    elif choice == "3":
        answer = Multiply(num1, num2)
        print("result:", num1, "*", num2, "=", answer)
    elif choice == "4":
        answer = divide(num1, num2)
        print("result:", num1, "/", num2, "=", answer)
    elif choice == "5":
        answer = power(num1, num2)
        print("result:", num1, "^", num2, "=", answer)
    
    lastResult = answer  # save it
    # TODO: add option to use last result as input
