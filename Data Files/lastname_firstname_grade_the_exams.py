filename = input("Enter a filename: ")
try:
    with open(filename, "r") as file1:
        FileContent = file1.read()
        print(FileContent)
except:
    print("File cannot found!")