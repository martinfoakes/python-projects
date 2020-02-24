from mpmath import mp

user_pi_count = 0 
while True:
    try: 
        user_pi_count = int(input("Enter a Number to generate Pi up to that many decimal points: "))
    except ValueError:
        print("Error: Input must be an integer")
        continue
    else:
        mp.dps = user_pi_count
        print(f"Pi up to {user_pi_count} places is -> ")
        print(mp.pi)
        break