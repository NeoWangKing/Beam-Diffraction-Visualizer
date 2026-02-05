import os

file_path = os.path.abspath(__file__)
print(file_path)

os.system('start cmd /k "cd {} && python main.py"'.format(os.path.dirname(file_path)))