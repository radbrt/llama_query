import sys

def print_red_square():
    print("\033[91m██\033[0m")  # Prints a red square

def print_green_checkmark():
    print("\033[92m✔\033[0m")  # Prints a green checkmark


def get_number(prompt, suggestion):
    while True:
        user_input = input(f"{prompt} (suggested: {suggestion}): ")
        if not user_input:
            return suggestion
        try:
            number = int(user_input)
            return number
        except ValueError:
            print("Please enter a valid number.")

def main():
    first_number = get_number("Enter the first number", 1)

    second_number = get_number("Enter the second number", first_number + 1)
    if second_number <= first_number:
        print_red_square()
        main()  # Restart the process
        return

    third_number = get_number("Enter the third number", second_number + 1)
    if third_number <= second_number:
        print_red_square()
        main()  # Restart the process
        return

    print_green_checkmark()

if __name__ == "__main__":
    main()
