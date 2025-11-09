import re
import math
import argparse
import secrets
import string
import os
import sys
from datetime import datetime

# Password Analyzer Module
def calculate_entropy(password: str) -> float:
    """Estimate password entropy (bits)."""
    pool = 0
    if re.search(r"[a-z]", password): pool += 26
    if re.search(r"[A-Z]", password): pool += 26
    if re.search(r"[0-9]", password): pool += 10
    if re.search(r"[^a-zA-Z0-9]", password): pool += 32
    if pool == 0 or len(password) == 0:
        return 0.0
    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)


def has_repeated_sequence(pwd: str) -> bool:
    """Check for repeated characters like 'aaa' or '111'."""
    return re.search(r"(.)\1\1", pwd) is not None


def is_keyboard_pattern(pwd: str) -> bool:
    """Check for simple patterns like qwerty or 1234."""
    lowered = pwd.lower()
    patterns = ["qwerty", "asdf", "1234", "password", "abcd", "1111"]
    return any(p in lowered for p in patterns)


def check_strength(password: str, blacklist: set = None) -> dict:
    """Analyze password strength and return structured result."""
    score = 0
    remarks = []

    # Length scoring
    if len(password) >= 16:
        score += 3
    elif len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        remarks.append("Too short (min 8 chars)")

    # Character variety
    if re.search(r"[a-z]", password): score += 1
    else: remarks.append("Add lowercase letters")

    if re.search(r"[A-Z]", password): score += 1
    else: remarks.append("Add uppercase letters")

    if re.search(r"[0-9]", password): score += 1
    else: remarks.append("Add digits")

    if re.search(r"[^a-zA-Z0-9]", password): score += 1
    else: remarks.append("Add symbols (!, @, #, etc.)")

    # Penalties
    if has_repeated_sequence(password):
        remarks.append("Contains repeated characters")
        score -= 1
    if is_keyboard_pattern(password):
        remarks.append("Contains common pattern (qwerty/1234)")
        score -= 1

    # Blacklist
    blacklisted = False
    if blacklist is not None and password.lower() in blacklist:
        blacklisted = True
        remarks.append("Found in common-password blacklist")
        score -= 2

    # Entropy calculation
    entropy = calculate_entropy(password)
    if score < 0:
        score = 0
    if score > 8:
        score = 8

    # Strength level
    if blacklisted:
        level = "Very Weak"
    elif entropy >= 80 and score >= 6:
        level = "Strong"
    elif entropy >= 50 and score >= 4:
        level = "Medium"
    else:
        level = "Weak"

    return {
        "password": password,
        "length": len(password),
        "entropy": entropy,
        "score": score,
        "level": level,
        "remarks": remarks,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# Password Generator
def generate_password(length: int = 16, use_upper=True, use_digits=True, use_symbols=True) -> str:
    """Generate a cryptographically secure password."""
    charset = string.ascii_lowercase
    if use_upper: charset += string.ascii_uppercase
    if use_digits: charset += string.digits
    if use_symbols: charset += "!@#$%^&*()-_=+[]{};:,.<>/?"
    return ''.join(secrets.choice(charset) for _ in range(length))


# Blacklist Loader
def load_blacklist(path="common_pass.txt") -> set:
    """Load a blacklist file from the script's directory, if it exists."""
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, path)
    if not os.path.isfile(file_path):
        print(f"Blacklist file not found at: {file_path}")
        return set()
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return set(line.strip().lower() for line in f if line.strip())



# Pretty Output
def print_result(result: dict):
    """Display password analysis report."""
    level = result["level"]
    entropy = result["entropy"]
    length = result["length"]

    print("\n Password Strength Report ")
    print("-------------------------------")
    print(f"Password : {result['password']}")
    print(f"Length   : {length}")
    print(f"Entropy  : {entropy} bits")
    print(f"Strength : {level}")
    print(f"Score    : {result['score']}/8")

    if result["remarks"]:
        print("\nSuggestions:")
        for r in result["remarks"]:
            print(" - " + r)


# CLI Main
def main():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer and Generator")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-p", "--password", help="Password to analyze")
    group.add_argument("-f", "--file", help="File with passwords (one per line)")
    group.add_argument("-g", "--generate", action="store_true", help="Generate a secure password")

    parser.add_argument("--gen-length", type=int, default=16, help="Password length for generator")
    parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase letters")
    parser.add_argument("--no-digits", action="store_true", help="Exclude digits")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    parser.add_argument("--blacklist", default="common_pass.txt", help="Path to blacklist file")


    args = parser.parse_args()

    # Load blacklist
    blacklist = load_blacklist(args.blacklist)

    # Generate password
    if args.generate:
        pwd = generate_password(
            length=args.gen_length,
            use_upper=not args.no_upper,
            use_digits=not args.no_digits,
            use_symbols=not args.no_symbols,
        )
        print(f"\nGenerated password: {pwd}")
        result = check_strength(pwd, blacklist)
        print_result(result)
        return

    # Analyze single password
    if args.password:
        result = check_strength(args.password, blacklist)
        print_result(result)
        return

    # Analyze multiple passwords from file
    if args.file:
        if not os.path.isfile(args.file):
            print("Error: file not found.")
            sys.exit(1)
        with open(args.file, "r", encoding="utf-8", errors="ignore") as f:
            passwords = [line.strip() for line in f if line.strip()]
        for pwd in passwords:
            result = check_strength(pwd, blacklist)
            print_result(result)
        print(f"\nAnalyzed {len(passwords)} passwords.")
        return

    # Default interactive mode
    password = input("Enter a password to analyze: ")
    if not password:
        print("No password entered.")
        sys.exit(0)
    result = check_strength(password, blacklist)
    print_result(result)


if __name__ == "__main__":
    main()
