from random import randint
import random


def generate_question():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return num1, num2


def main():
    score = 0
    num_questions = 10

    print("Welcome to the Multiplication Game!")

    for i in range(num_questions):
        num1, num2 = generate_question()
        correct_answer = num1 * num2

        # Ask the question
        user_answer = int(input(f"What is {num1} x {num2}? "))

        # Check if the answer is correct
        if user_answer == correct_answer:
            print("Correct! Good job!")
            score += 1
        else:
            print(f"Sorry, the correct answer is {correct_answer}.")
    # Display bad comment
    if score <= 4:
        print("You failed this test, try again")
        print(
            f"You got {score} out of {num_questions} questions correct. Bad")
    else:
        # Display final score
        print(
            f"You got {score} out of {num_questions} questions correct. Well done!")


if __name__ == "__main__":
    main()
