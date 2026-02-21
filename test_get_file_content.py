from functions.get_file_content import get_file_content
import config

content = get_file_content("calculator", "lorem.txt")

assert isinstance(content, str)
assert len(content) > 0
assert f'truncated at {config.MAX_CHARS} characters' in content

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))