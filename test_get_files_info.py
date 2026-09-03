from functions.get_files_info import get_files_info

# test 1
print(get_files_info("calculator", "."))
# test 2
print(get_files_info("calculator", "/bin"))
# test 3
print(get_files_info("calculator", "../"))
# test 4
print(get_files_info("calculator", "main.py"))
