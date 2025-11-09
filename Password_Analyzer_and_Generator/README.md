# Password Strength Analyzer (Python)

A **Python-based cybersecurity tool** that analyzes the strength of a password using **entropy, character variety, and pattern detection**.  
It also includes a **secure password generator** and optional **blacklist protection** to detect common weak passwords.

---

## Overview

This tool helps you:
- Detect weak or predictable passwords
- Understand password entropy and complexity
- Get actionable feedback for stronger passwords
- Generate secure passwords instantly

---

## Features
1. **Entropy Calculation** – measures randomness in bits  
2. **Character Variety Check** – evaluates lowercase, uppercase, digits, and symbols  
3. **Blacklist Detection** – detects passwords like `123456`, `password`, etc.  
4. **Pattern Recognition** – catches repeated or sequential patterns (e.g., `aaa`, `1234`)  
5. **Secure Password Generator** – creates random strong passwords  
6. **Multi-Mode CLI** – analyze one password, a file of passwords, or interactively  
7. **Colorized Output** – clean and readable report  

---

## How It Works
1. Entropy Calculation

Uses Shannon’s entropy approximation:
entropy = length × log₂(character_pool_size)
The more diverse and longer the password, the higher the entropy (in bits).

2. Scoring System
Criteria	Points
8–11 characters	+1
12–15 characters	+2
≥16 characters	+3
Lowercase letters	+1
Uppercase letters	+1
Digits	+1
Symbols	+1

🔻 Deductions:
Repeated sequences (like aaa) → −1
Common patterns (qwerty, 1234) → −1
Found in blacklist → −2
Total score = 0–8

🟢 Strong (≥6, entropy ≥80 bits)

🟡 Medium (≥4, entropy ≥50 bits)

🔴 Weak / Very Weak otherwise

---

## Command Reference
___________________________________________________________________________________________________________________
**Command**	                                                                |            **Description**          |
__________________________________________________________________________________________________________________|
python password_analyzer.py	                                                |       Run interactively             |
python password_analyzer.py -p "My@Pass123"	                                |       Analyze a single password     |
python password_analyzer.py -f test_passwords.txt	                          |       Analyze multiple passwords    |
python password_analyzer.py --generate                                      |   	  Generate a random password    |
python password_analyzer.py --generate --gen-length 20	                    |       Generate 20-char password     |
python password_analyzer.py -p "password" --blacklist common_passwords.txt	|       Use blacklist                 |
___________________________________________________________________________________________________________________

---

# Screenshots

<img width="1001" height="517" alt="image" src="https://github.com/user-attachments/assets/461d4a49-a64f-42ac-b769-d3e3fa5a2c0b" />
<img width="1021" height="711" alt="image" src="https://github.com/user-attachments/assets/e13e3cc1-7b74-43e4-bd99-007e53ef46b4" />
<img width="740" height="673" alt="image" src="https://github.com/user-attachments/assets/08921576-3d45-4869-8ca9-5f30c2c8178d" />
<img width="910" height="649" alt="image" src="https://github.com/user-attachments/assets/bc31d73a-1ddb-46d9-8266-84bda6835ef0" />
<img width="1046" height="707" alt="image" src="https://github.com/user-attachments/assets/b9865ef9-e021-46ec-9d4b-5eed77f5befc" />
<img width="1157" height="839" alt="image" src="https://github.com/user-attachments/assets/4a135928-c6e4-4464-919c-76d635d32c2a" />
