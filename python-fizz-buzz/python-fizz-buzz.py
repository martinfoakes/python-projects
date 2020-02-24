# Take a User input Integer, and return FizzBuzz solution up to that number

def fizz_buzz():
  user_input = int(input("Enter a Number to return FizzBuzz solution to that place: "))

  for num in range(1, user_input + 1):
    response = ""

    if num % 15 == 0:
      response += f'FizzBuzz: ({num})'
    elif num % 3 == 0:
      response += f'Fizz: ({num})'
    elif num % 5 == 0:
      response += f'Buzz: ({num})'

    print(response or num)

fizz_buzz()