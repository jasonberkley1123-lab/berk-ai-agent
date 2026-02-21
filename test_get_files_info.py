from functions.get_files_info import get_files_info

# Test 1
print("Result for current directory:")
print(f"{get_files_info('calculator', '.')}")

# Test 2
print("Result for 'pkg' directory:")
print(f"{get_files_info('calculator', 'pkg')}")

# Test 3
print("Result for '/bin' directory:")
print(f"{get_files_info('calculator', '/bin')}")

# Test 4
print("Result for '../' directory:")
print(f"{get_files_info('calculator', '../')}")