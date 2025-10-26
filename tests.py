from functions.get_file_content import get_file_content
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file

def print_block(header, result):
    print(header)
    if result.startswith("Error:"):
        print(f"    {result}")
    else:
        for line in result.splitlines(): # breaking the multi-line string into a list of strings
            print(f"{line}")
    

def main():
    # testing with the current directory
    result1 = run_python_file("calculator", "main.py")
    print_block("Result 1: ", result1)
    print()

    # 2) 'pkg' directory
    res2 = run_python_file("calculator", "main.py", ["3 + 5"])
    print_block("Result 2: ", res2)
    print()

    # 3) '/bin' directory (outside)
    res3 = run_python_file("calculator", "tests.py")
    print_block("Result 3: ", res3)
    print()

    res4 = run_python_file("calculator", "../main.py")
    print_block("Result 4: ", res4)
    print()

    res5 = run_python_file("calculator", "nonexistent.py")
    print_block("Result 5: ", res5)
    print()

    res6 = run_python_file("calculator", "lorem.txt")
    print_block("Result 6: ", res6)
    print()

if __name__ == "__main__":
    main()


