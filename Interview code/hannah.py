"""
Course: CSE 251
Lesson Week: 11
File: Assignment.py
"""


def is_it_a_mirror(text):
    text = text.lower()
    txet = ""
    for i in text:
        txet = i + txet

    if txet == text:
        return True
    else:
        return False
    
def main():
    print(is_it_a_mirror("hannah"))
    print(is_it_a_mirror("taco"))
    print(is_it_a_mirror("tacocat"))



if __name__ == '__main__':
    main()