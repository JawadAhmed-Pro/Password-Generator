import string
import random
import datetime
from cryptography.fernet import Fernet

# Generate an encryption key
key = Fernet.generate_key()
cipher = Fernet(key)

# Function to check password strength
def check_password_strength(password):
    length_score = len(password) >= 8
    digit_score = any(char.isdigit() for char in password)
    upper_score = any(char.isupper() for char in password)
    symbol_score = any(char in string.punctuation for char in password)

    strength = sum([length_score, digit_score, upper_score, symbol_score])

    if strength == 4:
        return "Strong"
    elif strength == 3:
        return "Moderate"
    else:
        return "Weak"

# Function to generate a password
def generate_password():
    password_length = int(input("Enter the desired password length: "))
    include_numbers = input("Include numbers? (yes/no): ").lower() == "yes"
    include_symbols = input("Include symbols? (yes/no): ").lower() == "yes"
    include_uppercase = input("Include uppercase letters? (yes/no): ").lower() == "yes"

    # Define character sets
    lowercase_letters = list(string.ascii_lowercase)
    uppercase_letters = list(string.ascii_uppercase) if include_uppercase else []
    numbers = list(string.digits) if include_numbers else []
    symbols = list(string.punctuation) if include_symbols else []

    # Combine all character sets
    all_characters = lowercase_letters + uppercase_letters + numbers + symbols

    # Generate and shuffle password
    password = ''.join(random.choice(all_characters) for _ in range(password_length))
    password_list = list(password)
    random.shuffle(password_list)
    final_password = ''.join(password_list)

    # Check and print password strength
    strength = check_password_strength(final_password)
    print(f"Generated Password: {final_password}")
    print(f"Password Strength: {strength}")

    password_label = input("Enter the name or purpose of this password: ")
    encrypted_password = cipher.encrypt(final_password.encode())

    # Set expiry date
    expiry_date = datetime.datetime.now() + datetime.timedelta(days=30)

    # Save password to file
    with open("passwords.txt", "a") as file:
        file.write(f"{password_label}: {encrypted_password.decode()} (Expires on: {expiry_date.strftime('%Y-%m-%d')})\n")

    print(f"The password has been saved in 'passwords.txt' with the label: {password_label}")

# Function to retrieve a password
def retrieve_password(label):
    with open("passwords.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            if label in line:
                encrypted_part = line.split(": ")[1].split(" (")[0]
                decrypted_password = cipher.decrypt(encrypted_part.encode()).decode()
                print(f"Retrieved Password for {label}: {decrypted_password}")
                return
    print("Password not found.")

# Function to update a password
def update_password(label, new_password):
    encrypted_new_password = cipher.encrypt(new_password.encode())
    with open("passwords.txt", "r") as file:
        lines = file.readlines()

    with open("passwords.txt", "w") as file:
        for line in lines:
            if label in line:
                file.write(f"{label}: {encrypted_new_password.decode()} (Updated on: {datetime.datetime.now().strftime('%Y-%m-%d')})\n")
            else:
                file.write(line)

# Menu for user to select operations
def menu():
    while True:
        print("\nSelect an operation:")
        print("1. Generate a password")
        print("2. Retrieve a password")
        print("3. Update a password")
        print("4. Check password strength")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == "1":
            generate_password()
        elif choice == "2":
            retrieve_label = input("Enter the label of the password to retrieve: ")
            retrieve_password(retrieve_label)
        elif choice == "3":
            label = input("Enter the label of the password to update: ")
            new_password = input("Enter the new password: ")
            update_password(label, new_password)
            print(f"Password for {label} updated.")
        elif choice == "4":
            password = input("Enter the password to check its strength: ")
            strength = check_password_strength(password)
            print(f"Password Strength: {strength}")
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please choose again.")

# Run the menu
menu()


