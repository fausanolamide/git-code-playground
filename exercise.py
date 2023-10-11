# prime number
# num = eval(input('Enter number: '))
# flag = 0
# for i in range(2, num):
#     if num % i == 0:
#         flag = 1
# if flag == 1:
#     print('Not prime')
# else:
#     print('Prime')
# largest number
# largest = eval(input('Enter a positive number: '))
# for i in range(9):
#     num = eval(input('Enter a positive number: '))
#     if num > largest:
#         largest = num
#         print('Largest number:', largest)
# numbers divisible by 3
# count = 0
# for i in range(10):
#     if i % 3 == 0:
#         count = count+1
# print("numbers divisible by in 1 to 100 is :", count)
# from random import randint
# count = 0
# for i in range(10000):
#     num = randint(1, 100)
#     if num % 12 == 0:
#         count = count+1
# print('Number of multiples of 12:', count)


# def sum_of_divisors(number):
#     divisor_sum = 0

#     for i in range(1, number + 1):
#         if number % i == 0:
#             divisor_sum += i

#     return divisor_sum


# try:
#     user_input = int(input("Enter a number: "))
#     if user_input <= 0:
#         print("Please enter a positive integer.")
#     else:
#         result = sum_of_divisors(user_input)
#         print(f"The sum of divisors of {user_input} is {result}.")
# except ValueError:
#     print("Invalid input. Please enter a valid positive integer.")
from random import randint
score = 0
for i in range(5):
    num = int(input("Enter a number you guessed:"))
    guessed_number = randint(1, 10)
    if guessed_number == num:
        score = score+10
    else:
        score = score+1

print('Your total score is', score)
