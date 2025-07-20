import random
import string
import sys
try:
    import pyperclip # Attempt to import pyperclip for cross-platform clipboard support
except ImportError:
    pyperclip = None # Set to None if pyperclip is not installed

def generate_secure_password(length):
    """
    Generates a secure password with a specified length, including
    uppercase, lowercase, digits, and special characters.
    """
    if length < 4:
        # print("Password length must be at least 4 to include all character types.")
        return None # Return None to indicate failure for invalid length

    # Define character sets
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    digits = string.digits
    special_chars = string.punctuation

    # Combine all character sets for general random selection
    all_chars = lowercase_chars + uppercase_chars + digits + special_chars

    # Ensure the password contains at least one of each required type
    password_list = [
        random.choice(lowercase_chars),
        random.choice(uppercase_chars),
        random.choice(digits),
        random.choice(special_chars)
    ]

    # Fill the remaining length with random characters from all_chars
    # Ensure we don't try to add more characters than the requested length
    for _ in range(length - len(password_list)): # Corrected loop range
        password_list.append(random.choice(all_chars))

    # Shuffle the list to randomize the position of the guaranteed characters
    random.shuffle(password_list)

    # Join the list of characters to form the final password string
    return "".join(password_list)

def copy_to_clipboard(text):
    """
    Attempts to copy the given text to the clipboard using pyperclip first,
    then fallback to system-specific commands if pyperclip is not available.
    """
    if pyperclip:
        try:
            pyperclip.copy(text)
            print("Password copied to clipboard (via pyperclip).")
            return True
        except pyperclip.PyperclipException as e:
            print(f"Could not copy to clipboard via pyperclip: {e}")
            print("Trying fallback methods...")
    
    # Fallback methods if pyperclip fails or is not installed
    try:
        if sys.platform == 'win32':
            import subprocess
            subprocess.run(['clip.exe'], input=text.strip().encode('utf-8'), check=True)
            print("Password copied to clipboard (Windows fallback).")
            return True
        elif sys.platform == 'darwin':
            import subprocess
            process = subprocess.Popen('pbcopy', stdin=subprocess.PIPE)
            process.communicate(input=text.strip().encode('utf-8'))
            print("Password copied to clipboard (macOS fallback).")
            return True
        elif sys.platform.startswith('linux'):
            import subprocess
            # Try xclip first
            try:
                subprocess.run(['xclip', '-selection', 'clipboard'], input=text.strip().encode('utf-8'), check=True)
                print("Password copied to clipboard (Linux - xclip fallback).")
                return True
            except FileNotFoundError:
                # Then try xsel
                try:
                    subprocess.run(['xsel', '-b'], input=text.strip().encode('utf-8'), check=True)
                    print("Password copied to clipboard (Linux - xsel fallback).")
                    return True
                except FileNotFoundError:
                    print("Could not copy to clipboard. Please install 'xclip' or 'xsel' (e.g., sudo apt install xclip or sudo apt install xsel).")
                    return False
        else:
            print("Clipboard copying not natively supported on this OS without 'pyperclip' or additional setup.")
            return False
    except Exception as e:
        print(f"Error during clipboard copy fallback: {e}")
        return False


if __name__ == "__main__":
    # Developer information displayed at the start
    print("Developed by Akash Madhukar")
    print("-" * 30)
    print("--- Secure Password Generator ---")

    while True:
        try:
            desired_length_str = input("Enter the desired password length (minimum 4): ")
            desired_length = int(desired_length_str)
            if desired_length < 4:
                print("Password length must be at least 4. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number for the length.")
        except KeyboardInterrupt: # Handle Ctrl+C gracefully during input
            print("\nExiting password generator. Goodbye!")
            sys.exit()

    generated_password = generate_secure_password(desired_length)

    if generated_password:
        print(f"\nYour generated password: {generated_password}")

        if pyperclip is None:
            print("\nNote: 'pyperclip' library not found. Clipboard functionality might be limited or require manual copy.")
            print("To enable robust clipboard copying, install it: pip install pyperclip")

        while True:
            copy_choice = input("Do you want to copy the password to clipboard? (yes/no): ").lower()
            if copy_choice == 'yes':
                if not copy_to_clipboard(generated_password):
                    print("Failed to copy password automatically. Please copy it manually:")
                    print(generated_password)
                break
            elif copy_choice == 'no':
                print("Password not copied.")
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
    else:
        print("Password generation failed (due to invalid length or an internal error).")

    # Professional closing with LinkedIn profile
    print("\n" + "=" * 40) # A more prominent separator
    print("Connect with me on LinkedIn:")
    print("Akash Madhukar")
    print("Profile: https://www.linkedin.com/in/mrakashmadhukar/")
    print("=" * 40)
    print("Thank you for using the Secure Password Generator!")
    print("Stay secure!")