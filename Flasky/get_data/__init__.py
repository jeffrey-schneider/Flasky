import os

dir_path = os.path.dirname(os.path.realpath(__file__))

file_name = "creds.txt"
file_path = dir_path + "/" + file_name


def read_credentials(file_path):
    credentials = {}
    print(f"{file_path}")
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            name, value = line.strip().split('=')
            credentials[name.strip()] = value.strip().strip("'")  #The extra strip removes the `'` from the string
    print(f"{credentials}")
    return credentials


