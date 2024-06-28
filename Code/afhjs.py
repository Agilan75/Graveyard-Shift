import random

# Initialize variables to track total questions and correct answers
total_questions = 0
correct_answers = 0

while True:
    # Generate two random integers between 1 and 1000
    num1 = random.randint(1, 1000)
    num2 = random.randint(1, 1000)

    # Get user input for the sum of the numbers
    user_answer = int(input(f"What is the sum of {num1} and {num2}? "))

    # Check if the answer is correct
    if user_answer == num1 + num2:
        print("Very Good!")
        correct_answers += 1
    else:
        print("No, try harder!")

    # Update total questions
    total_questions += 1

    # Ask if the user wants to try another question
    play_again = input("Do you want to try another question? (y/n) ").lower()

    # Check user's input for continuation or termination
    while play_again not in ['y', 'n']:
        play_again = input("Invalid input. Please enter 'y' or 'n': ").lower()

    if play_again == 'n':
        # Display results and exit the loop
        print("\nQuiz Summary:")
        print(f"Total Questions: {total_questions}")
        print(f"Correct Answers: {correct_answers}")
        percentage = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        print(f"Overall Percentage: {percentage:.1f}%")
        break
