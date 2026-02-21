from functions.run_python_file import run_python_file

# Test 1
print(run_python_file("calculator", "main.py"))

# Test 2
print(run_python_file("calculator", "main.py", ["3 + 5"]))

# Test 3
print(run_python_file("calculator", "tests.py"))

# Test 4
print(run_python_file("calculator", "../main.py"))

# Test 5
print(run_python_file("calculator", "nonexistent.py"))

# Test 6
print(run_python_file("calculator", "lorem.txt"))