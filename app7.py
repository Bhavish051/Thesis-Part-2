import os

path = ". ./finalData/"

os.chdir(path)

def read_file(file_path) :
    with open(file_path, "r") as f :
        return f.read()
    
    
for file in os.listdir(path) :
    print(file)
    data = read_file(file)
    print(data)